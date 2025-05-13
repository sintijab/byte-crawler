import json
import argparse

def deduplicate_by_title(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    seen_titles = set()
    deduplicated = []

    for obj in data:
        title = obj.get("title")
        if title and title not in seen_titles:
            seen_titles.add(title)
            deduplicated.append(obj)

    output_path = output_file or input_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('[\n')
        for i, item in enumerate(deduplicated):
            json_line = json.dumps(item, separators=(',', ':'), ensure_ascii=False)
            comma = ',' if i < len(deduplicated) - 1 else ''
            f.write(json_line + comma + '\n')
        f.write(']')

    print(f"Deduplicated and saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate JSON objects by 'title'.")
    parser.add_argument("input_file", help="Path to input JSON file.")
    parser.add_argument("--output", help="Optional output file. If not provided, input file is overwritten.")
    args = parser.parse_args()

    deduplicate_by_title(args.input_file, args.output)
