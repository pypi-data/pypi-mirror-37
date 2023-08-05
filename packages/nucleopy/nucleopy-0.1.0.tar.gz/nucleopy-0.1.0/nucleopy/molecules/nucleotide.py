"""
Molecule superclass for DNA and RNA classes
"""
import re


class Nucleotide(object):
    def __init__(self, sequence):
        """
        Creates an RNA object
        :param sequence: String sequence of nucleotides
        """

        self.seq = sequence
        self.seq = self.seq.upper()

    def __str__(self):
        """
        Printable representation of Nucleotide object
        :return: Sequence
        """

        return self.seq

    def __len__(self):
        """
        Gets length of sequence
        :return: Integer length of nucleotide sequence
        """

        return len(self.seq)

    def __iter__(self):
        """
        Iterates over sequence
        """

        for i in self.seq:
            yield i

    def __getitem__(self, item):
        """
        Allows for indexing
        :param item: Index
        """

        if isinstance(item, slice):
            return ''.join([self[ii] for ii in range(*item.indices(len(self)))])

        elif isinstance(item, int):
            if item < 0:
                item += len(self)
            if item >= len(self):
                raise IndexError("Index out of range")
            return self.seq[item]
        else:
            raise TypeError("Invalid argument")

    def __setitem__(self, key, value):
        """
        Supports assignment
        :param key: Index
        :param value: String of new sequence
        """
        from nucleopy.molecules.dna import DNA
        from nucleopy.molecules.rna import RNA

        s = []
        for ch in self.seq:
            s.append(ch)

        if isinstance(key, slice):
            # return ''.join([self[ii] for ii in range(*key.indices(len(self)))])

            for ii in range(*key.indices(len(self))):
                s[ii] = value[ii]
            self.seq = ''.join(s)

        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self):
                raise IndexError("Index out of range")
            s[key] = value
            self.seq = ''.join(s)

        else:
            raise TypeError("Invalid argument")

        self.seq = self.seq.upper()

        if type(self) == DNA:
            if re.search(r'[^ATCG]', self.seq) is not None:
                raise TypeError("Not a valid DNA sequence")

        if type(self) == RNA:
            if re.search(r'[^AUCG]', self.seq) is not None:
                raise TypeError("Not a valid RNA sequence")

    def sequence(self):
        """
        Returns a sequence
        :return: Sequence
        """
        return self.seq

    def setSequence(self, new_sequence):
        """
        Sets a new sequence
        :param new_sequence: New sequence to be in the Nucleotide object
        """
        from nucleopy.molecules.dna import DNA
        from nucleopy.molecules.rna import RNA

        self.seq = new_sequence
        self.seq = self.seq.upper()

        if type(self) == DNA:
            if re.search(r'[^ATCG]', self.seq) is not None:
                raise TypeError("Not a valid DNA sequence")

        if type(self) == RNA:
            if re.search(r'[^AUCG]', self.seq) is not None:
                raise TypeError("Not a valid RNA sequence")

    def onehot(self):
        """
        Turns DNA sequence into one-hot encoded list
        :return: List of one-hots
        """

        seq = []
        for base in self.seq:
            if base == "A":
                seq.append([1,0,0,0])
            elif base == "T" or base == 'U':
                seq.append([0,1,0,0])
            elif base == "G":
                seq.append([0,0,1,0])
            elif base == "C":
                seq.append([0,0,0,1])

        return seq

    def integerEncoding(self):
        """
        Turns DNA sequence into integer-encoded list
        :return: List of integers
        """

        seq = []
        for base in self.seq:
            if base == "A":
                seq.append(1)
            elif base == "T" or base == 'U':
                seq.append(2)
            elif base == "G":
                seq.append(3)
            elif base == "C":
                seq.append(4)

        return seq

    @classmethod
    def __compatible(cls, base1, base2):
        """
        Helper function to determine if two bases can be paired
        :param base1: Nucleotide 1
        :param base2: Nucleotide 2
        :return: True of bases can be paired; false otherwise
        """

        if (base1 == 'A' and base2 == 'T') or (base1 == 'T' and base2 == 'A'):
            return True
        elif (base1 == 'G' and base2 == 'C') or (base1 == 'C' and base2 == 'G'):
            return True
        elif (base1 == 'A' and base2 == 'U') or (base1 == 'U' and base2 == 'A'):
            return True
        else:
            return False

    def isComplement(self, otherseq):
        """
        Checks of two sequences are complements
        :param otherseq: Another DNA sequence
        :return: True if strands are complements; false otherwise
        """

        if len(self.seq) != len(otherseq):
            raise ValueError("Sequences not of same length")
        else:
            for i in range(len(otherseq)):
                if not Nucleotide.__compatible(self.seq[i], otherseq[i]):
                    return False

            return True
