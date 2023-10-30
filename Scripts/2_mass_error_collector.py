from genericpath import isfile
import requests
import json
import os

os.environ['NO_PROXY'] = '127.0.0.1'

from os import listdir
from os.path import isfile, join

url ="http://localhost:12081/api/json_schema/json/"
json2 = {
    "other_schemas": [],
    "settings": {
        "datagen_language": "en",
        "recursion": { "lower": 0, "upper": 5 },
        "prob_if": 80,
        "prob_patternProperty": 50,
        "random_props": True,
        "extend_objectProperties": "extend",
        "prefixItems": "extend",
        "extend_schemaProperties": "extend",
        "extend_prefixItems":"extend"
    }
}

path = r"C:\Users\Surface\Documents\LIP6\Stage-LIP6\dataGenDataset\github\sat\github_sat_13"
files = [f for f in listdir(path)
          if isfile (
              join(path, f)
          ) ]

# Create the 'instance' directory if it doesn't exist
instance_dir = join(path, "instance")
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Create a list to store distinct x.text values
distinct_errors = {}

for f in files: 
    print(f)
    schema = open(join(path, f), encoding="utf-8")
    data = json.load(schema) 
    json2["main_schema"] = data
    try:
        x = requests.post(url, json=json2, timeout=5)
        instance = x.json()['dataset']
        instance_file_path = join(instance_dir, f"{f}_instance.json")
        with open(instance_file_path, "w") as instance_file:
            instance_file.write(instance)
    except requests.exceptions.Timeout:
        error_msg = f"Timeout occurred for {f}"
        print(error_msg)
        if error_msg not in distinct_errors:
            distinct_errors[error_msg] = [f]
        else:
            distinct_errors[error_msg]+=[f]
    except Exception as e:
        error_msg = x.text
        print(error_msg)
        # Check if the error_msg text is distinct and not already in the list
        if error_msg not in distinct_errors:
            distinct_errors[error_msg] = [f]
        else:
            distinct_errors[error_msg]+=[f]

json_errors = json.dumps(distinct_errors, indent = 4) 
print(json_errors)
with open(path+"\instance"+"\errors.json", 'w') as f:
    f.write(json_errors)