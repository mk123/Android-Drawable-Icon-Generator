from PIL import Image
import sys
import os
import imghdr
import shutil


def resize_image(input_image_path, file_name):
    image = Image.open(input_image_path)
    for icon_ratio, icon_relative_location in zip(icon_size_ratio, icon_size_location):
        height = width = int(highest_resolution * (icon_ratio / icon_size_ratio[0]))
        resized_image = image.resize((height, width), Image.LANCZOS)
        resized_icon_directory = destination_directory + os.sep + icon_relative_location
        if destination_subdirectories.__len__() == 0:
        	resized_icon_location = resized_icon_directory + os.sep + file_name
        else:
        	resized_icon_location = resized_icon_directory + os.sep + \
        	 "_".join(destination_subdirectories) + "_" + file_name
        if not os.path.isdir(resized_icon_directory):
            os.makedirs(resized_icon_directory)
        resized_image.save(resized_icon_location, quality=90)


def read_directory(input_location):
    for file_name in os.listdir(input_location + os.sep + os.sep.join(destination_subdirectories)):
        if destination_subdirectories.__len__() == 0:
            absolute_file_path = input_location + os.sep + file_name
        else:
            absolute_file_path = input_location + os.sep + os.sep.join(destination_subdirectories) \
                                 + os.sep + file_name
        if os.path.isdir(absolute_file_path):
            destination_subdirectories.append(file_name)
            read_directory(input_location)
            destination_subdirectories.pop()
        else:
            # check if file is image
            if imghdr.what(absolute_file_path):
                resize_image(absolute_file_path, file_name)


# get directory location
location = sys.argv[1]
icon_size_ratio = [4, 3, 2, 1.5, 1, 0.75]
icon_size_location = ['drawable-xxxhdpi', 'drawable-xxhdpi',
                      'drawable-xhdpi', 'drawable-hdpi', 'drawable-mdpi',
                      'drawable-ldpi']
highest_resolution = 192
if location.endswith(os.sep):
    location = location[0:location.__len__() - 1]
destination_directory = location + os.sep + "resized_images"
destination_subdirectories = []

# check if resolution is specified first argument is default and value is file name
# second argument is location of directory of icons to be resized
if sys.argv.__len__() > 2:
    input_resolution_value = sys.argv[2] 
    if input_resolution_value.isdigit():
        highest_resolution = int(input_resolution_value)
    else:
        print("Enter correct resolution")
        print("using default hightest resolution")

# check if input location is directory
if not os.path.isdir(location):
    exit("Please provide correct directory location")
    exit()

# remove if destination directory exists
if os.path.isdir(destination_directory):
    shutil.rmtree(destination_directory)

# geneate resized icon  send absolution location and relative root
read_directory(location)

