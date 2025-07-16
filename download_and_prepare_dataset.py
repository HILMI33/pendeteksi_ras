import os
import urllib.request
import zipfile
import shutil

def download_utkface(destination_folder='dataset/UTKFace'):
    # Try multiple URLs to download dataset automatically
    urls = [
        'https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/UTKFace.zip',
        'https://data.deepai.org/UTKFace.zip'
    ]
    zip_path = 'UTKFace.zip'

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for url in urls:
        print(f'Trying to download UTKFace dataset from {url} ...')
        try:
            urllib.request.urlretrieve(url, zip_path)
            print('Download complete.')
            break
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
    else:
        print("Failed to download dataset from all sources.")
        print("Please download the dataset manually from one of the URLs:")
        for u in urls:
            print(u)
        return False

    print('Extracting dataset...')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    print('Extraction complete.')

    os.remove(zip_path)
    return True

def organize_utkface_dataset(source_folder='dataset/UTKFace', target_folder='dataset'):
    """
    Organize UTKFace dataset images into folders by ethnicity label.
    UTKFace filenames are in format: [age]_[gender]_[race]_[date&time].jpg
    race labels:
    0 = White
    1 = Black
    2 = Asian
    3 = Indian
    4 = Others
    We will map these to the classes: Asia, Afrika, Eropa, Amerika, Timur Tengah
    For simplicity:
    - 0 (White) -> Eropa
    - 1 (Black) -> Afrika
    - 2 (Asian) -> Asia
    - 3 (Indian) -> Timur Tengah
    - 4 (Others) -> Amerika
    """
    mapping = {
        '0': 'Eropa',
        '1': 'Afrika',
        '2': 'Asia',
        '3': 'Timur Tengah',
        '4': 'Amerika'
    }

    for key in mapping.values():
        dir_path = os.path.join(target_folder, key)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist. Please download the UTKFace dataset manually and place it in this folder.")
        return

    print('Organizing images into class folders...')
    for filename in os.listdir(source_folder):
        if filename.endswith('.jpg'):
            parts = filename.split('_')
            if len(parts) < 4:
                continue
            race = parts[2]
            class_name = mapping.get(race, 'Others')
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(target_folder, class_name, filename)
            shutil.move(src_path, dst_path)
    print('Organization complete.')

if __name__ == '__main__':
    success = download_utkface()
    if success:
        organize_utkface_dataset()
    else:
        print("Dataset download failed. Please download the dataset manually from one of the URLs:")
        print("https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/UTKFace.zip")
        print("https://data.deepai.org/UTKFace.zip")
        print("After downloading, extract the contents to the 'dataset/UTKFace' folder and then run this script again.")
