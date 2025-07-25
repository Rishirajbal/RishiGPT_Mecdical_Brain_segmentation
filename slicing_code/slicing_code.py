import os
import nibabel as nib
import numpy as np
import cv2
from tqdm import tqdm

# Input Paths
train_images_path = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\datasets\Task01_BrainTumour\imagesTr _unzipped'
train_labels_path = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\datasets\Task01_BrainTumour\lablesTr_unzipped'
test_images_path = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\datasets\Task01_BrainTumour\imagesTs_unzipped'

# Output Paths
output_train_images = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\2D_dataset\train\images'
output_train_masks = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\2D_dataset\train\masks'
output_test_images = r'C:\Users\KIIT\OneDrive\Desktop\Resume bulider\projects\Tumour_detection_project\2D_dataset\test\images'

# Create output directories
os.makedirs(output_train_images, exist_ok=True)
os.makedirs(output_train_masks, exist_ok=True)
os.makedirs(output_test_images, exist_ok=True)

# Normalization function
def normalize_img(img):
    img = img - np.min(img)
    if np.max(img) != 0:
        img = img / np.max(img)
    img = (img * 255).astype(np.uint8)
    return img

# ----------- Process Training Data (Images + Masks) ----------- 
print("🔎 Processing Training Data Smartly...")
train_img_files = sorted(os.listdir(train_images_path))
train_label_files = sorted(os.listdir(train_labels_path))

neighbor_range = 2  # save ±2 slices around tumor slices

for img_name, label_name in tqdm(zip(train_img_files, train_label_files), total=len(train_img_files)):
    img_path = os.path.join(train_images_path, img_name)
    label_path = os.path.join(train_labels_path, label_name)

    img_nii = nib.load(img_path)
    label_nii = nib.load(label_path)

    img_data = img_nii.get_fdata()
    label_data = label_nii.get_fdata()

    important_slices = set()

    # First pass: find slices with tumor
    for slice_idx in range(label_data.shape[2]):
        label_slice = label_data[:, :, slice_idx]
        if np.sum(label_slice) > 0:  # tumor exists
            # Mark this slice and neighbors
            for offset in range(-neighbor_range, neighbor_range + 1):
                neighbor_idx = slice_idx + offset
                if 0 <= neighbor_idx < label_data.shape[2]:  # stay in bounds
                    important_slices.add(neighbor_idx)

    # Second pass: save important slices
    for slice_idx in important_slices:
        img_slice = img_data[:, :, slice_idx]
        label_slice = label_data[:, :, slice_idx]

        img_slice_norm = normalize_img(img_slice)
        label_slice_bin = (label_slice > 0).astype(np.uint8) * 255

        # Check if there's tumor and append appropriate label to filename
        if np.sum(label_slice_bin) > 0:
            tumor_status = "tumor"
        else:
            tumor_status = "no_tumor"

        img_filename = f"{img_name.replace('.nii.gz', '').replace('.nii','')}_slice{slice_idx}_{tumor_status}.png"
        mask_filename = f"{label_name.replace('.nii.gz', '').replace('.nii','')}_slice{slice_idx}_{tumor_status}.png"

        cv2.imwrite(os.path.join(output_train_images, img_filename), img_slice_norm)
        cv2.imwrite(os.path.join(output_train_masks, mask_filename), label_slice_bin)

# ----------- Process Testing Data (Images only) ----------- 
print("\n🔎 Processing Testing Data (full slicing)...")
test_img_files = sorted(os.listdir(test_images_path))

for img_name in tqdm(test_img_files):
    img_path = os.path.join(test_images_path, img_name)

    img_nii = nib.load(img_path)
    img_data = img_nii.get_fdata()

    for slice_idx in range(img_data.shape[2]):
        img_slice = img_data[:, :, slice_idx]

        img_slice_norm = normalize_img(img_slice)

        # Since there is no mask for test data, just save the slice with a "no_tumor" tag
        img_filename = f"{img_name.replace('.nii.gz', '').replace('.nii','')}_slice{slice_idx}_no_tumor.png"
        cv2.imwrite(os.path.join(output_test_images, img_filename), img_slice_norm)

print("\n✅ Done Smartly! Saved clean slices inside '2D_dataset' 🚀")
