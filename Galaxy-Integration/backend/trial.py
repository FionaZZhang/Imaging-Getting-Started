from bioblend.galaxy import GalaxyInstance
import time

galaxy_url = "https://usegalaxy.org.au/"
galaxy_api_key = "38ae4d7d23fc78506d217aee88282462"
gi = GalaxyInstance(url=galaxy_url, key=galaxy_api_key)

input_image_path = '../../input.tif'
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

print('hist')
while hist['state'] != 'ok':
    time.sleep(10)  # Wait for 10 seconds before checking again
    hist = gi.histories.show_history(hist['id'])
    print(hist['state'])

datasetinfo = gi.datasets.show_dataset(hist['state_ids']['ok'][-1])
gi.datasets.download_dataset(dataset_id=datasetinfo['id'], file_path="outputs/histogram_equilization.tiff", use_default_filename=False)