import os
import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs
from PIL import Image
from io import BytesIO

def convert_google_drive_link(url):
    # Check if the URL is a Google Drive link
    parsed_url = urlparse(url)
    if 'drive.google.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'id' in query_params:
            file_id = query_params['id'][0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        elif 'file' in parsed_url.path:
            file_id = parsed_url.path.split('/')[3]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def download_images(input_folder, output_folder, log_func=None):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Search for a CSV or Excel file in the input folder
    input_file = None
    for file in os.listdir(input_folder):
        if file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.xls'):
            input_file = os.path.join(input_folder, file)
            break
    if input_file is None:
        print("No CSV or Excel file found in the input folder.")
        log_func("No CSV or Excel file found in the input folder.\n") if log_func else None
        return

    # Determine the file type and read the file
    file_extension = os.path.splitext(input_file)[1].lower()
    if file_extension == '.csv':
        df = pd.read_csv(input_file)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file)
    else:
        print("Unsupported file type. Please provide a CSV or Excel file.")
        log_func("Unsupported file type. Please provide a CSV or Excel file.\n") if log_func else None
        return

    # Make column names lower case
    df.columns = df.columns.str.lower()

    # Ensure the dataframe contains columns with image URLs and names
    if 'links' not in df.columns or 'names' not in df.columns:
        print("The input file must contain columns named 'links' and 'names'.")
        log_func("The input file must contain columns named 'links' and 'names'.\n") if log_func else None
        return

    # Download each image
    for index, row in df.iterrows():
        links = row['links']
        names = row['names']
        direct_url = convert_google_drive_link(links)
        try:
            response = requests.get(direct_url, stream=True)
            response.raise_for_status()

            # Open the image
            image = Image.open(BytesIO(response.content))

            # Save the image with the specified name and .jpg extension
            output_path = os.path.join(output_folder, f"{names}.jpg")
            image = image.convert("RGB")  # Ensure the image is in RGB mode
            image.save(output_path, 'JPEG')

            print(f"Downloaded {names} to {output_folder}")
            log_func(f"Downloaded {names}\n") if log_func else None

        except (requests.RequestException, IOError) as e:
            print(f"Failed to download or process {links}: {e}")