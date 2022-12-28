# -*- coding: utf-8 -*-
"""
Script that tweaks the spawnrate of modded structures.
The script does that for all mods in a folder.
Improvements I can think of are: make clearer to the user what the inputs are.
Add logging.
Add parameter for datapack version.
Add datapack version based on mc version.
Optimizations I can think of are: don't extract everything.
Created on Wed Dec 28 13:24:39 2022

@author: abovearth
"""
from zipfile import ZipFile
import zipfile
from pathlib import Path
import shutil
import os
import json


def remove_all_files_and_folders_except(to_keep, parent_directory):
    """
    Function that removes all files and folders from a parent directory,
except for the file or folder to keep

    Parameters
    ----------
    to_keep : str
        name of the file or folder to keep.
    parent_directory : Path object
        folder that will be cleaned.
        folder where all the files that will be removed are situated

    Returns
    -------
    None.

    """
    to_keep_full_path = parent_directory.joinpath(to_keep)
    files_and_folders = Path(parent_directory).glob('*')
    for clean_up in files_and_folders:
        if clean_up != to_keep_full_path:
            try:
                shutil.rmtree(clean_up)
            except NotADirectoryError:
                os.remove(clean_up)


# %%configure tweaks
# change this to the modifier you want.
# To halve the spawnrate of structures (less structures) put 0.5.
# To double the spwanrate (more structures) put 2
SPAWNRATE_MODIFIER = 0.9

# %%find all files
# assign directory
# replace this with your mods folder the r add the front is important and should be kept
DIRECTORY = r'C:\Users\roela\Twitch\Minecraft\Instances\MineColonies Official\mods'

# iterate over files in
# that directory
files = Path(DIRECTORY).glob('*')
zipfiles = []
for file in files:
    if zipfile.is_zipfile(file):
        zipfiles.append(file)

# %% extract all mods
datapack_destination = Path("new_datapack")
for zip_file in zipfiles:
    # opening the zip file in READ mode
    with ZipFile(zip_file, 'r') as zip_contents:
        # printing all the contents of the zip file
        zip_contents.extractall(datapack_destination)

# %% clean up folder for datapack
remove_all_files_and_folders_except("data", datapack_destination)

# %% go deeper in data folder and keep only worldgen
data_folder = datapack_destination.joinpath("data")
mod_folders = data_folder.glob('*')
for folder in mod_folders:
    remove_all_files_and_folders_except(
        "worldgen", folder)
    # go deeper and keep only structure_set
    worldgen_folder = folder.joinpath("worldgen")
    remove_all_files_and_folders_except(
        "structure_set", worldgen_folder)
    # remove all empty mod_folders
    try:
        folder.rmdir()
    except OSError:
        # skip not empty folders
        pass

# %% for all json files left
json_files = data_folder.glob("*/worldgen/structure_set/*.json")
for json_file in json_files:
    with json_file.open("r") as edit_file:
        data = json.load(edit_file)

    # %% find all spacing and separation parameters
    try:
        old_spacing = data["placement"]["spacing"]
        new_spacing = (1/SPAWNRATE_MODIFIER)*old_spacing
        # check new spacing can't be bigger than 4096 according to the wiki
        # https://minecraft.fandom.com/wiki/Custom_world_generation/structure_set
        new_spacing = min(4096, new_spacing)

        data["placement"]["spacing"] = int(new_spacing)
        old_separation = data["placement"]["separation"]
        new_separation = (1/SPAWNRATE_MODIFIER)*old_separation
        # new separation can't be bigger than 4096 or the spacing
        new_separation = min(4096, new_separation, new_spacing)
        data["placement"]["separation"] = int(new_separation)

    except KeyError:
        # if we for some reason can't find the parameters, we skip the file
        pass
    with json_file.open("w") as edit_file:
        json.dump(data, edit_file, indent=4)
# %% add pack.mcmeta
mcmeta_data = {
    "pack": {
        "description": "Structures spawnrate has been tweaked to "
        + str(SPAWNRATE_MODIFIER) + " the orginal value.",
        "pack_format": 10
    }
}
mcmeta_filepath = datapack_destination.joinpath("pack.mcmeta")
with open(mcmeta_filepath, "w") as mcmeta_file:
    json.dump(mcmeta_data, mcmeta_file, indent=4)
