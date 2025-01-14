import json
import os

directory = 'register'

for i in sorted(os.listdir(directory)):
    d = os.path.join(directory, i)
    if os.path.isdir(d):
        new_dict = {
            'year': os.path.splitext(i)[0],
            'pages': []
        }
        dictionary_list = []
        for file in sorted(os.listdir(d)):
            if file != ".DS_Store":
                f_path = os.path.join(d, file)
                with open(f_path, 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    data.pop("year", None)
                    dictionary_list.append(data)
        #print(dictionary_list)
        new_dict['pages'] = sorted(dictionary_list, key=lambda x: x['page'])
        with open(f'combined_registers/{os.path.splitext(i)[0]}_combined.json', 'w', encoding='utf-8') as new_json:
            json.dump(new_dict, new_json, indent=4, ensure_ascii=False)