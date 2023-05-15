import attr

@attr.s
class PreprocessorParam:
    # download data from source
    dataset_root:str=None # specify the root directory to save the data

    
    # data clean steps
    #single_chain_id = None # a chain id to select a single chain

    check_single_conformation:bool = True # check whether the pdb file has single conformation
    remove_residues:bool = True # remove ACE and NH2 residues
    remove_residues_list = ['ACE','NH2'] # the list of residues to be removed

    remove_invalid_atom:bool = True # remove invalid atoms
    valid_atoms = ['C','N','O','S'] # the list of valid atoms

    remove_UNK:bool = True # remove UNK residues



