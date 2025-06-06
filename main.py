import os
from pathlib import Path


def find_items_to_rename(root_dir, from_text, to_text, target_dirs=['app', 'components']):
    """
    Find all files and directories containing specified text
    """
    root_path = Path(root_dir)
    items_found = []

    for target_dir in target_dirs:
        dir_path = root_path / target_dir
        if not dir_path.exists():
            print(f"Directory '{target_dir}' not found, skipping...")
            continue

        print(f"Scanning /{target_dir} for '{from_text}'...")

        try:
            # Use os.walk to handle directory traversal more reliably
            for root, dirs, files in os.walk(dir_path):
                root_path_obj = Path(root)

                # Check directories first
                for dir_name in dirs:
                    if from_text.lower() in dir_name.lower():
                        dir_path_obj = root_path_obj / dir_name
                        items_found.append({
                            'path': dir_path_obj,
                            'type': 'directory',
                            'depth': len(dir_path_obj.parts)
                        })

                # Check files
                for file_name in files:
                    if from_text.lower() in file_name.lower():
                        file_path_obj = root_path_obj / file_name
                        items_found.append({
                            'path': file_path_obj,
                            'type': 'file',
                            'depth': len(file_path_obj.parts)
                        })
        except Exception as e:
            print(f"Error scanning {dir_path}: {e}")

    return items_found


def rename_items(items_found, from_text, to_text):
    """
    Rename items, starting with deepest directories first
    """
    # Sort by depth (deepest first) and type (files before directories at same level)
    items_found.sort(key=lambda x: (
        x['depth'], x['type'] == 'directory'), reverse=True)

    renamed_items = []

    for item in items_found:
        item_path = item['path']

        # Check if item still exists (parent directory might have been renamed)
        if not item_path.exists():
            print(
                f"Skipping {item_path} - no longer exists (likely parent was renamed)")
            continue

        # Create new name by replacing from_text with to_text (case-sensitive)
        old_name = item_path.name
        new_name = old_name.replace(from_text, to_text)

        # Also handle capitalized versions
        capitalized_from = from_text.capitalize()
        capitalized_to = to_text.capitalize()
        if capitalized_from != from_text:
            new_name = new_name.replace(capitalized_from, capitalized_to)

        new_path = item_path.parent / new_name

        # Check if target already exists
        if new_path.exists():
            print(f"Warning: {new_path} already exists, skipping {item_path}")
            continue

        try:
            print(f"Renaming {item['type']}: {old_name} -> {new_name}")
            print(f"  Full path: {item_path}")

            # Use os.rename for more reliable renaming
            os.rename(str(item_path), str(new_path))

            renamed_items.append({
                'old': str(item_path),
                'new': str(new_path),
                'type': item['type']
            })

        except PermissionError as e:
            print(f"Permission error renaming {item_path}: {e}")
        except FileExistsError as e:
            print(f"Target already exists for {item_path}: {e}")
        except Exception as e:
            print(f"Error renaming {item_path}: {e}")

    return renamed_items


def main():
    import sys

    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Use command line arguments
        import argparse

        parser = argparse.ArgumentParser(
            description='Rename files and directories in Next.js project')
        parser.add_argument('--from', dest='from_text',
                            required=True, help='Text to replace')
        parser.add_argument('--to', dest='to_text',
                            required=True, help='Replacement text')
        parser.add_argument('--dirs', nargs='+', default=['app', 'components'],
                            help='Target directories to search (default: app components)')

        args = parser.parse_args()
        from_text = args.from_text
        to_text = args.to_text
        target_dirs = args.dirs
    else:
        # Interactive mode
        print("=== File/Directory Renamer ===")
        from_text = input(
            "Enter text to replace (e.g., 'discussion'): ").strip()
        if not from_text:
            print("Error: 'from' text cannot be empty")
            return

        to_text = input("Enter replacement text (e.g., 'forum'): ").strip()
        if not to_text:
            print("Error: 'to' text cannot be empty")
            return

        dirs_input = input(
            "Enter directories to search (default: app components): ").strip()
        target_dirs = dirs_input.split() if dirs_input else [
            'app', 'components']

    current_dir = os.getcwd()

    print(f"Renaming '{from_text}' to '{to_text}'")
    print(f"Searching in directories: {', '.join(target_dirs)}")
    print(f"Root directory: {current_dir}")
    print("=" * 60)

    # First, find all items
    items_found = find_items_to_rename(
        current_dir, from_text, to_text, target_dirs)

    if not items_found:
        print(f"No files or directories containing '{from_text}' found.")
        return

    print(f"\nFound {len(items_found)} items containing '{from_text}':")
    for item in items_found:
        print(f"  {item['type'].capitalize()}: {item['path']}")

    print("\n" + "=" * 60)

    # Confirm before proceeding
    response = input("Do you want to proceed with renaming? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return

    print("\nStarting rename operation...")
    print("-" * 40)

    # Rename items
    renamed_items = rename_items(items_found, from_text, to_text)

    print("-" * 40)
    print(
        f"Operation completed! Successfully renamed {len(renamed_items)} items.")

    if renamed_items:
        print("\nSummary of successful changes:")
        for change in renamed_items:
            print(
                f"  {change['type'].capitalize()}: {Path(change['old']).name} -> {Path(change['new']).name}")

    # Check if any items were missed
    print(f"\nChecking for any remaining '{from_text}' items...")
    remaining_items = find_items_to_rename(
        current_dir, from_text, to_text, target_dirs)
    if remaining_items:
        print(
            f"Warning: {len(remaining_items)} items still contain '{from_text}':")
        for item in remaining_items:
            print(f"  {item['type'].capitalize()}: {item['path']}")
    else:
        print(f"✓ No remaining '{from_text}' items found!")


if __name__ == "__main__":
    main()
