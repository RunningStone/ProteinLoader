
def pdb_single_conformation(pdb_path, chain_id ,conf_id):
    '''
    某些pdb文件中存在AGLN，BGLN这类多构象的残基，该函数用来提取单个构象的pdb，与extract_single_conformation函数的不同点是，该函数需要指定conf_id，而extract_single_conformation函数不需要
    :param pdb_path:
    :param chain_id:
    :param conf_id:
    :return:
    '''
    with open(pdb_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
    lines_final_ =[]
    lines_tmp = []
    # flag = {} # key:AA_num, value:0表示有普通构像残基，1表示没有普通构像残基
    for i,line in enumerate(lines):
        if (line[:4] == 'ATOM' and line[21] == chain_id) or (line[:3] == 'TER' and line[21] == chain_id) or (line[:6] == 'HETATM' and line[21] == chain_id) :
            if line[16] == ' ' or line[16] == conf_id:
                if line[16] == conf_id:
                    line_ls = list(line)
                    line_ls[16] = " "
                    line = "".join(line_ls)
                lines_tmp.append(line)
    # 重设行号
    for i, line in enumerate(lines_tmp):
        line_ls = list(line)
        for j in range(7,11):
            line_ls[j] = str(i+1).rjust(4)[j - 7]
        line_final_ = "".join(line_ls)
        lines_final_.append(line_final_)
    return lines_final_

def extract_single_conformation(pdb_path):
    '''
    输入单链pdb，将所有多构象残基变为单构象
    :param pdb_path:
    :return:
    '''
    with open(pdb_path , 'r+',encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    lines_final = []
    lines_final_ = []
    AA_num = -1 # 氨基酸的序号,str类型
    i = 0
    # for i , line in enumerate(lines):
    while i < len(lines):
        line = lines[i]
        if not line[16] == ' ': # 找到多构象的氨基酸，初始化AA_num
            AA_num = line[22:26]
            conf_id = line[16]
            for j in range(i, len(lines)):
                if lines[j][16] == conf_id or lines[j][16] == ' ':
                    line_ls = list(lines[j])
                    line_ls[16] = ' '
                    line_ = ''.join(line_ls)
                    lines_final.append(line_)
                if not lines[j][22:26] == AA_num or j == len(lines) - 1: # 跳出循环的条件：遇到新氨基酸
                    i = j
                    break
        else:
            lines_final.append(line)
            i+=1
    # 重设行号
    for i, line in enumerate(lines_final):
        line_ls = list(line)
        for j in range(7,11):
            line_ls[j] = str(i+1).rjust(4)[j - 7]
        line_final_ = "".join(line_ls)
        lines_final_.append(line_final_)
    return lines_final_


def detect_pdb_if_singleConformation(pdb_path):
    '''
    输入一个pdb，检查是否存在多构想的残基
    :param pdb_path:
    :return: (True or False, conf_id)
    '''
    conf_id = None # pdb中的第一个构象标识
    with open(pdb_path, 'r+',encoding='utf-8') as f:
        lines = f.readlines()
        f.close()

    for i, line in enumerate(lines):
        if not line[16] == ' ':
            conf_id = line[16]
            return True, conf_id
    return False,conf_id

