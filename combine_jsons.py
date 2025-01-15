import os
import json
import argparse

def main():

    parser = argparse.ArgumentParser(description="Combine JSONs into one JSON dictionary.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the directory containing nested directories containing the JSON files.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory. Default: 'combined_jsons' in the current working directory.", default="./combined_jsons",)

    args = parser.parse_args()

    input_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Failed to create directory: {e}")

    for i in sorted(os.listdir(input_dir)):
        d = os.path.join(input_dir, i)
        if os.path.isdir(d):
            new_dict = {
                'year': os.path.splitext(i)[0],
                'pages': []
            }
            dictionary_list = []
            for file in sorted(os.listdir(d)):
                if file != ".DS_Store":
                    f_path = os.path.join(d, file)
                    try:
                        with open(f_path, 'r', encoding="utf-8") as f:
                            data = json.load(f)
                            data.pop("year", None)
                            dictionary_list.append(data)
                    except FileNotFoundError:
                        print(f"File not found: {f_path}")
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding failed: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

            new_dict['pages'] = sorted(dictionary_list, key=lambda x: x['page'])
            try:
                with open(f'{output_dir}/{os.path.splitext(i)[0]}_combined.json', 'w', encoding='utf-8') as new_json:
                    json.dump(new_dict, new_json, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Failed to save JSON file: {e}")

if __name__ == "__main__":
    main()