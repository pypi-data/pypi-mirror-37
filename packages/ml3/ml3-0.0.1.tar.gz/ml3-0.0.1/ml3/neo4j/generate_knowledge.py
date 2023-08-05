"""
生成节点和关系

"""
import json
import os
import csv
import copy
from pybloom_live import ScalableBloomFilter
from tqdm import tqdm


def get_conf(config_file_path):
    with open(config_file_path, "r", encoding="utf-8") as f:
        conf = json.load(f)
    return conf


def make_node(config,item):
    node = copy.deepcopy(config)
    if "enabled" in node and node["enabled"] == 0:
        return None
    node.pop("enabled")
    node.pop("desc")
    for k,v in node.items():
        if k=="label": continue
        node[k] = item[node[k]]
        #node["idx"] = item[node["idx"]] = item["IDENTIFICATIONNUMBERENCRYPT"]
        #node["media"] = item[node["media"]] = item["CARDMEDIATYPE"]
    return node


def make_rela(config,item):
    rela = copy.deepcopy(config)
    if "enabled" in rela and rela["enabled"] == 0:
        return None
    rela.pop("enabled")
    rela.pop("desc")
    for k,v in rela.items():
        if k == "rel": continue
        if k == "from_to": continue
        rela[k] = item[rela[k]]
        #node["idx"] = item[node["idx"]] = item["IDENTIFICATIONNUMBERENCRYPT"]
        #node["media"] = item[node["media"]] = item["CARDMEDIATYPE"]
    return rela


def gen_nodes_file(config,import_file,dump_dir):
    # 创建一个capacity等于100万，error rate等于0.001的bloomfilter对象
    sbf = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    #所有节点写入nodes_dict
    nodes_dict ={}
    nodes_config = config["nodes"]
    nodes_ignore_field = ['label', 'idx', 'enabled', 'desc']

    for node_config in nodes_config:
        node_label = node_config["label"]
        if node_label not in nodes_dict:
            nodes_dict[node_label] = []
        node_csv_header = ["idx:ID("+node_label+")",":LABEL","name","ctime","utime"]
        for node_attr in node_config.keys():
            if node_attr not in ["idx","label","name","ctime","utime"] and node_attr not in nodes_ignore_field:
                node_csv_header.append(node_attr)
        nodes_dict[node_label].append(node_csv_header)


    with open(import_file, "r", encoding="utf-8") as f:
        item_list = json.load(f)
        for item in tqdm(item_list):
            for node_config in nodes_config:
                node = make_node(node_config,item)
                if node == None:
                    continue
                else:
                    node_uniq_str = str(node["label"])+"/"+str(node["idx"])
                    if node_uniq_str not in sbf:
                        sbf.add(node_uniq_str)
                    else:
                        continue
                    node_csv_info = [node["idx"],node["label"],node["name"],node["ctime"],node["utime"]]
                    for node_attr in node.keys():
                        if node_attr not in ["idx","label","name","ctime","utime"] and node_attr not in nodes_ignore_field:
                            node_csv_info.append(node[node_attr])
                    nodes_dict[node_label].append(node_csv_info)
    for k,nodes in nodes_dict.items():
        write_node(k+".csv",nodes,dump_dir)           
 
 
def gen_relas_file(config,import_file,dump_dir):
    # 创建一个capacity等于100万，error rate等于0.001的bloomfilter对象
    sbf = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
 
    #所有节点写入nodes_dict
    relas_dict ={}
    relas_config = config["relations"]
    rela_ignore_field = ['label', 'idx', 'enabled', 'desc']

    for rela_config in relas_config:
        rela_fromto=rela_config["from_to"]
        if rela_fromto not in relas_dict:
            relas_dict[rela_fromto] = []
        label_from = rela_fromto.split("_2_")[0]
        label_to   = rela_fromto.split("_2_")[1]
        rela_csv_header = [":START_ID("+label_from+")",":END_ID("+label_to+")","rel:TYPE","ctime","utime"]
        relas_dict[rela_fromto].append(rela_csv_header)

    with open(import_file, "r", encoding="utf-8") as f:
        item_list = json.load(f)
        for item in tqdm(item_list):
            for rela_config in relas_config:
                rela = make_rela(rela_config,item)
                if rela == None:
                    continue

                rela_fromto = rela["from_to"]
                label_from = rela_fromto.split("_2_")[0]
                label_to   = rela_fromto.split("_2_")[1]
                rela_uniq_str = label_from+"/"+str(rela["startid"])+"-"+label_to+"/"+str(rela["endid"])
                if rela_uniq_str not in sbf:
                    sbf.add(rela_uniq_str)
                else:
                    continue

                rela_csv_info = [rela["startid"],rela["endid"],rela["rel"],rela["ctime"],rela["utime"]]
                relas_dict[rela_fromto].append(rela_csv_info)
    for k,relas in relas_dict.items():
        write_node(k+".csv",relas,dump_dir)           
       

def write_node(file_name, file_list, dump_dir = r"data"):
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    file_path = os.path.join(dump_dir, file_name)

    with open(file_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file_list)

def generate_knowmap_files(config_file_path, import_file_path, dump_dir="data_dump"):
    gen_nodes_file(get_conf(config_file_path), import_file_path, dump_dir)
    gen_relas_file(get_conf(config_file_path), import_file_path, dump_dir)


# generate_knowmap_files("config.json","import.mini.json","data_dump2")


