import os
import sys
import random
import math
import resource

import rnftools.rnfformat

# number of reads taken in a single run
READS_IN_GROUP = 10

ALLOWED_MODES = [
    "single-end",
    "paired-end-bwa",
    "paired-end-bfast",
]


class FqMerger:
    """Class for merging several RNF FASTQ files.

	Args:
		mode (str): Output mode (single-end / paired-end-bwa / paired-end-bfast).
		input_files_fn (list): List of file names of input FASTQ files.
		output_prefix (str): Prefix for output FASTQ files.
	"""

    def __init__(self, mode, input_files_fn, output_prefix):

        # basic variables
        self.mode = mode
        self.input_files_fn = input_files_fn
        self.output_prefix = output_prefix
        self.rng = random.Random()
        self.rng.seed(1)

        # single-file or multi-file mode
        files_to_be_opened_estimate = 2 + len(input_files_fn) + 10  # 1 or 2 output files; input files; backup
        (os_allowed_files, _) = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(len(input_files_fn), files_to_be_opened_estimate, os_allowed_files)
        self.keep_files_open = os_allowed_files > files_to_be_opened_estimate  # autodetection

        # input files
        self.i_files = [FileReader(fn, keep_file_open=self.keep_files_open) for fn in input_files_fn]
        self.i_files_sizes = [os.path.getsize(fn) for fn in input_files_fn]
        self.i_files_proc = [math.ceil((100.0 * x) / sum(self.i_files_sizes)) for x in self.i_files_sizes]
        self.i_files_weighted = []
        for i in range(len(self.i_files)):
            self.i_files_weighted.extend(self.i_files_proc[i] * [self.i_files[i]])

        # output files
        read_tuple_id_length_est = math.ceil(math.log(
            sum(self.i_files_sizes) / 20,
            16,
        ))

        if mode == "single-end":
            self.output_files_fn = ["{}.fq".format(output_prefix)]
            self.output = FqMergerOutput(
                fq_1_fn=self.output_files_fn[0],
                reads_in_tuple=1,
                read_tuple_id_width=read_tuple_id_length_est,
            )
            self._reads_in_tuple = 1
        elif mode == "paired-end-bwa":
            self.output_files_fn = [
                "{}.1.fq".format(output_prefix),
                "{}.2.fq".format(output_prefix),
            ]
            self.output = FqMergerOutput(
                fq_1_fn=self.output_files_fn[0],
                fq_2_fn=self.output_files_fn[1],
                reads_in_tuple=2,
                read_tuple_id_width=read_tuple_id_length_est,
            )
            self._reads_in_tuple = 2
        elif mode == "paired-end-bfast":
            self.output_files_fn = ["{}.fq".format(output_prefix)]
            self.output = FqMergerOutput(
                fq_1_fn=self.output_files_fn[0],
                reads_in_tuple=2,
                read_tuple_id_width=read_tuple_id_length_est,
            )
            self._reads_in_tuple = 2
        else:
            raise ValueError("Unknown mode '{}'".format(mode))

    def run(self):
        """Run merging.
		"""

        print("", file=sys.stderr)
        print("Going to merge/convert RNF-FASTQ files.", file=sys.stderr)
        print("", file=sys.stderr)
        print("   mode:          ", self.mode, file=sys.stderr)
        print("   input files:   ", ", ".join(self.input_files_fn), file=sys.stderr)
        print("   output files:  ", ", ".join(self.output_files_fn), file=sys.stderr)
        print("", file=sys.stderr)

        while len(self.i_files_weighted) > 0:
            file_id = self.rng.randint(0, len(self.i_files_weighted) - 1)
            for i in range(READS_IN_GROUP * self._reads_in_tuple):
                if self.i_files_weighted[file_id].closed:
                    del self.i_files_weighted[file_id]
                    break

                ln1 = self.i_files_weighted[file_id].readline()
                ln2 = self.i_files_weighted[file_id].readline()
                ln3 = self.i_files_weighted[file_id].readline()
                ln4 = self.i_files_weighted[file_id].readline()

                if ln1 == "" or ln2 == "" or ln3 == "" or ln4 == "":
                    self.i_files_weighted[file_id].close()
                    del self.i_files_weighted[file_id]
                    break
                assert ln1[0] == "@", ln1
                assert ln3[0] == "+", ln3
                self.output.save_read(ln1, ln2, ln3, ln4)
        self.output.close()


