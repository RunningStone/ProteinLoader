import numpy as np
import pandas as pd
import time
import torch
import os
from tqdm import tqdm
import torch
from pdb_utils import parse_PDB, process_coords


def get_pdbs(pdb, atom=['N', 'CA', 'C'], chain=None):
    # parse pdb and get coordinates
    coords, wt, _ = parse_PDB(pdb, atom, chain)
    coords_for_dihedral = {  # encapsulate coords from list to dict
        'N': coords[:, 0],  # (seq_len, 3)
        'CA': coords[:, 1],
        'C': coords[:, 2]
    }
    # fill diagonal element with 'nan' value
    dist, omega, theta, phi = process_coords(coords_for_dihedral)

    return wt, torch.tensor(dist, dtype=torch.float), \
        torch.tensor(omega, dtype=torch.float), \
        torch.tensor(theta, dtype=torch.float), \
        torch.tensor(phi, dtype=torch.float), \
        coords


if __name__ == "__main__":
    import sys

    '''
    if the PDB file has many chains, use `./get_pdb_singleChain.py` to get PDB with single chain. 
    '''
    pdb_path = "1ABT_singleChain.pdb"

    batch = get_pdbs(pdb_path)
