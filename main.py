import os
import shutil
import subprocess
import urllib.request
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse

BASE_DIR = os.getcwd()
WAD_EXTRACT_PATH = "data\\wad-extract.exe"
WAD_MAKE_PATH = "data\\wad-make.exe"
TEMP_FOLDER_PREFIX = "temp"
CHAMPIONS_PATH = "Game\\DATA\\FINAL\\Champions"
MAPS_PATH = "Game\\DATA\\FINAL\\Maps\\Shipping"


def update_hashes():
    try:
        online_response = urllib.request.urlopen(
            'https://raw.githubusercontent.com/CommunityDragon/CDTB/master/cdragontoolbox/hashes.game.txt',
            timeout=30
        )
        online_size = int(online_response.info()['Content-Length'])

        offline_path = os.path.join(BASE_DIR, 'data', 'hashes.game.txt')
        if os.path.exists(offline_path):
            offline_size = int(os.path.getsize(offline_path))
            if online_size != offline_size:
                with open(offline_path, 'wb+') as offline_file:
                    offline_file.write(online_response.read())
        else:
            with open(offline_path, 'wb+') as offline_file:
                offline_file.write(online_response.read())
    except Exception as e:
        logging.error(f"Error updating hashes: {e}")


def extract_wad(in_path, out_path):
    try:
        subprocess.run([WAD_EXTRACT_PATH, in_path, out_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        logging.error(f"Error extracting WAD: {e}")


def rename_files(new_region, temp_folder):
    try:
        old_region = os.listdir(os.path.join(temp_folder, 'assets\\sounds\\wwise2016\\vo'))[0]
        old_path = os.path.join(temp_folder, 'assets\\sounds\\wwise2016\\vo', old_region)
        new_path = os.path.join(temp_folder, 'assets\\sounds\\wwise2016\\vo', new_region.lower())
        os.rename(old_path, new_path)
    except Exception as e:
        logging.error(f"Error renaming file: {os.listdir(os.path.join(temp_folder, 'assets\\sounds\\wwise2016\\vo'))} {e}")


def make_wad(name, output_dir, new_region, temp_folder):
    try:
        out_wad = os.path.join(BASE_DIR, output_dir,
                               f'{name}.{new_region[:-2].lower()}{new_region[-2:].upper()}.wad.client')
        input_path = os.path.join(BASE_DIR, temp_folder)
        subprocess.run([WAD_MAKE_PATH, input_path, out_wad], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        logging.error(f"Error creating WAD: {e}")


def process_file(file_path, output_folder, new_region, temp_folder):
    extract_wad(file_path, os.path.join(BASE_DIR, temp_folder))
    rename_files(new_region, temp_folder)
    make_wad(os.path.basename(file_path).split('.')[0], output_folder, new_region, temp_folder)
    clean_temp(temp_folder)


def clean_temp(temp_folder):
    try:
        shutil.rmtree(os.path.join(BASE_DIR, temp_folder))
        logging.info(f"Cleaned temporary directory: {temp_folder}")
    except Exception as e:
        logging.error(f"Error cleaning temporary directory: {e}")


def main():
    parser = argparse.ArgumentParser(description="Process League of Legends files.")
    parser.add_argument("league_dir", help="Path to the League of Legends directory.")
    parser.add_argument("output_folder", help="Path to the output folder - preferably cslol MOD folder.")
    parser.add_argument("target_region", help="Target region.")
    parser.add_argument("new_region", help="New region.")

    args = parser.parse_args()

    league_dir = args.league_dir
    output_folder = args.output_folder
    target_region = args.target_region
    new_region = args.new_region

    logging.basicConfig(level=logging.INFO)

    update_hashes()

    champ_folder = os.path.join(league_dir, CHAMPIONS_PATH)
    map_folder = os.path.join(league_dir, MAPS_PATH)

    with ProcessPoolExecutor() as executor:
        files_champs = [os.path.join(champ_folder, filename) for filename in os.listdir(champ_folder) if
                        filename.endswith(f".{target_region}.wad.client")]

        files_maps = [os.path.join(map_folder, filename) for filename in os.listdir(map_folder) if
                      filename.endswith(f".{target_region}.wad.client")]

        files_to_process = files_champs + files_maps
        files_to_process.remove(os.path.join(champ_folder, f"TFTChampion.{target_region}.wad.client"))

        temp_folders = [f"{TEMP_FOLDER_PREFIX}_{i}" for i in range(len(files_to_process))]

        # Process each file sequentially within the pool
        futures = [executor.submit(process_file, file_path, output_folder, new_region, temp_folder) for
                   file_path, temp_folder in zip(files_to_process, temp_folders)]

        # Wait for all tasks to complete
        for future in as_completed(futures):
            # Handle exceptions in the individual tasks, if any
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in task: {e}")

    logging.info("Concurrent processing completed.")


if __name__ == '__main__':
    main()
