"""
Creates a DNA object which contains a nucleotide sequence
"""
from nucleopy.molecules.nucleotide import Nucleotide
import re


class DNA(Nucleotide):
    def __init__(self, sequence):
        """
        Creates a DNA object
        :param sequence: String sequence of nucleotides
        """
        Nucleotide.__init__(self, sequence)

        if re.search(r'[^ATCG]', self.seq) is not None:
            raise ValueError("Not a valid DNA sequence")

    def complement(self):
        """
        Gets the complement strand of the DNA
        :return: Complement of the DNA sequence
        """

        dna_seq = []
        for base in self.seq:
            if base == "A":
                dna_seq.append("T")
            elif base == "T":
                dna_seq.append("A")
            elif base == "G":
                dna_seq.append("C")
            elif base == "C":
                dna_seq.append("G")

        return DNA(''.join(dna_seq))

    def toRNA(self):
        """
        Converts the DNA to RNA
        :return: RNA sequence
        """

        from nucleopy.molecules.rna import RNA
        rna_seq = self.seq.replace("T", "U")

        return RNA(rna_seq)
