import argparse

def clear(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return [line.strip() for line in lines if line.strip()]

def save_lines(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def filter(file1_path, file2_path):
    file1 = clear(file1_path)
    file2 = set(clear(file2_path))

    unique_lines = [line for line in file1 if line not in file2]

    print(f"Original lines in {file1_path}: {len(file1)}")
    print(f"Lines removed: {len(file1) - len(unique_lines)}")
    print(f"Remaining lines: {len(unique_lines)}")

    save_lines(file1_path, unique_lines)

def deduplicate(file_path):
    lines = clear(file_path)
    unique_lines = list(dict.fromkeys(lines))  # preserves order

    print(f"Original lines in {file_path}: {len(lines)}")
    print(f"Duplicates removed: {len(lines) - len(unique_lines)}")
    print(f"Remaining unique lines: {len(unique_lines)}")

    save_lines(file_path, unique_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean song list files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare_parser = subparsers.add_parser("compare", help="Remove identical tracks from file1 if found in file2")
    compare_parser.add_argument("file1", help="File to clean (will be modified)")
    compare_parser.add_argument("file2", help="File to compare against")

    dedup_parser = subparsers.add_parser("dedup", help="Remove duplicate content from a single file")
    dedup_parser.add_argument("file", help="File to deduplicate (will be modified)")

    args = parser.parse_args()

    if args.command == "compare":
        filter(args.file1, args.file2)
    elif args.command == "dedup":
        deduplicate(args.file)
