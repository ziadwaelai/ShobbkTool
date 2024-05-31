from PIL import Image
import os
import random as r


def resize_images_in_folder(input_folder, output_folder,log_func=None):
    # Set the target size for the images
    target_size = (1024, 1024)
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is an image
        if (
            filename.endswith(".jpg")
            or filename.endswith(".png")
            or filename.endswith(".jpeg")
            or filename.endswith(".PNG")
        ):
            # Open the image file
            with Image.open(os.path.join(input_folder, filename)) as img:
                try:
                    # Convert the image to RGB mode if it's in RGBA mode
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    # Resize the image
                    resized_img = img.resize(target_size)
                    # Save the resized image to the output folder
                    resized_img.save(os.path.join(output_folder, filename))
                    print(f"Resized {filename} to {target_size}")
                    log_func(f"Resized {filename} to {target_size}\n") if log_func else None
                except:                    
                    print(f"Error resizing {filename}")
                    log_func(f"Error resizing {filename}\n") if log_func else None

    # choose a random image from the input folder
    random_image = r.choice(os.listdir(input_folder))
    # resize the random image to be 1290*789
    with Image.open(os.path.join(input_folder, random_image)) as img:
        try:
            # Convert the image to RGB mode if it's in RGBA mode
            if img.mode == "RGBA":
                img = img.convert("RGB")
            resized_img = img.resize((1290, 789))
            # save the resized image to the output folder with name "Banner.jpg"
            resized_img.save(os.path.join(output_folder, "Banner.jpg"))
            print(f"Resized {random_image} to 1290*789 and saved as Banner.jpg")
            log_func(f"Resized {random_image} to 1290*789 and saved as Banner.jpg\n") if log_func else None
        except:
            print(f"Error resizing {random_image} as Banner.jpg")
            log_func(f"Error resizing {random_image} as Banner.jpg\n") if log_func else None