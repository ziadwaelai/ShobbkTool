import os
from PIL import Image, ImageChops

def trim(image):
    """Trim the transparent edges of the image."""
    bg = Image.new(image.mode, image.size, (255, 255, 255, 0))  # Create a solid background with transparency
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image

def add_background(input_folder, output_folder, log_func=None):
    # Load the background image
    try:
        background = Image.open(os.path.join(input_folder, "background.jpg"))
    except FileNotFoundError:
        print("The background image does not exist, using a white background.")
        if log_func:
            log_func("The background image does not exist, using a white background.\n")
        background = Image.new('RGB', (1024, 1024), (255, 255, 255))

    # Resize background to 1024x1024
    size = (1024, 1024)
    background = background.resize(size)

    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the images in the input folder
    for object_filename in os.listdir(input_folder):
        if object_filename.lower().endswith(('.png', '.jpg', '.jpeg')) and object_filename.lower() != "background.jpg":
            object_path = os.path.join(input_folder, object_filename)

            if os.path.isfile(object_path):
                try:
                    # Load the object image
                    object_image = Image.open(object_path).convert("RGBA")

                    # Trim the transparent edges
                    object_image = trim(object_image)

                    # Calculate the new size to cover 70% of the background
                    factor = 0.7
                    target_area = factor * (size[0] * size[1])
                    aspect_ratio = object_image.width / object_image.height
                    object_width = int((target_area * aspect_ratio) ** 0.5)
                    object_height = int((target_area / aspect_ratio) ** 0.5)
                    object_size = (object_width, object_height)

                    # Resize the object image
                    object_image = object_image.resize(object_size)

                    # Center the object image on the background
                    position = ((size[0] - object_image.size[0]) // 2, (size[1] - object_image.size[1]) // 2)
                    combined = background.copy()
                    combined.paste(object_image, position, object_image)

                    # Save the combined image in JPEG format
                    output_filename = os.path.splitext(object_filename)[0] + '.jpg'
                    output_path = os.path.join(output_folder, output_filename)
                    combined.save(output_path, 'JPEG')
                    print(f"Added background to {object_filename}")
                    if log_func:
                        log_func(f"Added background to {object_filename}\n")

                    
                    # remove the original image
                    os.remove(object_path)
                except Exception as e:
                    print(f"Error combining {object_filename}: {e}")
                    if log_func:
                        log_func(f"Error combining {object_filename}: {e}\n")
                    continue
            else:
                print(f"Skipping {object_filename}: not a file")
                if log_func:
                    log_func(f"Skipping {object_filename}: not a file\n")
        else:
            print(f"Skipping {object_filename}: not a PNG, JPG, or JPEG file")
            if log_func:
                log_func(f"Skipping {object_filename}: not a PNG, JPG, or JPEG file\n")