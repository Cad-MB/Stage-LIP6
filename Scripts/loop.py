import requests
import json
url ="http://localhost:12081/api/json_schema/json/"
json2={
  "main_schema": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "age": { "type": "integer" }
    }
  },
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



x=requests.post(url,json=json2)



print(x.json()['dataset'])