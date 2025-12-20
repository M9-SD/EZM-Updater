import re
import shutil
from pathlib import Path
import os
import ctypes
from ctypes import wintypes
from windows_toasts import (
    AudioSource,
    Toast,
    ToastAudio,
    WindowsToaster,
    ToastDisplayImage,
)

# playsound3  playsound
import requests
import tempfile
#frm time imprt sleep

# sys
# winsound

ezm_version = "None"  # Example version


def get_windows_temp_dir():
    """
    Returns the path to the Windows temporary directory.
    """
    temp_dir = tempfile.gettempdir()

    # Optional: Ensure the path exists
    if not os.path.exists(temp_dir):
        raise FileNotFoundError(f"Temporary directory not found: {temp_dir}")

    return temp_dir


def update_name(file_path, new_name):
    """
    Updates the name field in header.sqe.
    """
    # Read the file
    # with open(file_path, "r") as file:
    #    lines = file.readlines()

    headertext = """
version=54;
name="";
author="Updater";
category="Enhanced Zeus Modules";
requiredAddons[]=
{
    "A3_Structures_F_Mil_Helipads"
};
    """
    lines = headertext.splitlines(keepends=True)

    # Update the name field
    for i, line in enumerate(lines):
        if line.strip().startswith("name="):
            # Replace the line with the new name, keeping the semicolon
            lines[i] = f'name="{new_name}";\n'
            break

    # Write the file back
    with open(file_path, "w") as file:
        file.writelines(lines)
    print(f"Updated name to '{new_name}' in {file_path}")


def clear_downloads_folder(download_dir: str):
    """
    Deletes all contents of the download directory.
    Creates the directory if it does not exist.
    """
    print("Clearing download folder...")
    if os.path.exists(download_dir):
        for item in os.listdir(download_dir):
            item_path = os.path.join(download_dir, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                print(f"Unlinking {item_path}...")
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                print(f"Deleting {item_path}...")
                shutil.rmtree(item_path)
    else:
        os.makedirs(download_dir, exist_ok=True)


def download_latest_github_release(
    owner: str, repo: str, download_dir: str = "downloads", filename: str | None = None
):
    """
    Fetches and downloads assets from the latest release of a GitHub repository.

    Args:
        owner (str): GitHub owner/organization name.
        repo (str): Repository name.
        download_dir (str): Local directory to save downloaded files.
        filename (str | None): Specific asset filename to download.
                                If None, downloads all assets.

    Returns:
        List[str]: Paths to the downloaded files.
    """

    os.makedirs(download_dir, exist_ok=True)

    # Clear downloads folder first
    # clear_downloads_folder(download_dir)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api_url, headers={"Accept": "application/vnd.github+json"})
    response.raise_for_status()

    release_info = response.json()

    global ezm_version
    ezm_version = release_info.get("tag_name", "None")
    ezm_version = f"EZM {ezm_version}"

    assets = release_info.get("assets", [])

    if not assets:
        print("No assets found in the latest release.")
        return []

    downloaded_files = []

    for asset in assets:
        asset_name = asset["name"]

        # If a specific filename is requested, skip others
        if filename is not None and asset_name != filename:
            continue

        download_url = asset["browser_download_url"]
        print(f"Downloading {asset_name} from {download_url}...")

        asset_response = requests.get(download_url, stream=True)
        asset_response.raise_for_status()

        file_path = os.path.join(download_dir, asset_name)
        with open(file_path, "wb") as f:
            for chunk in asset_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        downloaded_files.append(file_path)
        print(f"Saved: {file_path}")

    if filename and not downloaded_files:
        raise FileNotFoundError(f"Asset '{filename}' not found in the latest release.")

    return downloaded_files


def get_documents_folder():
    """
    Returns the real Windows Documents folder path,
    including OneDrive-redirection if enabled.
    """

    # Define the GUID for the Documents folder
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8),
        ]

    FOLDERID_Documents = GUID(
        0xFDD39AD0, 0x238F, 0x46AF, (0xAD, 0xB4, 0x6C, 0x85, 0x48, 0x03, 0x69, 0xC7)
    )

    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID),
        wintypes.DWORD,
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p),
    ]
    SHGetKnownFolderPath.restype = wintypes.HRESULT

    path_ptr = ctypes.c_wchar_p()
    result = SHGetKnownFolderPath(
        ctypes.byref(FOLDERID_Documents), 0, None, ctypes.byref(path_ptr)
    )

    if result != 0:
        raise ctypes.WinError(result)

    path = Path(path_ptr.value)
    ctypes.windll.ole32.CoTaskMemFree(path_ptr)  # free memory
    return path


def sqf_to_init_string(path):
    with open(path, "r", encoding="utf-8") as f:
        sqf_code = f.read()

    # Normalize line endings
    sqf_code = sqf_code.replace("\r\n", "\n").replace("\r", "\n")

    # Remove newlines and tabs (flatten to one line)
    sqf_code = sqf_code.replace("\n", " ").replace("\t", " ")

    # Collapse multiple spaces into one
    sqf_code = re.sub(r"\s+", " ", sqf_code).strip()

    # Escape double quotes for SQF strings
    escaped = sqf_code.replace('"', '""')

    # Wrap in quotes (single-line)
    return f'"{escaped}"'


