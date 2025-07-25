import gzip
import shutil
import os


source_folder = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\datasets\Task01_BrainTumour\labelsTr'
destination_folder = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\datasets\Task01_BrainTumour\lablesTr_unzipped'


os.makedirs(destination_folder, exist_ok=True)


file_list = os.listdir(source_folder)
print(f"Found {len(file_list)} files in the source folder.")

for filename in file_list:
    if filename.startswith('._'):
        print(f"⚡ Skipping hidden file: {filename}")
        continue

    if filename.endswith('.nii.gz'):
        source_path = os.path.join(source_folder, filename)
        destination_filename = filename.replace('.nii.gz', '.nii')
        destination_path = os.path.join(destination_folder, destination_filename)

        print(f"Unzipping {filename} -> {destination_filename}")
        
        with gzip.open(source_path, 'rb') as f_in:
            with open(destination_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

print("\n🎯 Done unzipping all .nii.gz files into the destination folder!")
