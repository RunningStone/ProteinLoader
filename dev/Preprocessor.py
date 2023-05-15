import os
import pickle
import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist
import torch


from ProteinLoader.dev.BaseIO import Parser_wrapper
from ProteinLoader.dev.predefined_constant import IUPAC_CODES
from ProteinLoader import logger
from ProteinLoader.dev.preprocessor_param import Preprocessor_param

class pFiles:
    def __init__(self,params:Preprocessor_param):
        """
        Class for reading and writing protein files.
        """
        self.params = params
        # initialize parsers
        self.parser = Parser_wrapper()
        
        # initialize variables to save data
        self.df = None
        self.fasta_loc = None
        self.pdb_loc = None
        self.mmcif_loc = None
    
    #################################################################
    #                    public functions                          #
    #################################################################
    def read(self, file_path:str):
        """
        Read a file and return the data. The file type is determined by the file extension.
        """
        logger.info(f"Reading file: {file_path}")
        # get file extension
        _, ext = os.path.splitext(file_path)
        # use the appropriate function
        if ext.lower() == '.fasta':
            return self.parser.read_fasta(file_path)
        elif ext.lower() == '.pdb':
            return self.parser.read_pdb(file_path)
        elif ext.lower() == '.cif':
            return self.parser.read_mmcif(file_path)
        else:
            raise ValueError("Unsupported file type: " + ext)
        
    def save_data(self, data, file_path):
        """
        Save data to a file using pickle.
        """
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    def load_data(self, file_path):
        """
        Load data from a file using pickle.
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)   
 
    #################################################################
    #                    tool functions                          #
    #################################################################

    def clean_data(self,chain_id):
        df = get_single_chain(self.df,chain_id)

        if self.params.check_single_conformation:
            logger.info("Extracting single conformation")
            df = extract_single_conformation(df)

        if self.params.remove_residues:
            logger.info(f"Removing residues {self.params.remove_residues_list}")
            df = remove_residues(df,self.params.remove_residues_list)
        
        if self.remove_invalid_atom:
            logger.info(f"Removing invalid atoms and keep {self.params.valid_atoms}")
            df = remove_invalid_atom(df,self.params.valid_atoms)
        
        if self.remove_UNK:
            logger.info(f"Removing UNK")
            df = remove_UNK(df)

        self.df = df

    def dihedral_to_tensor(self,atoms=["N", "CA", "C"],chain=None):
        """
        Convert the data to a tensor.
        input:  atoms = atoms to extract (optional)
        output: (seq,dist, omega, theta, phi, coords)
        """
        coords_for_dihedral, coords, wt, valid_resn = get_coords_from_df(self.df)
        dist, omega, theta, phi = process_coords(coords_for_dihedral)

        return wt, torch.tensor(dist, dtype=torch.float), \
            torch.tensor(omega, dtype=torch.float), \
            torch.tensor(theta, dtype=torch.float), \
            torch.tensor(phi, dtype=torch.float), \
            coords

#################################################################
#                   utility functions                          #
#################################################################

def get_coords_from_df(df, atoms=["N", "CA", "C"], chain=None):
    """
    input:  df = dataframe from wrapper
            atoms = atoms to extract (optional)
    output: (,coords=(x,y,z),seq, xyz.keys, ), 
            coords 是一个(seq_len, 3)的矩阵
            sequence
            xyz.keys 
    """
    #df = df['ATOM']
    seq, xyz = [], []
    min_resn, max_resn = np.inf, -np.inf
    
    for _, row in df.iterrows():
        if row['chain_id'] == chain or chain is None:
            if row['atom_name'].strip() in atoms:
                resn = int(row['residue_number'])
                if resn < min_resn:
                    min_resn = resn
                if resn > max_resn:
                    max_resn = resn
                xyz.append(np.array([row['x_coord'], row['y_coord'], row['z_coord']]))
                seq.append(row['residue_name'])
                
    # 三个字母表达转为单个字母表达 -> 变成序列
    seq = [IUPAC_CODES.get(s.capitalize(), "X") for s in seq]
    
    # convert to numpy arrays, fill in missing values
    seq_, xyz_ = [], []
    for resn in range(min_resn, max_resn + 1):
        if resn in seq:
            seq_.append(seq[resn])
        else:
            seq_.append("X")
        if resn in xyz:
            xyz_.append(xyz[resn])
        else:
            for _ in atoms:
                xyz_.append(np.full(3, np.nan))
                
    
    coords = np.array(xyz_).reshape(-1, len(atoms), 3)
    wt = "".join(seq_)
    valid_resn = np.array(sorted(xyz.keys()))
    coords_for_dihedral = {  # encapsulate coords from list to dict
        # TODO: make this more general？
        # atoms = ["N", "CA", "C"] #是一定是N,CA,C吗？还是atoms变化了也可以？
        atoms[0]: coords[:, 0],  # (seq_len, 3) 
        atoms[1]: coords[:, 1],
        atoms[2]: coords[:, 2]
    }
    return coords_for_dihedral, coords, wt, valid_resn

def get_dihedrals(a, b, c, d):
    b0 = -1.0 * (b - a)
    b1 = c - b
    b2 = d - c

    b1 /= np.linalg.norm(b1, axis=-1)[:, None]

    v = b0 - np.sum(b0 * b1, axis=-1)[:, None] * b1
    w = b2 - np.sum(b2 * b1, axis=-1)[:, None] * b1

    x = np.sum(v * w, axis=-1)
    y = np.sum(np.cross(b1, v) * w, axis=-1)

    return np.arctan2(y, x)

def get_angles(a, b, c):
    v = a - b
    v /= np.linalg.norm(v, axis=-1)[:, None]

    w = c - b
    w /= np.linalg.norm(w, axis=-1)[:, None]

    x = np.sum(v * w, axis=1)

    return np.arccos(x)

def process_coords(coords,atoms=["N", "CA", "C"]):
    #TODO: atoms 可以选择吗？
    # 这里是只能处理三个原子N,CA,C吗还是可能有其他？
    N = np.array(coords['N'])
    Ca = np.array(coords['CA'])
    C = np.array(coords['C'])

    # recreate Cb given N,Ca,C
    nres = len(N)
    b = Ca - N
    c = C - Ca
    a = np.cross(b, c)
    Cb = -0.58273431 * a + 0.56802827 * b - 0.54067466 * c + Ca

    # Cb-Cb distance matrix
    # pdist 计算向量对之间的距离 -> 质保函上或下三角部分的矩阵值, squareform 将这个压缩矩阵还原成对称的距离矩阵
    dist = squareform(pdist(Cb))
    np.fill_diagonal(dist, np.nan)
    indices = [[i for i in range(nres) if i != j] for j in range(nres)]
    idx = np.array([[i, j] for i in range(len(indices))
                   for j in indices[i]]).T  # 用于存储每个原子对应的k个最近邻居的索引
    idx0 = idx[0]  # 自身节点idx
    idx1 = idx[1]  # 连接的邻居节点idx
    # matrix of Ca-Cb-Cb-Ca dihedrals
    omega = np.zeros((nres, nres)) + np.nan
    omega[idx0, idx1] = get_dihedrals(
        Ca[idx0], Cb[idx0], Cb[idx1], Ca[idx1])  # (seq_len *(seq_len - 1))

    # matrix of polar coord theta
    theta = np.zeros((nres, nres)) + np.nan
    theta[idx0, idx1] = get_dihedrals(N[idx0], Ca[idx0], Cb[idx0], Cb[idx1])

    # matrix of polar coord phi
    phi = np.zeros((nres, nres)) + np.nan
    phi[idx0, idx1] = get_angles(Ca[idx0], Cb[idx0], Cb[idx1])
    return dist, omega, theta, phi


def extract_single_conformation(df: pd.DataFrame):
    '''
    输入单链pdb，将所有多构象残基变为单构象
    :param pdb_path:
    :return: DataFrame with single conformation
    '''
    # Select the ATOM records
    #df = df['ATOM']
    
    # Identify residues with multiple conformations
    multi_conformation_residues = df[df['alt_loc'] != ' ']
    unique_residues = multi_conformation_residues['residue_number'].unique()

    for residue_number in unique_residues:
        # Select the first conformation for each residue
        residue = df[df['residue_number'] == residue_number]
        first_conformation = residue[residue['alt_loc'] == residue['alt_loc'].min()]
        
        # Update the DataFrame
        df = df[df['residue_number'] != residue_number]
        df = pd.concat([df, first_conformation])
    
    return df

def remove_residues(df:pd.DataFrame,res = ['ACE','NH2']):
    '''
    去除pdb文件中的ACE和NH2残基
    :param df:DataFrame
    :return: DataFrame without ACE and NH2 residues
    '''
    
    # Remove ACE and NH2 residues
    df = df[~df['residue_name'].isin(res)]
    
    return df

def remove_invalid_atom(df:pd.DataFrame,valid_atoms = ['C','N','O','S']):
    '''
    去除pdb文件中的无效原子
    :param df:
    :return: DataFrame without invalid atoms
    '''
    
    # Remove invalid atoms
    df = df[df['element_symbol'].isin(valid_atoms)]
    
    return df


def remove_UNK(df:pd.DataFrame):
    '''
    去除pdb文件中的未知氨基酸（UNK）
    :param df:
    :return: DataFrame without UNK residues
    '''
    
    # Remove UNK residues
    df = df[df['residue_name'] != 'UNK']
    
    return df

def get_single_chain(df,chain_id):
    
    #df = ppdb.df['ATOM']
    
    # Filter for specified chain
    df = df[df['chain_id'] == chain_id]
    
    return df

