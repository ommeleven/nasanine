import xarray
import re
import tempfile
import numpy as np
import boto3
import os
import gzip,shutil, wget
import s3fs
import hashlib
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from my_connection_string import my_connection_string
import requests
# Need to replace with the actual connection string
blob_service_client = BlobServiceClient.from_connection_string(my_connection_string)
container_name = "nasaocaid"
container_client = blob_service_client.create_container(container_name)


session = boto3.session.Session()
s3_client = session.client("s3")
fs = s3fs.S3FileSystem()

data_dir = "data/"
dataset_name = "odiac-ffco2-monthgrid-v2023"
cog_data_bucket = "ghgc-data-store-develop"
cog_data_prefix= f"transformed_cogs/{dataset_name}"
cog_checksum_prefix= "checksum"

# Retrieve the checksum of raw files
checksum_dict ={}
for year in range(2000,2023):
    checksum_url = f"https://db.cger.nies.go.jp/nies_data/10.17595/20170411.001/odiac2023/1km_tiff/{year}/odiac2023_1km_checksum_{year}.md5.txt"
    response = requests.get(checksum_url)
    content = response.text
    tmp={}
    
    # Split the content into lines
    lines = content.splitlines()
    
    for line in lines:
        checksum, filename = line.split()
        tmp[filename[:-3]] = checksum
    checksum_dict.update(tmp)
checksum_dict = {k: v for k, v in checksum_dict.items() if k.endswith('.tif')}


def calculate_md5(file_path):
    """
    Calculate the MD5 hash of a file.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The MD5 hash of the file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#Code to download raw ODIAC data in your local machine

# Creating  a base directory for ODIAC data
if not os.path.exists(data_dir):
        os.makedirs(data_dir)

checksum_dict_local={}
# Download and unzip data for the years you want
# for year in range(2000,2023):
    # year_dir = os.path.join(data_dir, str(year))
    # checksum_download_link = f"https://db.cger.nies.go.jp/nies_data/10.17595/20170411.001/odiac2023/1km_tiff/{year}/odiac2023_1km_checksum_{year}.md5.txt"
    # wget.download(checksum_download_link, year_dir)
    # # Make a subfolder for each year
    # if not os.path.exists(year_dir):
    #     os.makedirs(year_dir)

    # for month in range(1,13):
    #     month = f"{month:02d}"
    #     download_link = f"https://db.cger.nies.go.jp/nies_data/10.17595/20170411.001/odiac2023/1km_tiff/{year}/odiac2023_1km_excl_intl_{str(year)[-2:]}{month}.tif.gz"
    #     target_folder = f"{data_dir}/{year}/"
    #     fname = os.path.basename(download_link)
    #     target_path = os.path.join(target_folder, fname)

    #     # Download the file
    #     wget.download(download_link, target_path)

    #     # Unzip the file
    #     with gzip.open(target_path, 'rb') as f_in:
    #         with open(target_path[:-3], 'wb') as f_out:
    #             shutil.copyfileobj(f_in, f_out)
                
    #     # Calculate checksum of the .gz file 
    #     checksum_dict_local[target_path.split("/")[-1][:-3]]=calculate_md5(target_path)
        
    #     # Remove the zip file
    #     os.remove(target_path)

for year in range(2000,2023):
    for month in range(1,13):
        month = f"{month:02d}"
        download_link = f"https://db.cger.nies.go.jp/nies_data/10.17595/20170411.001/odiac2023/1km_tiff/{year}/odiac2023_1km_excl_intl_{str(year)[-2:]}{month}.tif.gz"
        fname = os.path.basename(download_link)
        target_path = f"{year}/{fname}"

        # Download the file
        response = requests.get(download_link, stream=True)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container_name, target_path)

        # Upload the file
        blob_client.upload_blob(response.raw.read())

        # Calculate checksum of the .gz file 
        checksum_dict_local[target_path.split("/")[-1][:-3]]=calculate_md5(response.raw)


    # check if the checksums match
checksum_dict_local == checksum_dict
# List of years you want to run the transformation on
fold_names=[str(i) for i in range(2020,2023)]

for fol_ in fold_names:
    names= os.listdir(f"{data_dir}{fol_}")
    names= [name for name in names if name.endswith('.tif')]
    print("For year: " ,fol_)
    for name in names:
        xds = xarray.open_dataarray(f"{data_dir}{fol_}/{name}")
        filename = name.split("/ ")[-1]
        filename_elements = re.split("[_ .]", filename)
        
        # Remove the extension
        filename_elements.pop()
        # Extract and insert date of generated COG into filename
        filename_elements[-1] = fol_ + filename_elements[-1][-2:]

        # Replace 0 values  with -9999
        xds = xds.where(xds!=0, -9999)
        xds.rio.set_spatial_dims("x", "y", inplace=True)
        xds.rio.write_nodata(-9999, inplace=True)
        xds.rio.write_crs("epsg:4326", inplace=True)

        cog_filename = "_".join(filename_elements)
        cog_filename = f"{cog_filename}.tif"

        # Write the cog file to s3 
        with tempfile.NamedTemporaryFile() as temp_file:
            xds.rio.to_raster(
                temp_file.name,
                driver="COG",
                compress="DEFLATE"
            )
            s3_client.upload_file(
                Filename=temp_file.name,
                Bucket=cog_data_bucket,
                Key=f"{cog_data_prefix}/{cog_filename}",
            )

        print(f"Generated and saved COG: {cog_filename}")

print("ODIAC COGs generation completed!!!")
