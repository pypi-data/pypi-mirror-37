"""
导入数据的工具
"""


import os
import re


def get_nodes_relas(data_dir):
    """
    获得所有的节点和关系文件名
    :param data_dir: 节点和关系的csv存放的文件夹
    :return:
    """
    if not os.path.exists(data_dir):
        print (str(data_dir) + " 不是一个正确的路径")
        return False
    data_dir = os.path.abspath(data_dir)

    # 得到数据文件夹下的所有文件，忽略文件夹
    data_files = []
    files = os.listdir(data_dir)
    for file_one in files:
        if os.path.isfile(os.path.join(data_dir, file_one)):
            data_files.append(file_one)

    # 将数据文件分类
    nodes = []  # 存储结点文件
    relas = []   # 存储关系文件

    for file_one in data_files:
        if re.findall(r'(.*?)_2_(.*?)', file_one):
            relas.append(file_one)
        else:
            nodes.append(file_one)
    return nodes, relas


def gen_import_command(data_dir, out_path, ignore_missing_nodes = True, ignore_duplicate_nodes = True ):
    """
    生成导入命令，生成的命令放在文件中
    :param data_dir: 节点和关系的csv存放的文件夹
    :param out_path: 输出命令文件的路径
    :param ignore_missing_nodes: 导入关系时时候忽略丢失的节点，默认是True
    :param ignore_duplicate_nodes: 导入节点时是否忽略重复的节点，默认是True
    :return:写入成功返回写入的文件路径，失败返回None
    """

    parent_dir = os.path.join(out_path, "..")
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
        # print (str(out_path) + " 不是一个正确的文件路径，生成导入命令失败")
        # return False

    nodes, relas = get_nodes_relas(data_dir)

    command = "neo4j-admin import --id-type string"

    # 相对路径转换为绝对路径，这样生成的导入命令就可以在本地的任何一个目录下执行
    data_dir = os.path.abspath(data_dir)

    for node in nodes:
        command += " \\\n--nodes:" + str(node[:-4]) + " " + os.path.join(data_dir, node)

    for rela in relas:
        command += " \\\n--relationships:" + str(rela[:-4]) + " " + os.path.join(data_dir, rela)

    if ignore_missing_nodes:
        command += " \\\n--ignore-duplicate-nodes"
    if ignore_duplicate_nodes:
        command += " \\\n--ignore-duplicate-nodes"

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(command)
        print("nodes: " + str(len(nodes)))
        print("relationships: " + str(len(relas)))
        print ("The command is saved in: " + str(os.path.abspath(out_path)))
        return True
    except Exception as e:
        print (e)
        return False

