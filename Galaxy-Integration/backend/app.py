import os
from flask import Flask, send_from_directory, request
from bioblend.galaxy import GalaxyInstance
import time
import json
from flask_cors import CORS


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
galaxy_api_key = "38ae4d7d23fc78506d217aee88282462"
gi = GalaxyInstance(url=galaxy_url, key=galaxy_api_key)

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
        'image_path': image_path
    }

    return response_data



@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/response', methods=['POST'])
def upload_image():
    if not request.files:
        return 'No file part'
    file = request.files['files']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        data_out = histogram_normalisation(filename, app.config['OUTPUT_FOLDER'])
        return json.dumps(data_out)
@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)