from PIL import Image
import os
import random
import numpy as np
import cv2
import json
from pathlib import Path
import matplotlib.pyplot as plt


def multiDrawMask(p_target_json_file, p_total_json_file, p_img_dir, p_target_mask_dir, p_total_mask_dir=None, num_augmentation=0):
  """
    A function that translate json file and draw mask that correspond to the raw image.
    Requires: A json file with XY coordinates of the mask (Can be create using VGG Image Annotator)
              A raw image path for width and height
              A mask path for output
    Mask area -> white
    background -> black
  """
  target_json_file = open(p_target_json_file, "r")
  total_json_file = open(p_total_json_file, "r")

  target_data = json.load(target_json_file) # Dictionary
  total_data = json.load(total_json_file)
  tar_data = target_data["_via_img_metadata"]
  tot_data = total_data["_via_img_metadata"]

  img_dir = p_img_dir # The original image directory
  target_mask_dir = p_target_mask_dir
  total_mask_dir = p_total_mask_dir 


  target_keys = list(tar_data.keys())
  total_keys = list(tot_data.keys())
  
  count = 0
  if (len(tar_data) == len(tar_data)):
    for i in range(len(tar_data)):
      tar_key = target_keys[i]
      tot_key = total_keys[i]
      tar_value = tar_data[tar_key]
      tot_value = tot_data[tot_key]
      count += 1
      print(count)
    
      tar_filename = tar_value["filename"]
      tot_filename = tot_value["filename"]
      tar_regions = tar_value["regions"]
      tot_regions = tot_value["regions"]
    
    
      # Get the height and width of the original image
      tar_filename = tar_filename.replace('.jpg', '.png').replace('.JPG', '.png')
      ori_img_path = f"{img_dir}/{tar_filename}"
      
      ori_img_path = convert_image_to_png(ori_img_path)
      tar_filename = os.path.splitext(tar_filename)[0] + '.png'
      tot_filename = os.path.splitext(tot_filename)[0] + '.png'
    
      if not os.path.exists(ori_img_path):
          print(f"File does not exist: {ori_img_path}")
          continue
        
      img = cv2.imread(ori_img_path, cv2.IMREAD_COLOR)
      h, w, _ = img.shape
    
    
      # Draw the background with black color
      tar_mask = np.zeros((h, w))
      tot_mask = np.zeros((h, w))

      if (len(tar_regions) == len(tot_regions)):
        for i in range(len(tar_regions)):
        
          tar_x_points = tar_regions[i]["shape_attributes"]["all_points_x"]
          tar_y_points = tar_regions[i]["shape_attributes"]["all_points_y"]
          
          tot_x_points = tot_regions[i]["shape_attributes"]["all_points_x"]
          tot_y_points = tot_regions[i]["shape_attributes"]["all_points_y"]
        
          tar_contours = []
          tot_contours = []
          
          for x, y in zip(tar_x_points, tar_y_points):
            tar_contours.append((x,y))
          tar_contours = np.array(tar_contours)
          
          for x, y in zip(tot_x_points, tot_y_points):
            tot_contours.append((x,y))
          tot_contours = np.array(tot_contours)
        
          # Draw the mask area with White color
          cv2.drawContours(tar_mask, [tar_contours], -1, i + 1, -1) 
          cv2.drawContours(tot_mask, [tot_contours], -1, i + 1, -1)
      else:
        print("TARGET REGIONS DOES NOT HAVE THE SAME LENGTH AS TOTAL REGIONS")
    
      # Output to the designated pathway

      target_mask_path = f"{target_mask_dir}/targetMask{tar_filename}"
      cv2.imwrite(target_mask_path, tar_mask)


      total_mask_path = f"{total_mask_dir}/totalMask{tot_filename}"
      cv2.imwrite(total_mask_path, tot_mask)
    
      if (total_mask_dir != None):
        for num in range(num_augmentation):
          augment_image(ori_img_path, target_mask_path, total_mask_path, add_suffix(ori_img_path, num+1), add_suffix(target_mask_path, num+1), add_suffix(total_mask_path, num+1))
  else:
    print("TARGET DATA DOES NOT HAVE THE SAME LENGTH AS TOTAL DATA")
    
    
  print("Drawing process succeed!")


