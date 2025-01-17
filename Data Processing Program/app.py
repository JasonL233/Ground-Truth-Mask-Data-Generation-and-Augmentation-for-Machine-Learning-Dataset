from flask import Flask, request, jsonify, render_template
import os
from data_utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processDrawMask', methods=['POST'])
def process_draw_mask_endpoint():
    tarJson_file = request.files.get('tarJsonFile')
    totJson_file = request.files.get('totJsonFile')
    img_folder_path = request.form.get('imgFolderPath')
    target_mask_output_folder_path = request.form.get('targetMaskOutputFolderPath')
    total_mask_output_folder_path = request.form.get('totalMaskOutputFolderPath')
    
    # Save the JSON file
    tarJson_path = os.path.join('/tmp', tarJson_file.filename)
    totJson_path = os.path.join('/tmp', totJson_file.filename)
    
    tarJson_file.save(tarJson_path)
    totJson_file.save(totJson_path)
    
    # Call the drawMask function
    multiDrawMask(tarJson_path, totJson_path, img_folder_path, target_mask_output_folder_path, total_mask_output_folder_path)
    
    return jsonify({'status': 'success'})


@app.route('/processAugmentation', methods=['POST'])
def process_augmentation_endpoint():
    img_files = request.files.getlist('imgFiles')
    target_mask_files = request.files.getlist('targetMaskFiles')
    total_mask_files = request.files.getlist('totalMaskFiles')
    img_output_folder_path = request.form.get('imgOutputFolderPath')
    target_mask_output_folder_path = request.form.get('targetMaskOutputFolderPath')
    total_mask_output_folder_path = request.form.get('totalMaskOutputFolderPath')
    num_augmentations = int(request.form['numAugmentations'])
    
    # Save the files to a temporary location
    for img_file, target_mask_file, total_mask_file in zip(img_files, target_mask_files, total_mask_files):

        img_path = os.path.join('/tmp', img_file.filename)
        target_mask_path = os.path.join('/tmp', target_mask_file.filename)
        total_mask_path = os.path.join('/tmp', total_mask_file.filename)
        
        img_file.save(img_path)
        target_mask_file.save(target_mask_path)
        total_mask_file.save(total_mask_path)
        
        img_output_path = os.path.join(img_output_folder_path, img_file.filename)
        target_mask_output_path = os.path.join(target_mask_output_folder_path, target_mask_file.filename)
        total_mask_output_path = os.path.join(total_mask_output_folder_path, total_mask_file.filename)

        # Call the augmentation function
        for num in range(num_augmentations):  
            augment_image(img_output_path, target_mask_output_path, total_mask_output_path, add_suffix(img_output_path, num+1), add_suffix(target_mask_output_path, num+1), add_suffix(total_mask_output_path, num+1))
    
    return jsonify({'status': 'success'})


@app.route('/processBoth', methods=['POST'])
def process_both_endpoint():
    tar_json_file = request.files['tarJsonFile']
    tot_json_file = request.files['totJsonFile']
    img_folder_path = request.form.get('imgFolderPath')
    target_mask_output_folder_path = request.form.get('targetMaskOutputFolderPath')
    total_mask_output_folder_path = request.form.get('totalMaskOutputFolderPath')
    num_augmentations = int(request.form['numAugmentations'])
    
    
    # Save the files
    tar_json_path = os.path.join('/tmp', tar_json_file.filename)
    tot_json_path = os.path.join('/tmp', tot_json_file.filename)
    
    tar_json_file.save(tar_json_path)
    tot_json_file.save(tot_json_path)
    
    
    # Call the both function
    multiDrawMask(tar_json_path, tot_json_path, img_folder_path, target_mask_output_folder_path, total_mask_output_folder_path, num_augmentations)
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)