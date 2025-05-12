import json

def filter_missing(json_file, txt_file, output_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        existing_titles = set(line.strip() for line in f if line.strip())

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    missing_tracks = [track for track in data if track.get("title") not in existing_titles]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(missing_tracks, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Saved {len(missing_tracks)} missing tracks to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Filter tracks with titles not in the text file.")
    parser.add_argument("json_file", help="Path to the JSON file with track objects.")
    parser.add_argument("txt_file", help="Path to the TXT file with titles (one per line).")
    parser.add_argument("output_file", help="Path to the output JSON file.")
    args = parser.parse_args()

    filter_missing_titles(args.json_file, args.txt_file, args.output_file)
