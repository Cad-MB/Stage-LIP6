from genericpath import isfile
from unittest import expectedFailure
import requests
import json
import os

from os import listdir
from os.path import isfile, join



url ="http://localhost:12081/api/json_schema/json/"
json2={

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

path = r"C:\Users\Surface\Documents\LIP6\Stage-LIP6\dataGenDataset\github\sat"
files = [f for f in listdir(path)
          if isfile (
              join(path, f)
          ) ]

# Create the 'instance' directory if it doesn't exist
instance_dir = join(path, "instance")
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

for f in files: 
    print(f)
    schema= open(join(path,f))
    data= json.load(schema) 
    json2["main_schema"] = data
    x=requests.post(url,json=json2)
    try:
      instance = x.json()['dataset']
      instance_file_path = join(instance_dir, f"{f}_instance.json")
      with open(instance_file_path, "w") as instance_file:
        instance_file.write(instance)
    except:
      instance = x.text
      print(instance)