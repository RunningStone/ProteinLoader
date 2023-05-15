"""
proteinLoader数据读取和写入的部分
为了保持尽可能少的依赖项 使用了BioPython和pickle

"""

from ProteinLoader import logger
import pandas as pd

class Parser_wrapper:
    """
    Wrapper class for the parsers 
    all data should be read into pandas dataframe
    """
    def __init__(self,):
        # check whether BioPython is installed
        try:
            import Bio # import BioPython
        except ImportError:
            logger.info("BioPython is not installed.")
            #raise ImportError("need to install BioPython as parser")
        else:
            self.active_biopython = "BioPython"

        # check whether biopanda is installed
        try:
            import biopandas # import biopanda
        except ImportError: 
            logger.info("biopandas is not installed.")
            #raise ImportError("need to install biopandas as parser")
        else:
            self.active_biopandas = "biopandas"

    def init_parsers(self):
        """
        Return the parsers.
        """
        if self.active_biopython == "BioPython":
            from Bio import SeqIO
            from Bio.PDB import PDBParser, MMCIFParser
            self.fasta_parser = SeqIO
            self.pdb_parser = PDBParser(QUIET=True) 
            self.mmci_parser = MMCIFParser(QUIET=True)
        if self.active_biopandas == "biopandas":
            import biopandas
            self.pdb_parser = biopandas.pdb.PandasPdb()
        else:
            raise ValueError("wrapper_flag is not valid,check whether a backend parser is installed")

    def read_fasta(self,loc):
        if self.active_biopython == "BioPython":
            records = list(self.fasta_parser.parse(loc, "fasta"))
            data = []
            for record in records:
                data.append([record.id, str(record.seq)])
                
            df = pd.DataFrame(data, columns=['id', 'sequence'])
            return df
        else:
            raise ValueError("wrapper_flag is not valid,check whether a backend parser is installed")
    

    def read_pdb(self,loc):
        if self.active_biopandas == "biopandas":
            ppdb = self.pdb_parser.read_pdb(loc)
            # TODO: 不确定是否是需要直接进入atom
            df = ppdb.df['ATOM']
            return df
        elif self.active_biopython == "BioPython":
            # read the structure
            structure = self.pdb_parser.get_structure("temp", loc)
            # save as pandas dataframe
            data = []
            for model in structure:
                for chain in model:
                    for residue in chain:
                        for atom in residue:
                            data.append([model.id, chain.id, residue.id[1], residue.id[2], atom.id, atom.coord[0], atom.coord[1], atom.coord[2]])
            df = pd.DataFrame(data, columns=['model', 'chain', 'residue_number', 'insertion', 'atom_name', 'x', 'y', 'z'])
            return df

    def read_mmcif(self,loc):
        """
        Convert mmCIF file to Pandas DataFrame.
        """
        if self.active_biopython:
            structure = self.mmci_parser.get_structure('X', loc)
            
            data = []
            for model in structure:
                for chain in model:
                    for residue in chain:
                        for atom in residue:
                            data.append([model.id, chain.id, residue.id[1], residue.id[2], atom.id, atom.coord[0], atom.coord[1], atom.coord[2]])

            df = pd.DataFrame(data, columns=['model', 'chain', 'residue_number', 'insertion', 'atom_name', 'x', 'y', 'z'])

            return df