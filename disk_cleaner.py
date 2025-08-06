import os
from pathlib import Path
import openai
from typing import List, Tuple

from gpt_helper import ask_gpt_about_file, GPT_ENABLED

TOP_HEAVISET_DIRS = 15


def get_size(path: str) -> int:
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
                except Exception as e:
                    continue
    except Exception as e:
        pass
    return total_size

def scan_folders(root_path: str, limit=TOP_HEAVISET_DIRS) -> List[Tuple[str, int]]:
    folder_sizes = []
    root = Path(root_path)
    for p in root.iterdir():
        if p.is_dir():
            print(f"Scanning {p}...")
            size = get_size(str(p))
            folder_sizes.append((str(p), size))

    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    return folder_sizes[:limit]


def main():
    path = input("Укажи путь к папке для анализа (например, C:/ или /home/user): ").strip()
    results = scan_folders(path)

    print("\n[TOP ДИРЕКТОРИЙ ПО РАЗМЕРУ]")
    for folder, size in results:
        size_gb = round(size / (1024**3), 2)
        print(f"{folder}: {size_gb} GB")

        if GPT_ENABLED:
            response = ask_gpt_about_file(folder, size)
            print(f"[GPT]: {response}\n")

if __name__ == "__main__":
    main()