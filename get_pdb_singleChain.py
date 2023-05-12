
def get_pdb_single_chain(pdb_path,chain_id,output_path):
    '''
    指定原始pdb文件的路径pdb_path和蛋白链的索引chain_id，获取该蛋白链的pdb，并保存到路径output_path
    :param pdb_path:
    :param chain_id:
    :param output_path: 处理后的pdb的保存路径，如 "./data/5XCO.pdb"
    :return:
    '''
    with open(pdb_path,'r+') as f:
        lines = f.readlines()
        f.close()
    # chain_id = pdbid_chain_table[pdbid]
    final_lines = []
    # (1)提取ATOM、HETATM、TER的行（只保留一个MODEL的行）
    for i, line in enumerate(lines):
        if (line[:4] == 'ATOM' and line[21] == chain_id) or (line[:3] == 'TER' and line[21] == chain_id) or (line[:6] == 'HETATM' and line[21] == chain_id):
            final_lines.append(line)
            if line[:3] == 'TER':
                break
    with open(output_path,'w+') as f_write:
        f_write.writelines(final_lines)
        f_write.close()
    # (2)检查处理后的pdb是否存在多构象的问题
    from pdb_extract_single_conformation import extract_single_conformation,detect_pdb_if_singleConformation
    flag, _ = detect_pdb_if_singleConformation(output_path)
    if flag:
        lines_single_conf = extract_single_conformation(output_path)
        with open(output_path,'w+',encoding='utf-8') as f2:
            f2.writelines(lines_single_conf)
            f2.close()
    # (3)检查末端氨基酸是否残缺，即是否缺失CA原子
    # if pdb_if_exists_broken_AA(output_path):
    #     remove_broken_AA(output_path,output_path)

    # (4)去除ACE,NH2和无效原子
    remove_ACE_and_NH2(output_path,output_path)
    remove_invalid_atom(output_path,output_path)
    remove_UNK(output_path,output_path)


def remove_ACE_and_NH2(pdb_path,output_path):
    '''
    去除pdb文件中的ACE和NH2残基
    :param pdb_path:
    :return:
    '''
    with open(pdb_path,'r+',encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    lines_tmp = []
    for i, line in enumerate(lines):
        if (not line[17:20] == 'ACE') and (not line[17:20] == 'NH2'):
            lines_tmp.append(line)

    # 重设行号
    lines_ = []
    for i, line in enumerate(lines_tmp):
        line_ls = list(line)
        for j in range(7,11):
            line_ls[j] = str(i+1).rjust(4)[j - 7]
        line_ = "".join(line_ls)
        lines_.append(line_)

    with open(output_path,'w+', encoding='utf-8') as f:
        f.writelines(lines_)
        f.close()

def remove_invalid_atom(pdb_path, output_path):
    with open(pdb_path,'r+') as f:
        lines = f.readlines()
        f.close()
    # 去除无效原子
    valid_atom_flag_in_line77 = ['C','N','O','S']
    lines_final = []
    for line in lines:
        if line[77] in valid_atom_flag_in_line77:
            lines_final.append(line)

    # 重设行号
    lines_ = []
    for i, line in enumerate(lines_final):
        line_ls = list(line)
        for j in range(7,11):
            line_ls[j] = str(i+1).rjust(4)[j - 7]
        line_ = "".join(line_ls)
        lines_.append(line_)

    with open(output_path,'w+',encoding='utf-8') as f1:
        f1.writelines(lines_)
        f1.close()

def remove_UNK(pdb_path, output_path):
    with open(pdb_path,'r+') as f:
        lines = f.readlines()
        f.close()
    # 去除UNK氨基酸
    lines_final = []
    for line in lines:
        if not line[17:20] == 'UNK':
            lines_final.append(line)

    # 重设行号
    lines_ = []
    for i, line in enumerate(lines_final):
        line_ls = list(line)
        for j in range(7,11):
            line_ls[j] = str(i+1).rjust(4)[j - 7]
        line_ = "".join(line_ls)
        lines_.append(line_)

    with open(output_path,'w+',encoding='utf-8') as f1:
        f1.writelines(lines_)
        f1.close()

if __name__ == '__main__':
    pdb_path = '../1ABT.pdb'
    chain_id = 'A'
    output_path = '../1ABT_singleChain.pdb'
    get_pdb_single_chain(pdb_path=pdb_path,chain_id=chain_id,output_path=output_path)