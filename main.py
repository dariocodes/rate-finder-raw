import subprocess
import xml.etree.ElementTree as ET
import os
import shutil

def get_rating(file_path: str)-> str:
    # Run the ExifTool command with the -b option to extract binary data
    process = subprocess.Popen(['exiftool', '-XMP', '-b', file_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print("Error:", err.decode())
        return

    # Parse the XML output
    try:
        root = ET.fromstring(out)
        namespaces = {'xmp': 'http://ns.adobe.com/xap/1.0/'}  # Define the namespace
        rating = root.find('.//xmp:Rating', namespaces)

        if rating is not None:
            return(f"Rating: {rating.text}")
        else:
            return("Rating not found")
    except ET.ParseError as e:
        return("Error parsing XML:", e)
 
if __name__ == '__main__':
    # assign directory
    input_directory = input(str('Path of input directory: '))
    output_directory = input(str('Path of output directory: '))

    # iterate over files in 
    # that directory
    for filename in os.scandir(input_directory):
        if filename.is_file():
            data = get_rating(filename)
            if data == 'Rating: 5':
                shutil.copy(filename, output_directory)
 

