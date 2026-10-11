import logging
import argparse
from pathlib import Path


# Map file extensions to their destination categories.
FILE_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".svg", ".webp", ".tiff", ".ico"
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".odt", ".xls", ".xlsx", ".ppt", ".pptx",
        ".csv", ".md"
    },
    "Videos": {
        ".mp4", ".mkv", ".mov", ".avi", ".wmv",
        ".flv", ".webm", ".mpeg", ".mpg"
    },
    "Music": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg",
        ".m4a", ".wma", ".mid", ".midi"
    },
    "Code": {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".html",
        ".css", ".java", ".c", ".cpp", ".h", ".cs",
        ".php", ".rb", ".go", ".rs", ".json", ".xml",
        ".sql", ".sh", ".bat"
    },
}


def get_category(file_path):
    """Return the category matching a file's extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def scan_directory(source_dir):
    """Return visible files directly inside the source directory."""
    source_path = Path(source_dir).expanduser().resolve()

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source directory does not exist: {source_path}"
        )

    if not source_path.is_dir():
        raise NotADirectoryError(
            f"Source path is not a directory: {source_path}"
        )

    files = []

    for item in source_path.iterdir():
        if item.is_file() and not item.name.startswith("."):
            files.append(item)

    return files


def setup_logging():
    """Configure logging to record organizer operations."""
    log_path = Path(__file__).parent / "organizer.log"

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True,
    )


def get_unique_destination(destination):
    """Return a destination path that does not overwrite an existing file."""
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"

        if not candidate.exists():
            return candidate

        counter += 1


import shutil


def organize_files(source_dir, dry_run=False):
    """Organize files into category folders, or preview in dry-run mode."""
    setup_logging()
    source_path = Path(source_dir).expanduser().resolve()
    files = scan_directory(source_path)

    moved_count = 0
    skipped_count = 0

    for file_path in files:
        category = get_category(file_path)
        destination_folder = source_path / category
        destination = get_unique_destination(
            destination_folder / file_path.name
        )

        if dry_run:
            print(f"[DRY RUN] {file_path.name} -> {destination}")
            logging.info(
                "DRY RUN: Would move %s to %s",
                file_path,
                destination,
            )
            skipped_count += 1
            continue

        try:
            destination_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(destination))
            logging.info("Moved %s to %s", file_path, destination)
            print(f"Moved: {file_path.name} -> {category}/{destination.name}")
            moved_count += 1
        except OSError as error:
            logging.error("Failed to move %s: %s", file_path, error)
            print(f"Error moving {file_path.name}: {error}")
            skipped_count += 1

    print("\n===== Organization Summary =====")
    print(f"Files scanned: {len(files)}")

    if dry_run:
        print(f"Files that would be moved: {skipped_count}")
        print("Dry-run mode: no files were moved.")
    else:
        print(f"Files moved: {moved_count}")
        print(f"Files skipped or failed: {skipped_count}")


def main():
    """Parse command-line arguments and run the organizer."""
    parser = argparse.ArgumentParser(
        description="Organize files into folders by file type."
    )
    parser.add_argument(
        "source",
        help="Path to the directory containing files to organize.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned file movements without moving files.",
    )

    args = parser.parse_args()

    try:
        organize_files(args.source, dry_run=args.dry_run)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
