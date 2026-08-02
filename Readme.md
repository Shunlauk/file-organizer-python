# 📂 Python File Organizer

A lightweight command-line file organizer built with Python that automatically sorts files into folders based on their extensions.

The project is built entirely with Python's standard library and demonstrates practical filesystem automation using `pathlib`, `shutil`, `argparse`, `hashlib`, `json`, and `logging`.

---

# ✨ Features

* Organize files based on their file extensions
* Custom extension-to-folder mapping (`extension.json`)
* Automatically prompts for unknown extensions and saves them
* Dry-run mode to preview operations before making changes
* Copy mode (copy files instead of moving them)
* Undo the last organization operation
* SHA-256 duplicate detection
* Automatic renaming when duplicate filenames exist
* Logging to both the terminal and `organizer.log`
* Hidden files are skipped by default
* Optional support for organizing hidden files (`--include-hidden`)
* Skips directories
* Skips symbolic links
* Skips organizer configuration files
* Cross-platform implementation using `pathlib`

---

# 📁 Project Structure

```text
python-file-organizer/
├── organizer.py
├── extension.json
├── organizer.log
├── undo.json
└── README.md
```

---

# 🚀 Usage

### Organize the current directory

```bash
python organizer.py
```

### Organize another folder

```bash
python organizer.py /path/to/folder
```

### Preview changes before organizing

```bash
python organizer.py --dry-mode
```

### Copy files instead of moving them

```bash
python organizer.py --copy
```

### Undo the last organization

```bash
python organizer.py --undo
```

### Preview copy operations

```bash
python organizer.py --copy --dry-mode
```

### Include hidden files

```bash
python organizer.py --include-hidden
```

---

# 📂 Extension Mapping

Extension mappings are stored in `extension.json`.

Example:

```json
{
    ".jpg": "Images",
    ".png": "Images",
    ".pdf": "Documents",
    ".mp3": "Music",
    ".mp4": "Videos"
}
```

If an unknown extension is encountered, the organizer asks which folder it should belong to and automatically updates `extension.json`.

---

# 🔄 Duplicate Handling

The organizer compares files using SHA-256 hashes.

* If the destination file does not exist, the file is moved or copied.
* If an identical file already exists, the operation is skipped.
* If a file with the same name but different content exists, the new file is automatically renamed.

Example:

```text
photo.jpg
photo(1).jpg
photo(2).jpg
```

---

# ↩️ Undo

Every successful organization stores its operations in `undo.json`.

* Move mode restores files to their original locations.
* Copy mode removes the copied files.
* Only the most recent operation can be undone.

---

# 📝 Logging

All operations are recorded in `organizer.log` and displayed in the terminal.

Example:

```text
2026-07-10 14:35:21 | INFO | Moved photo.jpg -> Images/photo.jpg
2026-07-10 14:35:22 | INFO | Copied report.pdf -> Documents/report.pdf
```

---

# ⚠️ Current Limitations

* Organization is non-recursive.
* Empty folders are not removed.
* Symbolic links are skipped.
* Undo supports only the last organization operation.

---

# 🛣️ Future Roadmap

## Smart Organization

* Organize by creation date
* Organize by modification date
* Organize by file size
* Rule-based organization
* Import/export extension mappings

## Automation

* Automatic folder monitoring
* Scheduled organization

## Command-Line Improvements

* Include/exclude extension filters
* Recursive organization
* Better undo history
* Summary statistics

## GUI

* Folder picker
* Drag-and-drop support
* Progress bar
* Dark mode

---

# 🛠️ Built With

* Python 3
* pathlib
* shutil
* argparse
* hashlib
* json
* logging

---

# 📄 License

This project is open source and available under the MIT License.

