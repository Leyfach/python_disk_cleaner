import os
from pathlib import Path
from typing import List, Tuple, Dict

from gpt_helper import ask_gpt_about_file, GPT_ENABLED

TOP_HEAVIEST_ITEMS = 15

TEXTS = {
    "enter_path": "Enter a folder path to analyze (e.g., C:/ or /home/user): ",
    "top_list": "\n[TOP ITEMS BY SIZE]",
    "choose_next": "\nEnter a number to drill into that folder, 'b' to go back, or press Enter to exit: ",
    "scanning": "Scanning",
    "empty_folder": "This folder is empty or inaccessible.",
}

scan_cache: Dict[str, List[Tuple[str, int]]] = {}

def get_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except:
        return 0

def scan_items(path: str, limit=TOP_HEAVIEST_ITEMS) -> List[Tuple[str, int]]:
    if path in scan_cache:
        return scan_cache[path]

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
    scan_cache[path] = sizes[:limit]
    return scan_cache[path]

def interactive_scan():
    history = []

    current_path = input(TEXTS["enter_path"]).strip()
    if not Path(current_path).exists():
        print("Invalid path. Exiting.")
        return

    while True:
        results = scan_items(current_path)

        if not results:
            print(f"\n{TEXTS['empty_folder']}")
            choice = input("Type a new path or 'b' to go back: ").strip()
            if choice.lower() == 'b' and history:
                current_path = history.pop()
                continue
            elif Path(choice).exists():
                history.append(current_path)
                current_path = choice
                continue
            else:
                print("Invalid input. Exiting.")
                break

        print(TEXTS["top_list"])
        for idx, (item, size) in enumerate(results):
            size_gb = round(size / (1024**3), 2)
            print(f"[{idx}] {item}: {size_gb} GB")

            if GPT_ENABLED:
                response = ask_gpt_about_file(item, size)
                print(f"[GPT]: {response}\n")

        choice = input(TEXTS["choose_next"]).strip().lower()
        if not choice or choice == 'q':
            break
        elif choice == 'b':
            if history:
                current_path = history.pop()
            else:
                print("No previous path to go back to.")
        elif choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(results):
                selected_path = results[idx][0]
                if Path(selected_path).is_dir():
                    history.append(current_path)
                    current_path = selected_path
                else:
                    print("Not a directory. Returning to menu.")
            else:
                print("Invalid selection.")
        else:
            print("Invalid input.")

if __name__ == "__main__":
    interactive_scan()
