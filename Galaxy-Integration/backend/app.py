import os
from flask import Flask, send_from_directory, request
from bioblend.galaxy import GalaxyInstance
import json
from flask_cors import CORS
import os
import time
import cv2
import numpy as np
import ast
import subprocess
import sys

app = Flask(__name__, static_folder='../galaxy-web/dist', static_url_path='/')
CORS(app)

# Define a folder for uploaded images
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define a folder for processed images
OUTPUT_FOLDER = './outputs'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

galaxy_url = "https://usegalaxy.org.au/"
galaxy_api_key = "******" # replace with your Galaxy API
gi = GalaxyInstance(url=galaxy_url, key=galaxy_api_key)

milton_acc = "your.account" # replace with your Milton account

def histogram_normalisation(input_image_path, output_folder):
    history_name = 'HistogramNormalisationInput'
    history = gi.histories.create_history(name=history_name)
    input_dataset = gi.tools.upload_file(input_image_path, history['id'])
    input_id = input_dataset['outputs'][0]['id']
    input_dataset = gi.datasets.show_dataset(input_dataset['outputs'][0]['id'])

    print("input_dataset")
    while input_dataset['state'] != 'ok':
        time.sleep(5)
        input_dataset = gi.datasets.show_dataset(input_dataset['dataset_id'])
        print(input_dataset['state'])

    workflow = gi.workflows.show_workflow('b7acc99e5fb755e8')
    datamap = {
        '0': {
            'src': 'hda',
            'id': input_id,
        }
    }
    hist = gi.workflows.invoke_workflow(workflow['id'], inputs=datamap, history_id=history['id'])
    hist = gi.histories.show_history(hist['history_id'])

    state_times = {}
    print('hist')
    timer = 0
    while hist['state'] != 'ok':
        time.sleep(1)  # Wait for 10 seconds before checking again
        hist = gi.histories.show_history(hist['id'])
        print(hist['state'])
        timer += 1
        if hist['state'] not in state_times:
            state_times[hist['state']] = 1
        else:
            state_times[hist['state']] += 1

    datasetinfo = gi.datasets.show_dataset(hist['state_ids']['ok'][-1])
    gi.datasets.download_dataset(dataset_id=datasetinfo['id'], file_path="outputs/histogram_equilization.tiff",
                                 use_default_filename=False)

    image_path = os.path.join(output_folder, 'histogram_equilization.tiff')

    response_data = {
        'state_times': state_times,
        'output_path': image_path
    }

    return response_data


def hdab_counts(image_path):
    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found or could not be read.")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the DAB stain
    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use the blue channel to extract the blue stain
    blue_channel = image[:, :, 0]  # Blue channel is at index 0 for BGR images

    # Calculate the Hematoxylin (H) stain by subtracting the blue channel from the grayscale image
    hematoxylin_image = gray_image - blue_channel

    # Calculate the DAB stain by subtracting the grayscale image from the thresholded image
    dab_image = thresholded_image - gray_image

    # Count the number of pixels in each stain
    h_count = int(np.sum(hematoxylin_image > 0))
    dab_count = int(np.sum(dab_image > 0))

    response_data = {
        "Hcount": h_count,
        "DABcount": dab_count
    }

    return response_data

# This section still have some bugs in it unfortunately.
# def extract_required_libraries(script):
#
#     # Parse the script to extract import statements
#     module = ast.parse(script)
#
#     # Extract import statements
#     imports = [node for node in module.body if isinstance(node, ast.Import)]
#     import_froms = [node for node in module.body if isinstance(node, ast.ImportFrom)]
#
#     # Get module names from import statements
#     required_libraries = []
#     for import_node in imports + import_froms:
#         for alias in import_node.names:
#             required_libraries.append(alias.name)
#
#     return required_libraries
#
# def install_libraries(libraries):
#     for library in libraries:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", library])
#
# def custom(script_path, input_data_path):
#
#     with open(script_path, 'r') as file:
#         script = file.read()
#         print(script)
#
#     # Extract required libraries from the script
#     required_libraries = extract_required_libraries(script)
#
#     # Install required libraries if any
#     if required_libraries:
#         install_libraries(required_libraries)
#
#     # Create a dictionary to store the variables accessible within the script
#     variables = {}
#
#     # Execute the script
#     exec(script, globals(), variables)
#     result = variables.get("main", None)
#
#     if result is None or not callable(result):
#         raise ValueError("No callable 'main' function found in the script")
#
#     return result(input_data_path)


@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/squeue')
def squeue():
    try:
        # Execute the squeue command to get job status
        cmd = "squeue -u " + milton_acc + " --format='%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R'"
        job_status = subprocess.check_output(cmd, shell=True, text=True)

        # Split the output into lines and create a list of dictionaries
        job_list = []
        for line in job_status.strip().split('\n'):
            fields = line.split()
            job_info = {
                'job_id': fields[0],
                'partition': fields[1],
                'name': fields[2],
                'user': fields[3],
                'status': fields[4],
                'memory': fields[5],
                'time': fields[6],
                'nodes': fields[7]
            }
            job_list.append(job_info)

        return json.dumps(job_list)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/response', methods=['POST'])
def upload_image():
    if not request.files:
        return 'No file'
    file = request.files['files']
    workflow = request.form['workflow']

    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        if (workflow == 'workflow1'):
            data_out = histogram_normalisation(filename, app.config['OUTPUT_FOLDER'])
        if (workflow == 'workflow2'):
            data_out = hdab_counts(filename)
        if (workflow == 'workflow3'):

            input = request.form['inputs']
            try:
                # Get the job script from the request
                sbatch_script = request.form['script']

                # Create a temporary script file to store the job script
                script_file_path = 'temp_script.sh'
                control = f'\nmodule load python/3.8.3\npython ./uploads/control.py {filename} {input}'
                with open(script_file_path, 'w') as script_file:
                    script_file.write(sbatch_script)
                    script_file.write(control)

                # Submit the job using sbatch
                cmd = f'sbatch {script_file_path}'
                data_out = subprocess.check_output(cmd, shell=True, text=True)

                # Remove the temporary script file
                subprocess.run(['rm', script_file_path])

            except Exception as e:
                return json.dumps({'error': str(e)})
        return json.dumps(data_out)

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)