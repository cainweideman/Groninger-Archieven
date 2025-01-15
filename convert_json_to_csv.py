import os
import csv
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to CSV.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to a single JSON.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file. Default: 'combined_json.csv' in the current working directory.", default="./combined_json.csv",)

    args = parser.parse_args()
    input_file = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output)
    output_dir = os.path.dirname(output_file)

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Failed to create directory: {e}")

    # Load the JSON data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Open the CSV file for writing
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the header row
            writer.writerow(["year", "page", "name", "jobTitle", "address"])
            
            # Loop through the pages and write rows
            for page in data.get("pages", []):
                page_number = page.get("page", "Unknown")
                year = data.get("year", "Unknown")
                for entry in page.get("register", []):
                    # Write a row if entry is valid
                    if isinstance(entry, dict):
                        writer.writerow([
                            year,
                            page_number,
                            entry.get("name", ""),
                            entry.get("jobTitle", ""),
                            entry.get("address", "")
                        ])
            print(f"CSV file has been created: {output_file}")
    except Exception as e:
        print(f"Failed to save CSV file: {e}")

if __name__ == "__main__":
    main()