def augment_image(raw_path, target_mask_path, total_mask_path, output_raw_path, output_target_mask_path, output_total_mask_path):
    """
    A function for data augmentation by using random rotation, zoom (resize), and shifting
    Data augmentation for both the raw image and the corresponding mask image 
    Requires: A raw image path, 
              A mask path,
              An output path for the raw image
              An output path for the mask
    """
    # Open images
    raw = Image.open(raw_path)
    target_mask = Image.open(target_mask_path)
    total_mask = Image.open(total_mask_path)

    # Get original dimensions
    width, height = raw.size

    # Rotate image randomly between -359 to 360 degrees----------------------------------------------------------------------
    rotate_angle = random.randint(-359, 360)
    raw_rotated_image = raw.rotate(rotate_angle, expand=True, fillcolor=(0, 0, 0))
    target_mask_rotated_image = target_mask.rotate(rotate_angle, expand=True, fillcolor=0)
    total_mask_rotated_image = total_mask.rotate(rotate_angle, expand=True, fillcolor=0)


    # Shift the image--------------------------------------------------------------------------------------------------------
    max_shift = 6  # Maximum shift in pixels
    attempt = 0
    max_attempts = 10
    while True:
      shift_x = random.randint(-max_shift, max_shift)
      shift_y = random.randint(-max_shift, max_shift)

      raw_shifted_image = Image.new("RGB", (width, height), (0, 0, 0))
      target_mask_shifted_image = Image.new("L", (width, height), 0)
      total_mask_shifted_image = Image.new("L", (width, height), 0)

      raw_shifted_image.paste(raw_rotated_image, (shift_x, shift_y))
      target_mask_shifted_image.paste(target_mask_rotated_image, (shift_x, shift_y))
      total_mask_shifted_image.paste(total_mask_rotated_image, (shift_x, shift_y))

      if np.any(np.array(target_mask_shifted_image) > 0):
        print("Shifting Succeeded")
        break
      elif attempt >= max_attempts:
        print("Shifting Failed: Max attempts reached, proceeding without shift")
        target_mask_shifted_image = target_mask_rotated_image
        total_mask_shifted_image = total_mask_rotated_image
        raw_shifted_image = raw_rotated_image
        break
      else:
        attempt += 1
        print(f"Shifting Attempt {attempt} Failed, Retrying...")
              
              
    # Zoom in or out (resize) the image------------------------------------------------------------------------------------
    attempt = 0
    max_attempts = 10
    zoom_factor = random.uniform(0.3, 2)

    while True:
      new_width = int(width * zoom_factor)
      new_height = int(height * zoom_factor)

      raw_zoomed_image = raw_shifted_image.resize((new_width, new_height), Image.BILINEAR)
      target_mask_zoomed_image = target_mask_shifted_image.resize((new_width, new_height), Image.NEAREST)
      total_mask_zoomed_image = total_mask_shifted_image.resize((new_width, new_height), Image.NEAREST)

      # Create a blank canvas with the original size
      final_raw_image = Image.new("RGB", (width, height), (0, 0, 0))
      final_target_mask_image = Image.new("L", (width, height), 0)
      final_total_mask_image = Image.new("L", (width, height), 0)

      # Calculate offsets for centering
      offset_x = (width - new_width) // 2
      offset_y = (height - new_height) // 2

      # Paste the zoomed image into the center of the original size image
      final_raw_image.paste(raw_zoomed_image, (offset_x, offset_y))
      final_target_mask_image.paste(target_mask_zoomed_image, (offset_x, offset_y))
      final_total_mask_image.paste(total_mask_zoomed_image, (offset_x, offset_y))
      
      if (np.any(np.array(target_mask_shifted_image) > 0)):
        print("Resized Succeeded")
        break
      elif (attempt > max_attempts):
        print("Resize Failed: Max attempts reached, proceeding without resize")
        final_raw_image = raw_shifted_image
        final_target_mask_image = target_mask_shifted_image
        final_total_mask_image = total_mask_shifted_image
        break
      else:
        attempt += 1
        print(f"Resize Attempt {attempt} Failed, Retrying...")
        

    
    # Save augmented images
    os.makedirs(os.path.dirname(output_raw_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_target_mask_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_total_mask_path), exist_ok=True)

    final_raw_image.save(output_raw_path, format='PNG')
    final_target_mask_image.save(output_target_mask_path, format='PNG')
    final_total_mask_image.save(output_total_mask_path, format='PNG')

    print("Data augmentation succeeded!")




def count_files(folder_path, file_types='png'):
    """
      A function that return the number of specific files in a given folder
    """
    folder = Path(folder_path)
    files = list(folder.glob('*.' + file_types))
    print(type(file_types))
    return len(files)




def add_suffix(filename, num):
    """
      Example: 1.png -> 1_1.png
    """
    name, ext = os.path.splitext(filename)
    modified_filename = f"{name}_{num}{ext}"
    return modified_filename
  
  
  
  
def convert_image_to_png(image_path):
    """
    Converts an image to PNG format if it's not already a PNG.
    """
    
    if image_path.lower().endswith('.png'):
      return image_path  # No conversion needed
      
    if not os.path.exists(image_path):
      return "NONE.png"
    # Check if the image is already in PNG format


    # Load the image using PIL
    img = Image.open(image_path)

    # Convert to PNG
    png_image_path = os.path.splitext(image_path)[0] + '.png'
    img.save(png_image_path, 'PNG')

    return png_image_path
    