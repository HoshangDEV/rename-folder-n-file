# File & Directory Renamer

A Python script designed to rename files and directories in Next.js projects by replacing specified text patterns. Perfect for refactoring projects when you need to rename components, routes, or features across multiple files and directories.

## Features

- 🔍 **Smart Search**: Recursively searches through specified directories
- 📁 **Handles Complex Paths**: Works with Next.js App Router conventions including route groups `(folder)`, dynamic routes `[id]`, and catch-all routes `[...params]`
- 🎯 **Dual Mode**: Interactive prompts or command-line arguments
- 📋 **Preview Mode**: Shows what will be renamed before making changes
- 🔄 **Case Handling**: Automatically handles both lowercase and capitalized versions
- ✅ **Verification**: Confirms operation success and reports any missed items
- 🛡️ **Safe Operations**: Asks for confirmation and handles errors gracefully

## Installation

No installation required! Just ensure you have Python 3.6+ installed on your system.

## Usage

### Interactive Mode (Recommended)

Simply run the script and follow the prompts:

```bash
python rename.py
```

You'll be prompted to enter:

- **Text to replace** (e.g., `discussion`)
- **Replacement text** (e.g., `forum`)
- **Directories to search** (default: `app components`)

### Command Line Mode

For automation or scripting:

```bash
# Basic usage
python rename.py --from discussion --to forum

# Specify custom directories
python rename.py --from discussion --to forum --dirs app components lib

# Multiple directories
python rename.py --from user --to member --dirs app components pages utils
```

## Examples

### Example 1: Renaming Discussion to Forum

```bash
python rename.py --from discussion --to forum
```

This will rename:

- `app/(public)/discussions/` → `app/(public)/forum/`
- `discussion-page.tsx` → `forum-page.tsx`
- `DiscussionComponent.jsx` → `ForumComponent.jsx`
- `useDiscussion.js` → `useForum.js`

### Example 2: Interactive Mode

```
=== File/Directory Renamer ===
Enter text to replace (e.g., 'discussion'): user
Enter replacement text (e.g., 'forum'): member
Enter directories to search (default: app components): app lib

Renaming 'user' to 'member'
Searching in directories: app, lib
Root directory: /your/project
============================================================

Found 3 items containing 'user':
  Directory: /your/project/app/(dashboard)/user
  File: /your/project/app/components/UserProfile.tsx
  File: /your/project/lib/userUtils.js

============================================================
Do you want to proceed with renaming? (y/n): y
```

## Command Line Options

| Option   | Description                                   | Required | Default          |
| -------- | --------------------------------------------- | -------- | ---------------- |
| `--from` | Text to search for and replace                | Yes      | -                |
| `--to`   | Replacement text                              | Yes      | -                |
| `--dirs` | Space-separated list of directories to search | No       | `app components` |

## How It Works

1. **Scanning**: The script uses `os.walk()` to recursively traverse the specified directories
2. **Detection**: Finds all files and directories containing the target text (case-insensitive search)
3. **Sorting**: Orders items by depth (deepest first) to avoid conflicts when renaming parent directories
4. **Preview**: Shows exactly what will be renamed before making changes
5. **Execution**: Renames items using `os.rename()` for maximum compatibility
6. **Verification**: Checks for any remaining items that weren't renamed

## Safety Features

- **Preview before action**: Always shows what will be renamed
- **Confirmation prompt**: Requires explicit user confirmation
- **Existence checking**: Verifies items still exist before renaming (handles parent directory renames)
- **Conflict detection**: Warns if target names already exist
- **Error handling**: Gracefully handles permission errors and other issues
- **Verification**: Double-checks that the operation completed successfully

## Supported File Types

The script works with any file type and handles:

- React components (`.tsx`, `.jsx`, `.js`)
- TypeScript files (`.ts`, `.tsx`)
- Style files (`.css`, `.scss`, `.module.css`)
- Configuration files (`.json`, `.yaml`, `.env`)
- Documentation files (`.md`, `.txt`)
- Any other file types in your project

## Next.js Specific Features

Designed with Next.js projects in mind:

- **Route Groups**: `(auth)`, `(dashboard)`, `(public)`
- **Dynamic Routes**: `[id]`, `[slug]`, `[userId]`
- **Catch-all Routes**: `[...params]`, `[[...slug]]`
- **App Router**: Works with the new `app/` directory structure
- **Pages Router**: Also works with traditional `pages/` directory

## Troubleshooting

### Permission Errors

```bash
# Run with elevated permissions if needed (be careful!)
sudo python rename.py --from discussion --to forum
```

### Items Not Found

- Ensure you're running the script from your project root
- Check that the directories you specified actually exist
- Verify the text you're searching for exists in file/directory names

### Partial Renames

If some items weren't renamed:

- Check the error messages for specific issues
- Ensure target names don't already exist
- Verify you have write permissions in all directories

## Best Practices

1. **Backup First**: Always backup your project before running bulk rename operations
2. **Test in Development**: Run the script on a development branch first
3. **Review Changes**: Carefully review the preview before confirming
4. **Update Imports**: Remember to update import statements in your code after renaming
5. **Version Control**: Use git to track changes and easily revert if needed

## Example Output

```
Renaming 'discussion' to 'forum'
Searching in directories: app, components
Root directory: /Users/developer/my-project
============================================================
Scanning /app for 'discussion'...
Scanning /components for 'discussion'...

Found 4 items containing 'discussion':
  Directory: /Users/developer/my-project/app/(public)/discussions
  File: /Users/developer/my-project/app/(public)/discussions/page.tsx
  File: /Users/developer/my-project/components/DiscussionCard.tsx
  File: /Users/developer/my-project/components/discussion-utils.js

============================================================
Do you want to proceed with renaming? (y/n): y

Starting rename operation...
----------------------------------------
Renaming file: page.tsx -> page.tsx
  Full path: /Users/developer/my-project/app/(public)/discussions/page.tsx
Renaming file: DiscussionCard.tsx -> ForumCard.tsx
  Full path: /Users/developer/my-project/components/DiscussionCard.tsx
Renaming file: discussion-utils.js -> forum-utils.js
  Full path: /Users/developer/my-project/components/discussion-utils.js
Renaming directory: discussions -> forum
  Full path: /Users/developer/my-project/app/(public)/discussions
----------------------------------------
Operation completed! Successfully renamed 4 items.

Summary of successful changes:
  File: DiscussionCard.tsx -> ForumCard.tsx
  File: discussion-utils.js -> forum-utils.js
  Directory: discussions -> forum

Checking for any remaining 'discussion' items...
✓ No remaining 'discussion' items found!
```

## License

This script is provided as-is for educational and development purposes. Use at your own risk and always backup your projects before running bulk operations.

---

**Happy Refactoring! 🚀**
