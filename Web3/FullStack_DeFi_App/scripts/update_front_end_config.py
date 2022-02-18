import json
import os
import shutil
import yaml

def update_front_end_config():
    path = "./front_end/src/chain-config/"
    
    _copy_folders_to_front_end("./build", path + "chain-build")
    dump_config_to_json(path)

def dump_config_to_json(path="./"):
   with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open(f"{path}brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json) 
        
        chain_id_map = {}
        for network in config_dict["networks"]:
            if network == "default" or type(config_dict["networks"][network]) is type(""):
                continue
            
            if "chainId" in config_dict["networks"][network]:
                chain_id_map[config_dict["networks"][network]["chainId"]] = network
        with open(f"{path}chain_id_mapping.json", "w") as chain_id_mapping:
            json.dump(chain_id_map, chain_id_mapping) 
                
        
        
        

def _copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

def main():
    update_front_end_config()