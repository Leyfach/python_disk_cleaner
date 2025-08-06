import os
from pathlib import Path
from typing import List, Tuple

from gpt_helper import ask_gpt_about_file, GPT_ENABLED

TOP_HEAVIEST_ITEMS = 15

TEXTS = {
    "enter_path": "Enter a folder path to analyze (e.g., C:/ or /home/user): ",
    "top_list": "\n[TOP ITEMS BY SIZE]",
    "choose_next": "\nEnter a number to drill into that folder or press Enter to exit: ",
    "scanning": "Scanning",
}


def get_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except:
        return 0

def scan_items(path: str, limit=TOP_HEAVIEST_ITEMS) -> List[Tuple[str, int]]:
    sizes = []
    p = Path(path)
    try:
        for item in p.iterdir():
            try:
                if item.is_dir():
                    print(f"{TEXTS['scanning']} {item}...")
                    size = sum(get_size(os.path.join(dirpath, f))
                               for dirpath, _, files in os.walk(item)
                               for f in files)
                else:
                    size = item.stat().st_size
                sizes.append((str(item), size))
            except Exception:
                continue
    except Exception:
        pass
    sizes.sort(key=lambda x: x[1], reverse=True)
    return sizes[:limit]


def interactive_scan():
    current_path = input(TEXTS["enter_path"]).strip()

    while True:
        results = scan_items(current_path)

        print(TEXTS["top_list"])
        for idx, (item, size) in enumerate(results):
            size_gb = round(size / (1024**3), 2)
            print(f"[{idx}] {item}: {size_gb} GB")

            if GPT_ENABLED:
                response = ask_gpt_about_file(item, size)
                print(f"[GPT]: {response}\n")

        choice = input(TEXTS["choose_next"]).strip()
        if not choice:
            break

        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(results):
                selected_path = results[idx][0]
                if Path(selected_path).is_dir():
                    current_path = selected_path
                else:
                    print("Not a directory. Exiting.")
                    break
            else:
                print("Invalid selection.")
        else:
            print("Invalid input.")


if __name__ == "__main__":
    interactive_scan()
