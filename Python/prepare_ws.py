"""
CAUTION!! READ BEFORE USING!!

1. Requirements:

1.1 Ubuntu packages:
- p7zip-full

1.2 PIP libs:
- patool
- pyunpack
- tqdm

2. Execution Path (file structure):
- /home/.../ITS/ (root must be ITS folder)
  * HW1/
  * HW2/
  * prepare_ws.py

3. Usage:
- python prepare_ws.py HW3 archive.zip -r
  * first arg (subfolder): new folder for the submissions
  * second arg (file): the archive zip file downloaded from course management page
  * -r --remove flag: remove archive files after extracting
"""
import argparse
from pathlib import Path, PosixPath
import os
from typing import Union, Final
from tqdm import tqdm
from pyunpack import Archive


def remove_file(f: Union[Path, PosixPath]) -> None:
    f.unlink()
    return


def extract_archive(p_in: Union[Path, PosixPath], f_out: PosixPath, remove: bool = True) -> None:
    Archive(p_in.as_posix()).extractall(f_out.as_posix())

    if remove:
        remove_file(p_in)
    return


if Path('.').absolute().name != "ITS":
    print("Please move to the root 'ITS' folder to run this script!")
    exit(0)
else:
    print("Start preparing working directory...")

# arg parser
parser = argparse.ArgumentParser()
parser.add_argument("subfolder", help="sub-folder to create for the assignments.")
parser.add_argument("file", help="Archive file to extract.")
parser.add_argument("-r", "--remove", help="Remove archive files after reorganizing the assignments.",
                    action="store_true")
args = parser.parse_args()
REMOVE_ARCHIVE: Final = True if args.remove else False

# create ws folder
ws = args.subfolder
p_ws = Path(ws).absolute()

if p_ws.exists():
    print("Target folder already exists! Please provide another folder name!")
    exit(0)
else:
    p_ws.mkdir()
    print("Target folder created at: {}".format(p_ws.as_posix()))

# unzip the zip file
file = args.file
p_file = Path(file).absolute()
print("Unzipping target file: {}".format(file))
extract_archive(p_file, p_ws, remove=REMOVE_ARCHIVE)
print("Extraction completed. Archive removed...")

# change dir
print("Changing to ws dir: {}".format(ws))
os.chdir(p_ws)

# organizing files
print("Reorganizing all files...")
stu_codes = set([p.name.split('_')[0] for p in p_ws.glob('*')])  # get unique students codes
p_bar = tqdm(stu_codes)
p_single = p_ws.joinpath("single_files")
p_single.mkdir()  # single file without images will be put here
for code in p_bar:
    p_bar.set_description("Processing code: {}".format(code))

    # in case some students uploaded twice or more
    uploads = sorted(list(p_ws.glob(code + "*")))
    upload_latest = uploads.pop(-1)  # get the latest one

    # if it's a single python file or notebook
    if upload_latest.name.endswith(("ipynb", 'py')):
        upload_latest.rename(p_single.joinpath(upload_latest.name))  # move current file to students folder
    else:
        # create student specific folder
        stu_dir = p_ws.joinpath(code)
        stu_dir.mkdir()

        # if it's an archive
        if upload_latest.name.endswith(('zip', 'rar', 'tar', 'gz', '7z')):
            extract_archive(upload_latest, stu_dir, remove=REMOVE_ARCHIVE)

        else:
            print("Unexpected file type! {}".format(upload_latest.as_posix()))

    # remove remaining files (old submissions)
    for p in uploads:
        remove_file(p)

print("Working directory prepared! Enjoy!")
