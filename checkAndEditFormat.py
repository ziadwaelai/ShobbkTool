import os
from PIL import Image
import re as r

list_of_special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "'", "\"", "<", ">", ",", ".", "?", "/"]
# def convert_and_save_images(input_folder, output_folder, log_func=None):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     valid_extensions = {".png", ".jpeg", ".webp"}
    
#     for filename in os.listdir(input_folder):
#         file_ext = os.path.splitext(filename)[1].lower()
        
#         if file_ext in valid_extensions:
#             try:
#                 input_path = os.path.join(input_folder, filename)
#                 img = Image.open(input_path)

#                 img = img.convert("RGB")
#                 new_filename = os.path.splitext(filename)[0] + ".jpg"
#                 output_path = os.path.join(output_folder, new_filename)

#                 img.save(output_path, "JPEG")
#                 print(f"Converted {filename} to {new_filename} and saved to {output_folder}")
#                 log_func(f"Converted {filename} to {new_filename}\n") if log_func else None

#             except Exception as e:
#                 print(f"Error processing {filename}: {e}")
#                 log_func(f"Error processing {filename}: {e}\n") if log_func else None

#     print("Conversion complete.")
#     log_func("Conversion complete.\n") if log_func else None



def convert_images_to_jpg(input_folder, output_folder, log_func=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        # Get the file path
        file_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Convert the image to RGB mode (necessary for saving as JPG)
                    img = img.convert("RGB")
                    
                    # Preserve the original name and save the image as JPG
                    base_filename = os.path.splitext(filename)[0]
                    # rmove the special characters from the filename
                    for special_character in list_of_special_characters:
                        base_filename = base_filename.replace(special_character, "")
                    output_path = os.path.join(output_folder, f"{base_filename}.jpg")
                    img.save(output_path, "JPEG")
                    
                    print(f"Converted {filename} to {base_filename}.jpg")
                    log_func(f"Converted {filename} to {base_filename}.jpg\n") if log_func else None

            except Exception as e:
                print(f"Could not convert {filename}: {e}")
                log_func(f"Could not convert {filename}: {e}\n") if log_func else None






def compress_images(input_folder, output_folder,log_func=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
            or filename.endswith(".PNG")
        ):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with Image.open(input_path) as img:
                try:
                    if (
                        os.path.getsize(input_path) > 1 * 1024 * 1024 - 100000
                    ):  # Check if image size is greater than 1MB
                        compration_ratio = 1024 * 1024 / os.path.getsize(input_path)
                        compress_images = img.convert("RGB").save(
                            output_path,
                            optimize=True,
                            format="JPEG",
                            quality=int(compration_ratio * 100),
                        )
                        print(
                            f"Compressed {filename} from {os.path.getsize(input_path)} to {os.path.getsize(output_path)}"
                        )
                        log_func(f"Compressed {filename} \n") if log_func else None

                    else:
                        img.save(output_path)  # Save image as it is
                        print(f"Saved {filename}")
                        log_func(f"Saved {filename}\n") if log_func else None
                except:
                    print(f"Error processing {filename}\n")
                    log_func(f"Error processing {filename}\n") if log_func else None
                    


