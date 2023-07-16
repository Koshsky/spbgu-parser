import json


with open('parsed_data/01.03.01 Математика.json', 'r') as f:
    s = json.load(f)
    print(s)