def write_init_string(input_sqf_path, output_txt_path):
    if not input_sqf_path.lower().endswith(".sqf"):
        raise ValueError("Input file does not look like an SQF file")

    init_string = sqf_to_init_string(input_sqf_path)

    with open(output_txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(init_string)


def insert_init_into_sqe(
    sqf_path, sqe_input_path, sqe_output_path, sqe_output_path_headerFile
):
    init_string = sqf_to_init_string(sqf_path)

    # with open(sqe_input_path, "r", encoding="utf-8") as f:
    #    sqe_text = f.read()

    sqe_text = """
version=54;
center[]={7777,7777,7777};
class items
{
	items=1;
	class Item0
	{
		dataType="Object";
		side="Empty";
		class Attributes
		{
			init="";
		};
		id=0;
		type="Land_HelipadEmpty_F";
	};
};
    """

    pattern = re.compile(r'init\s*=\s*"(?:[^"]|"")*"\s*;', re.DOTALL)

    if not pattern.search(sqe_text):
        raise ValueError('No init="..."; field found in SQE file')

    new_sqe = pattern.sub(lambda _: f"init={init_string};", sqe_text, count=1)

    with open(sqe_output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_sqe)

    update_name(sqe_output_path_headerFile, ezm_version)


def copy_composition_to_all_profiles(composition_folder_path):
    composition_folder_path = Path(composition_folder_path)

    if not composition_folder_path.is_dir():
        raise ValueError("composition_folder_path must be a directory")

    composition_name = composition_folder_path.name

    documents_dir = get_documents_folder()

    arma3_default = documents_dir / "Arma 3"
    arma3_other = documents_dir / "Arma 3 - Other Profiles"

    target_dirs = []

    if arma3_default.exists():
        target_dirs.append(arma3_default)

    if arma3_other.exists():
        for profile_dir in arma3_other.iterdir():
            if profile_dir.is_dir():
                target_dirs.append(profile_dir)

    if not target_dirs:
        raise RuntimeError("No Arma 3 profile directories found")

    for profile_dir in target_dirs:
        compositions_dir = profile_dir / "compositions"
        compositions_dir.mkdir(parents=True, exist_ok=True)

        target_composition_dir = compositions_dir / composition_name

        if target_composition_dir.exists():
            shutil.rmtree(target_composition_dir)

        shutil.copytree(composition_folder_path, target_composition_dir)

        print(f"Copied composition to: {target_composition_dir}")


def main():

    if True:
        # Create app temp folder
        tmp_win = get_windows_temp_dir()
        if not os.path.exists(tmp_win):
            os.makedirs(tmp_win, exist_ok=True)
        tmp_folder_name = "EZM_Updater"
        tmp_folder_path = os.path.join(tmp_win, tmp_folder_name)
        os.makedirs(tmp_folder_path, exist_ok=True)
        download_folder_name = "ezm_downloads"
        download_dir = os.path.join(tmp_folder_path, download_folder_name)
        ezm_file_path = os.path.join(download_dir, "Enhanced_Zeus_Modules.sqf")

        download_latest_github_release(
            owner="expung3d",
            repo="Enhanced-Zeus-Modules",
            download_dir=download_dir,
            filename="Enhanced_Zeus_Modules.sqf",
        )

        if not os.path.exists(ezm_file_path):
            return

        # refernce_composition_folder_path = "EZM_Comp_Reference"
        comp_folder_name = "EZM_Comp"
        composition_folder_path = os.path.join(tmp_folder_path, comp_folder_name)
        if not os.path.exists(composition_folder_path):
            os.makedirs(composition_folder_path, exist_ok=True)

        # First, make new comp folder based off reference
        # shutil.rmtree(composition_folder_path, ignore_errors=True)
        # shutil.copytree(refernce_composition_folder_path, composition_folder_path)

        comp_sqe_path = os.path.join(composition_folder_path, "composition.sqe")
        header_sqe_path = os.path.join(composition_folder_path, "header.sqe")

        # Create blank files
        open(comp_sqe_path, "w").close()
        open(header_sqe_path, "w").close()

        # Example usage
        insert_init_into_sqe(
            sqf_path=ezm_file_path,
            sqe_input_path=f"",
            sqe_output_path=comp_sqe_path,
            sqe_output_path_headerFile=header_sqe_path,
        )

        copy_composition_to_all_profiles(composition_folder_path)

        print(f"Cleaning up temp folder...")
        shutil.rmtree(tmp_folder_path, ignore_errors=True)

    toaster = WindowsToaster("EZM Updater")
    newToast = Toast()
    newToast.text_fields = [
        f"✅ {ezm_version} installed!"
    ]
    #"Click to open Enhanced Zeus Modules GitHub.",
    #newToast.AddImage(ToastDisplayImage.fromPath("EZM_Updater_Icon.ico"))
    # ewToast.launch = "https://github.com/expung3d/Enhanced-Zeus-Modules"
    # script_dir = Path(__file__).parent  # directory of the current script
    newToast.audio = ToastAudio(AudioSource.Default, looping=False, silent=False)
    newToast.on_activated = lambda _: print("EAST WIND ACTIVATED!")
    toaster.show_toast(newToast)
    # play sound
    """
    wav_file = os.path.join(sys._MEIPASS, "a3.wav")

    print("Looking for WAV file at:", wav_file)
    print("Exists?", os.path.exists(wav_file))


    # Make sure the WAV file exists
    if os.path.exists(wav_file):
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)
    else:
        print("WAV file not found!")

    #input("Press Enter to exit...")
    """
    #sleep(10)  # wait for toast to be seen, or clicked


if __name__ == "__main__":
    main()
