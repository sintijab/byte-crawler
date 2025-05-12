import argparse

def clear(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return [line.strip() for line in lines if line.strip()]

def save(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def filter(file1_path, file2_path):
    file1 = clear(file1_path)
    file2 = set(clear(file2_path))

    unique = [line for line in file1 if line not in file2]

    print(f"Original count: {file1_path}: {len(file1)}")
    print(f"Removed: {len(file1) - len(unique)}")
    print(f"Remaining: {len(unique)}")

    save(file1_path, unique)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two files and remove identical lines from the first.")
    parser.add_argument("file1", help="Path to the file to clean (will be modified)")
    parser.add_argument("file2", help="Path to the file to compare against (read-only)")
    args = parser.parse_args()

    filter(args.file1, args.file2)
