from pathlib import Path
import shutil
import argparse
import sys
import json
import logging
import hashlib

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("organizer.log"),
        logging.StreamHandler() 
    ]
)

def parse():
    var = argparse.ArgumentParser()
    var.add_argument("folder",nargs="?",type=Path,default=Path("."),help="which folder to organize")
    var.add_argument("--dry-mode"      ,action="store_true"        ,help="Know what will happen before Organization")
    var.add_argument("--copy"          ,action="store_true"        ,help="copy file instead of moving them")
    var.add_argument("--undo"          ,action="store_true"        ,help="undo last operation")
    var.add_argument("--include-hidden",action="store_true"        ,help="also move hidden files")
    return var.parse_args()

def hashs(filep,chunk_size=8192):
    obj = hashlib.sha256()
    with open(filep,"rb") as file:
        while chunk := file.read(chunk_size):
            obj.update(chunk)
    return obj.hexdigest()

def make_undo():
    with open("undo.json","w") as UndoFile:
        data["last_call"] = 1 if var.copy else 0
        json.dump(data,UndoFile)
        
def undo():
    with open("undo.json","r") as UndoFile:
        File = json.load(UndoFile)
        last_call = File.pop("last_call")
    for undo,destination in File.items():
        undo = Path(undo)
        destination = Path(destination)
        if Path(destination).exists():
            if last_call:
                Path(destination).unlink(missing_ok=True)
            else:
                undo.parent.mkdir(parents=True,exist_ok=True)
                shutil.move(destination,undo)
    sys.exit()

def make_format(resolve=True):
    new_extensions = {}
    files = {}
    if sys.argv[0] != __file__:
        resolve = False
    for file in var.folder.rglob("*"):
        if resolve and file.resolve() == Path(__file__).resolve():
            resolve=False
            continue
        elif file.name in ignore:
            continue
        elif (file.name.startswith(".") and not var.include_hidden) or not file.is_file() or file.is_symlink():
            continue
        suffix = file.suffix.lower()
        if suffix in types:
            files[file]=types[suffix]
        else:
            logging.info(f"Unknown Extension Found: {suffix}")
            new = input("Which folder would you like to add this extensions(default:Others) : ")
            if new == "":
                new = "Others"
            new_extensions[suffix] = new
            files[file] = new
    if new_extensions:
        types.update(new_extensions)
        with open("extension.json","w") as extension:
            json.dump(types,extension,indent=5)
    return files

def duplication_handler(new_file,file):
    if not new_file.exists() :
        return new_file
    elif file.stat().st_size == new_file.stat().st_size:
        hash1 = hashs(file)
        hash2 = hashs(new_file)
        if hash1 is None:
            logging.error(f"Something Went Wrong while checking hash of {file}")
            return "e"
        elif hash2 is None:
            logging.error(f"Something Went Wrong while checking hash of {new_file}")
            return "e"
        elif hash1 == hash2:
            return ""
    return counter(new_file)


def counter(file,count=1):
    while True:
        Paths = file.with_name(f"{file.stem}({count}){file.suffix}")
        if not Paths.exists():
            return Paths
        count+=1
    
def move_files(files):
    for file,folder in files.items():
        destination = var.folder / folder
        destination.mkdir(exist_ok=True)
        destination = destination / file.name
        destination = duplication_handler(destination,file)
        if destination in ("","e"):
            continue
        if var.copy:
            shutil.copy2(file,destination)
            logging.info(f"Copied {file} -> {destination}")
        else:
            shutil.move(file,destination)
            logging.info(f"Moved {file} -> {destination}")
        data[str(file)] = str(destination)
    if not files:
        logging.info("No File Found")
    logging.info("Organization Completed")

def dry(files):
    for file,folder in files.items():
        destination = var.folder / folder / file.name
        if destination.exists():
            new_file = duplication_handler(destination,file)
            logging.info(f"File with Same Names Found")
            if new_file == "":
                logging.info(f"Both File are same Skipped")
            elif new_file == "e":
                continue
            else:
                logging.info(f"File move {file} -> {new_file}")
        elif var.copy:
            logging.info(f"Will copy {file} -> {destination}")
        else:
            logging.info(f"Will move {file} -> {destination}")
    if "y" != input("would you like to continue(y/n)").strip().lower():
        logging.info("Organization Stopped")
        sys.exit()
        
var = parse()
data = {}
ignore = {'undo.json','extension.json','organizer.log'}
try:
    if not var.folder.exists() or not var.folder.is_dir():
        logging.info("folder is either doesn't exist or is not a directory")
        logging.info("Organization Stopped")
        sys.exit()
    with open("extension.json","r") as file:
        types = json.load(file)
        ignore.update(types.values())
    if var.undo:undo()
    files = make_format()
    if var.dry_mode:
        dry(files)
    move_files(files)
    if data:
        make_undo()
except Exception as e:
    logging.error(e)
    sys.exit(1)
            

