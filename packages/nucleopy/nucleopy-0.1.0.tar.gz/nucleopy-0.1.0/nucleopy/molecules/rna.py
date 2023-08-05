"""
Creates an RNA object which contains a nucleotide sequence
"""
from nucleopy.molecules.nucleotide import Nucleotide
import re


class RNA(Nucleotide):
    def __init__(self, sequence):
        """
        Creates an RNA object
        :param sequence: String sequence of nucleotides
        """
        Nucleotide.__init__(self, sequence)

        if re.search(r'[^AUCG]', self.seq) is not None:
            raise ValueError("Not a valid RNA sequence")

    def complement(self):
        """
        Gets the complement strand of the RNA
        :return: Complement of the RNA sequence
        """

        rna_seq = []
        for base in self.seq:
            if base == "A":
                rna_seq.append("U")
            elif base == "U":
                rna_seq.append("A")
            elif base == "G":
                rna_seq.append("C")
            elif base == "C":
                rna_seq.append("G")

        return RNA(''.join(rna_seq))

    def toDNA(self):
        """
        Converts RNA to DNA
        :return: DNA sequence
        """

        from nucleopy.molecules.dna import DNA
        dna_seq = self.seq.replace("U", "T")
        return DNA(dna_seq)

    def toProtein(self):
        """
        Converts RNA to protein
        :return: Amino Acid sequence
        """

        protein = []
        amino_split = lambda x, n, acc=[]: amino_split(x[n:], n, acc + [(x[:n])]) if x else acc

        codons = {"UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
               "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
               "UAU": "Tyr", "UAC": "Tyr", "UAA": "STOP", "UAG": "STOP",
               "UGU": "Cys", "UGC": "Cys", "UGA": "STOP", "UGG": "Trp",
               "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
               "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
               "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
               "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
               "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
               "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
               "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
               "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
               "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
               "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
               "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
               "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly"}

        if len(self.seq) % 3 != 0:
            raise ValueError("Not in sets of three")
        set3 = amino_split(self.seq, 3)

        for codon in set3:
            protein.append(codons[codon])

        return (protein)


    def Viennafold(self):
        """
        Returns structure and energy of the RNA sequence
        :return: Structure (in dot-bracket) and energy (in kcal)
        """

        try:
            import RNA
            struc, energy = RNA.fold(self.seq)
            return struc, energy
        except ImportError:
            print ("ViennaRNA Python library not installed. "
                   "Please see config-ViennaRNA.md for installation details.")

    def ViennaTargetEnergy(self, target_structure):
        """
        Gets energy of RNA molecule forced to fold into a certain shape
        :param target_structure: The forced structure
        :return: Free energy (in kcal)
        """

        try:
            if len(self.seq) != len(target_structure):
                raise ValueError("Nucleotide sequence and structure not of same length")
            import RNA
            e = RNA.energy_of_structure(self.seq, target_structure, 0)
            return e
        except ImportError:
            raise ImportError("ViennaRNA Python library not installed. "
                   "Please see config-ViennaRNA.md for installation details.")
