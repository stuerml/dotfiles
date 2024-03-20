"""
    _       _     __  _  _          
 __| | ___ | |_  / _|(_)| | ___  ___
/ _` |/ _ \|  _||  _|| || |/ -_)(_-/
\__/_|\___/ \__||_|  |_||_|\___|/__/

@author stuerml
@date 2024
"""

import typer

import os

from enum import Enum
from typing import Dict, List

from pathlib import Path

# from apt_pkg import Cache

from rich import print

''' packages '''
PACKAGES: List[str] = [
        "python3-pip", "python3-xcffib", "python3-cairocffi", "zsh", "kitty", "picom"
    ]

PIP_DEPENDENCIES: List[str] = ["qtile"]
'''end packages '''

PROFILE_PATH = "~/.local/share/profile"
class Profile(str, Enum):
    work = "work"
    home = "home"

''' utilities '''
def create_dir_if_not_exists(dest: Path):
    directory = Path("/").joinpath(Path("/".join(dest.parts[:-1])))
    if not directory.exists():
        print(f"Creating directory: {directory}")
        directory.mkdir(parents=True)
    
def validate_destination_path(dest_path: Path) -> Path:
    """
    Makes sure the path is a valid absolute system path.
    """
    components = dest_path.parts
    if components[0] == "home":
        '''Get the home directory of the current user '''
        return Path.home().joinpath(Path("/".join(components[1:])))

    if components[0] == "usr" or components[0] == "etc":
        '''Prefix with root '''
        return Path("/").joinpath(dest_path) 


def get_configuration_files() -> Dict[Path, Path]:
    """
    Returns a dictionary containing the local path of the configuration files
    as keys and the destination path in the system as values.
    """
    found_files: Dict[Path, Path] = {}

    for dirpath, dirs, files in os.walk(".files"):
        dest_path = Path(dirpath.removeprefix(".files/"))
        dest_path = validate_destination_path(dest_path)
        for filename in files:
            found_files[Path(dirpath).absolute().joinpath(filename)] = Path(os.path.join(dest_path, filename))

    return found_files
''' end utilities '''


dotfiles = typer.Typer()

def install_packages():
    print("Installing packages...")

def install_files():
    print("Installing files...")
    dotfiles = get_configuration_files()

    for src, dest in dotfiles.items():
        create_dir_if_not_exists(dest)
        try:
            # in case we run as root
            if dest.parts[1] == "root":
                print("Skipping dotfiles for root")
                continue

            if dest.exists():
                print(f"File {dest} exists on system! Replacing it.")
                dest.unlink()

            print(f"Creating symbolic link: {dest} -> {src}")
            dest.symlink_to(src)

        except Exception as e:
            print(f"Failed to create a symlink to {dest}")
            print("You may run the program again with the correct permissions")
            continue

def write_profile(profile: Profile):
    profile_path = os.path.expanduser(PROFILE_PATH)
    print(f"{profile_path}")
    with open(profile_path, 'w+') as f:
        f.write(profile)
        f.close()


@dotfiles.command()
def install(pkgs: bool = typer.Option(default=False, help="Installs packages for dotfiles."),
            files: bool = typer.Option(default=False, help="Installs configuration files."),
            profile: Profile = typer.Option(default=Profile.home, help="Creates a file containing the profile string")) -> None:
    if pkgs:
        install_packages()
    
    if files:
        install_files()

    # Always update the profile
    write_profile(profile)

if __name__ == "__main__":
    dotfiles()