#!/usr/bin/env python3
import os
import subprocess
import sys
import traceback


_VENV_DIR = ".venv"


def is_win():
    return sys.platform == "win32"


def check_py_version(major: int, minor: int) -> None:
    pyver = sys.version_info
    if pyver.major != major or pyver.minor < minor:
        print(
            f"Your Python version is {pyver.major}.{pyver.minor}. "
            f"Python {major}.{minor} is required!\n"
            "Aborting setup process!"
        )
        sys.exit()


def create_venv() -> None:
    if os.environ.get("VIRTUAL_ENV", "").strip():
        return
    subprocess.run([sys.executable, "-m", "venv", _VENV_DIR])


def perform_installations() -> None:
    print("\033[96mInstalling pip requirements...\033[0m\n")

    venv_pip = f"{_VENV_DIR}/bin/pip"
    if is_win():
        venv_pip = f"{_VENV_DIR}/Scripts/pip"

    subprocess.run([venv_pip, "install", "-r", "requirements-dev.txt"])
    subprocess.run([venv_pip, "install", "-r", "requirements.txt"])

    print("\033[96m\nInstalling precommit hook...\033[0m\n")

    venv_precommit = f"{_VENV_DIR}/bin/pre-commit"
    if is_win():
        venv_precommit = f"{_VENV_DIR}/Scripts/pre-commit"

    subprocess.run([venv_precommit, "install"])


def main():
    try:
        check_py_version(3, 7)
        create_venv()
        perform_installations()
    except:
        traceback.print_exc()
        print(
            "\033[91m\nFailed to automatically setup virtual environment.\n"
            "Please check the setup doc for a manual process instead!\n\033[0m"
        )
        return

    activate_command = f"\033[93msource {_VENV_DIR}/bin/activate\033[92m"
    if is_win():
        activate_command = (
            f"\033[93m.\\{_VENV_DIR}\\Scripts\\Activate.ps1\033[92m "
            "if you are using powershell, "
            f"or \033[93m.\\{_VENV_DIR}\\Scripts\\activate.bat\033[92m "
            "if you are using CMD"
        )

    print(
        "\033[92m"
        + "\nYour development environemnt is successfully created!\n"
        + "Please run "
        + activate_command
        + "\033[92m to enter your virtual environemnt and start developing!\n\033[0m"
    )


if __name__ == "__main__":
    main()
