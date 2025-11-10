import os
import shutil

source_folder = r"C:\Users\kovac\PycharmProjects\MagicalJourney"
target_folder = os.path.join(source_folder, "converted_txt")

os.makedirs(target_folder, exist_ok=True)

for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".py"):
            src_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_path, source_folder)
            dst_path = os.path.join(target_folder, relative_path).replace(".py", ".txt")

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copyfile(src_path, dst_path)

print("✅ Minden .py fájl konvertálva lett .txt formába.")
