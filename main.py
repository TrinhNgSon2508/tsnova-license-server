from rembg import remove
from PIL import Image
import os

input_folder = "input"
output_folder = "output"

os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# tạo output nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# duyệt từng file
for filename in os.listdir(input_folder):

    input_path = os.path.join(input_folder, filename)

    # bỏ qua nếu không phải file
    if not os.path.isfile(input_path):
        continue

    try:
        print(f"Processing: {filename}")

        input_image = Image.open(input_path)

        output_image = remove(input_image)

        # tên file output
        name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name}_no_bg.png")

        output_image.save(output_path)

        print(f"Done: {filename}")

    except Exception as e:
        print(f"Error with {filename}: {e}")

print("TSNOVA Batch Remove Complete!")