# File Organizer

A Python command-line utility that automatically organizes files into category-based folders according to their file extensions.

## Author
Sweta Koshta

## Features

- **Automatic Categorization:** Organizes files into Images, Documents, Videos, Music, Code, and Others.
- **Duplicate Filename Handling:** Adds a numeric suffix to prevent existing files from being overwritten.
- **Dry-Run Mode:** Previews planned file movements without modifying files.
- **Hidden File Filtering:** Skips hidden files and subdirectories.
- **Logging:** Records file movements and dry-run operations in `organizer.log`.
- **Command-Line Interface:** Accepts a source directory and optional arguments.

## Requirements

- Python 3.8 or later
- No external Python packages required; the project uses Python's standard library.

### Python Modules Used

| Module | Purpose |
|---|---|
| `pathlib` | Handles file and directory paths. |
| `shutil` | Moves files between directories. |
| `logging` | Records file operations and errors. |
| `argparse` | Processes command-line arguments. |
| `os` | Supports operating-system-related operations. |

## Usage

Open a terminal in the `file_organizer` project directory.

### 1. Organize files

Run the following command, replacing the path with your target directory:

```bash
python file_organizer.py "path/to/your/folder"
```

The program categorizes files into folders based on their extensions.

### 2. Preview file movements

To preview the planned changes without moving any files, use:

```bash
python file_organizer.py "path/to/your/folder" --dry-run
```

### 3. View the operation log

After running the organizer, check `organizer.log` in the project directory for recorded file movements and dry-run operations.

## File Categories

The organizer identifies a file's category using its extension.

| Category | Example Extensions |
|---|---|
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg` |
| Documents | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv` |
| Videos | `.mp4`, `.mkv`, `.mov`, `.avi` |
| Music | `.mp3`, `.wav`, `.aac`, `.flac` |
| Code | `.py`, `.js`, `.html`, `.css`, `.java` |
| Others | File extensions not listed in the categories above |

### Customize Categories

To add or remove supported extensions, edit the `FILE_CATEGORIES` dictionary in `file_organizer.py`.

Add the extension, in lowercase and including the dot, to the appropriate category's set. For example, to categorize `.zip` files as Documents, add `".zip"` to the Documents set.

Extensions not matched by any category are placed in `Others`.

## Notes and Limitations

- The organizer processes files directly inside the specified source directory; it does not recursively scan subdirectories.
- Hidden files are skipped.
- Existing files are preserved by adding a numeric suffix to duplicate filenames.
- Dry-run mode previews planned movements without changing file locations.
- The organizer requires permission to read the source directory and move its files.