def extract_tracks(input_file, output_file):
    extracted_tracks = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("Error processing line: "):
                track = line.replace("Error processing line: ", "").strip()
                if track:
                    extracted_tracks.append(track)

    with open(output_file, 'w', encoding='utf-8') as f:
        for track in extracted_tracks:
            f.write(track + '\n')

    print(f"Extracted {len(extracted_tracks)} tracks to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract track titles from error lines.")
    parser.add_argument("input_file", help="Path to the file containing error logs.")
    parser.add_argument("output_file", help="Path to the file where extracted tracks will be saved.")
    args = parser.parse_args()

    extract_tracks(args.input_file, args.output_file)
