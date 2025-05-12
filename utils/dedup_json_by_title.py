import json

def remove_titles_from_txt(json_file, txt_file, output_file=None):
    # Load JSON and extract titles
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    json_titles = {entry.get("title", "").strip() for entry in json_data}

    # Load TXT lines and filter
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt_lines = [line.strip() for line in f]

    filtered_lines = [line for line in txt_lines if line not in json_titles]

    # Save the filtered result
    output_path = output_file or txt_file
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in filtered_lines:
            if line:  # Skip blank lines
                f.write(line + '\n')

    print(f"Filtered TXT saved to: {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Remove lines from TXT file if titles exist in JSON.")
    parser.add_argument("json_file", help="Path to input JSON file.")
    parser.add_argument("txt_file", help="Path to TXT file with titles to clean.")
    parser.add_argument("--output", help="Optional path for output TXT file. Overwrites original if not provided.")
    args = parser.parse_args()

    remove_titles_from_txt(args.json_file, args.txt_file, args.output)
