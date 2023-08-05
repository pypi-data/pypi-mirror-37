import rnftools
from .Source import *

import os
import snakemake
import re


class CuReSim(Source):
    """Class for CuReSim (http://www.pegase-biosciences.com/curesim-a-customized-read-simulator).

	Only single-end reads simulations are supported.

	Args:
		fasta (str): File name of the genome from which reads are created (FASTA file). Corresponding CuReSim parameter: ``-f``.
		sequences (set of int or str): FASTA sequences to extract. Sequences can be specified either by their ids, or by their names.
		coverage (float): Average coverage of the genome (if number_of_reads specified, then it must be equal to zero).
		number_of_read_tuples (int): Number of read tuples (if coverage specified, then it must be equal to zero). Corresponding CuReSim parameter: ``-n``.
		read_length_1 (int): Length of the first read.  Corresponding CuReSim parameter: ``-m``.
		read_length_2 (int): Length of the second read. Fake parameter (unsupported by CuReSim).
		random_reads (bool): Simulate random reads (see CuReSim documentation for more details).
		rng_seed (int): Seed for simulator's random number generator. Fake parameter (unsupported by CuReSim).
		other_params (str): Other parameters which are used on command-line.

	Raises:
		ValueError
	"""

    def __init__(
        self,
        fasta,
        sequences=None,
        coverage=0,
        number_of_read_tuples=0,
        read_length_1=100,
        read_length_2=0,
        random_reads=False,
        rng_seed=1,
        other_params="",
    ):

        if read_length_2 != 0:
            rnftools.utils.error(
                "CuReSim supports only single-end reads",
                program="RNFtools",
                subprogram="MIShmash",
                exception=ValueError,
            )

        super().__init__(
            fasta=fasta,
            sequences=sequences,
            reads_in_tuple=1,
            rng_seed=rng_seed,
            number_of_required_cores=9999,
        )

        self.read_length_1 = read_length_1
        self.read_length_2 = read_length_2
        self.random_reads = random_reads
        self.other_params = other_params

        coverage = float(coverage)
        number_of_read_tuples = int(number_of_read_tuples)
        if coverage * number_of_read_tuples != 0:
            rnftools.utils.error(
                "coverage or number_of_read_tuples must be equal to zero",
                program="RNFtools",
                subprogram="MIShmash",
                exception=ValueError,
            )

        self.number_of_read_tuples = number_of_read_tuples
        self.coverage = coverage

    def get_input(self):
        return [
            self._fa_fn,
            self._fai_fn,
        ]

    def get_output(self):
        return [
            self._fq_fn,
            os.path.join(
                self.get_dir(),
                "output.fastq",
            ),
            os.path.join(
                self.get_dir(),
                "log.txt",
            ),
        ]

    # todo: check if "output.fastq" is defined as an output file
    def create_fq(self):
        if self.number_of_read_tuples == 0 and self.number_of_read_tuples == 0:
            for x in self.get_output():
                with open(x, "w+") as f:
                    f.write(os.linesep)
        else:
            if self.number_of_read_tuples == 0:
                genome_size = os.stat(self._fa_fn).st_size
                self.number_of_read_tuples = int(
                    self.coverage * genome_size / (self.read_length_1 + self.read_length_2)
                )

            if self.random_reads:
                no_normal_reads = 1
                no_random_reads = self.number_of_read_tuples
            else:
                no_normal_reads = self.number_of_read_tuples
                no_random_reads = 0

            rnftools.utils.shell(
                """
					(cd "{dir}" && \
					"{curesim}" \
					-f "{fa}" \
					-n {no_normal} \
					-r {no_random} \
					-m {rlen1} \
					-sd 0 \
					-y 0 \
					{other_params} \
					> /dev/null)
				""".format(
                    dir=self.get_dir(),
                    curesim="curesim",
                    fa=self._fa_fn,
                    no_normal=no_normal_reads,
                    no_random=no_random_reads,
                    rlen1=self.read_length_1,
                    other_params=self.other_params,
                    rng_seed=self._rng_seed,
                )
            )

            curesim_fastq_fn = os.path.join(
                self.get_dir(),
                "output.fastq",
            )

            with open(curesim_fastq_fn, "r+") as curesim_fastq_fo:
                with open(self._fai_fn) as fai_fo:
                    with open(self._fq_fn, "w+") as rnf_fastq_fo:
                        self.recode_curesim_reads(
                            curesim_fastq_fo=curesim_fastq_fo,
                            rnf_fastq_fo=rnf_fastq_fo,
                            fai_fo=fai_fo,
                            genome_id=self.genome_id,
                            number_of_read_tuples=10**9,
                            recode_random=self.random_reads,
                        )

    @staticmethod
    def recode_curesim_reads(
        curesim_fastq_fo,
        rnf_fastq_fo,
        fai_fo,
        genome_id,
        number_of_read_tuples=10**9,
        recode_random=False,
    ):
        """Recode CuReSim output FASTQ file to the RNF-compatible output FASTQ file.

		Args:
			curesim_fastq_fo (file object): File object of CuReSim FASTQ file.
			fastq_rnf_fo (file object): File object of RNF FASTQ.
			fai_fo (file object): File object for FAI file of the reference genome.
			genome_id (int): RNF genome ID to be used.
			number_of_read_tuples (int): Expected number of read tuples (to estimate number of digits in RNF).
			recode_random (bool): Recode random reads.

		Raises:
			ValueError
		"""

        curesim_pattern = re.compile('@(.*)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)')
        """
			CuReSim read name format

			@<#1>_<#2>_<#3>_<#4>_<#5>_<#6>_<#7>_<#8>

			1: contig name
			2: original position
			3: strand (0=forward;1=reverse)
			4: random read (0=non-random;1=random)
			5: number of insertions
			6: number of deletions
			7: number of substitution
			8: read number (unique within a genome)
		"""

        max_seq_len = 0

        fai_index = rnftools.utils.FaIdx(fai_fo=fai_fo)
        read_tuple_id_width = len(format(number_of_read_tuples, 'x'))

        fq_creator = rnftools.rnfformat.FqCreator(
            fastq_fo=rnf_fastq_fo,
            read_tuple_id_width=read_tuple_id_width,
            genome_id_width=2,
            chr_id_width=fai_index.chr_id_width,
            coor_width=fai_index.coor_width,
            info_reads_in_tuple=True,
            info_simulator="curesim",
        )

        # parsing FQ file
        read_tuple_id = 0

        i = 0
        for line in curesim_fastq_fo:
            if i % 4 == 0:
                m = curesim_pattern.search(line)
                if m is None:
                    rnftools.utils.error(
                        "Read '{}' was not generated by CuReSim.".format(line[1:]), program="RNFtools",
                        subprogram="MIShmash", exception=ValueError
                    )

                contig_name = m.group(1)
                start_pos = int(m.group(2))
                direction = "R" if int(m.group(3)) else "F"
                random = bool(m.group(4))
                ins_nb = int(m.group(5))
                del_nb = int(m.group(6))
                subst_nb = int(m.group(7))
                rd_id = int(m.group(8))

                end_pos = start_pos - 1 - ins_nb + del_nb

                chr_id = 0

                random = contig_name[:4] == "rand"

            # TODO: uncomment when the chromosome naming bug in curesim is corrected
            # chr_id = self.dict_chr_ids[contig_name] if self.dict_chr_ids!={} else "0"

            elif i % 4 == 1:
                bases = line.strip()
                end_pos += len(bases)

                if recode_random:
                    left = 0
                    right = 0
                else:
                    left = start_pos + 1
                    right = end_pos

                segment = rnftools.rnfformat.Segment(
                    genome_id=genome_id,
                    chr_id=chr_id,
                    direction=direction,
                    left=left,
                    right=right,
                )

            elif i % 4 == 2:
                pass

            elif i % 4 == 3:
                qualities = line.strip()

                if random == recode_random:
                    fq_creator.add_read(
                        read_tuple_id=read_tuple_id,
                        bases=bases,
                        qualities=qualities,
                        segments=[segment],
                    )

                read_tuple_id += 1

            i += 1

        fq_creator.flush_read_tuple()