class FileReader:
    """Class for reading a file without "OSError: Too many open files".
	If keep_file_open==True, data are read in small batches and files are being reopened
	and closed for each reading. Last position in file is kept.

	Args:
		fn (str): File name of the file to be read.
		keep_file_open (bool): Keep the file open.
		buffer_lines (int): Number of lines read as a single batch.
	"""

    def __init__(self, fn, keep_file_open=False, buffer_lines=50):
        self.fn = fn
        self.keep_file_open = keep_file_open

        if self.keep_file_open:
            self.fo = open(fn)
        else:
            self.fo = None
            self.buffer = []
            self.buffer_lines = buffer_lines
            self._closed = False
            self.file_pos = 0

    def readline(self):
        if self.keep_file_open:
            return self.fo.readline()
        else:
            if len(self.buffer) == 0:
                self.fo = open(self.fn)
                self.fo.seek(self.file_pos)
                for _ in range(self.buffer_lines):
                    line = self.fo.readline()
                    self.buffer.append(line)
                self.file_pos = self.fo.tell()
                self.fo.close()

            return self.buffer.pop(0)

    def close(self):
        if self.keep_file_open:
            self.fo.close()
        else:
            self._closed = True

    @property
    def closed(self):
        if self.keep_file_open:
            return self.fo.closed
        else:
            return self._closed


class FqMergerOutput:
    """Class for output of FqMerger.

	Args:
		reads_in_tuple (int): Number of reads in a tuple.
		fq_1_fn (str): File name of first output FASTQ.
		fq_2_fn (str): File name of second output FASTQ.
		read_tuple_id_width: Width of Read ID.
	"""

    def __init__(self, reads_in_tuple, fq_1_fn, fq_2_fn=None, read_tuple_id_width=6):
        self.reads_in_tuple = reads_in_tuple
        self.fs = [open(fq_1_fn, "w+")]
        if fq_2_fn is not None:
            self.fs.append(open(fq_2_fn, "w+"))
        self.read_tuple_counter = 1
        self.rnf_profile = rnftools.rnfformat.RnfProfile(read_tuple_id_width=read_tuple_id_width)

    def __del__(self):
        for f in self.fs:
            if not f.closed:
                f.close()

    def close(self):
        for f in self.fs:
            f.close()

    def save_read(self, ln1, ln2, ln3, ln4):
        [ln1, ln2, ln3, ln4] = [ln1.strip(), ln2.strip(), ln3.strip(), ln4.strip()]

        ln1 = self.rnf_profile.apply(read_tuple_name=ln1, read_tuple_id=self.read_tuple_counter)

        if self.reads_in_tuple == 1:
            file_id = 0
            if ln1[-2] == "/":
                raise ValueError("Wrong read name '{}'. Single end read should not contain '/'.".format(ln1[1:]))
            self.read_tuple_counter += 1

        else:
            if ln1[-2] != "/":
                raise ValueError("Wrong read name '{}'. A read with two ends should contain '/'.".format(ln1[1:]))
            if len(self.fs) == 1:
                ln1 = ln1[:-2]
                file_id = 0
                self.read_tuple_counter += 1
            else:
                if ln1[-1] == "1":
                    file_id = 0
                elif ln1[-1] == "2":
                    file_id = 1
                    self.read_tuple_counter += 1
                else:
                    raise ValueError("Wrong read name '{}'.".format(ln1[1:]))

        self.fs[file_id].write("".join([ln1, os.linesep, ln2, os.linesep, ln3, os.linesep, ln4, os.linesep]))
