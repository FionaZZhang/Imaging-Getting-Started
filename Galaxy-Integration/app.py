import os
from flask import Flask, send_from_directory, request
from bioblend.galaxy import GalaxyInstance
# gi = GalaxyInstance('<Galaxy IP>', key='38ae4d7d23fc78506d217aee88282462')
# libs = gi.libraries.get_libraries()
# gi.workflows.show_workflow('workflow ID')
# wf_invocation = gi.workflows.invoke_workflow('workflow ID', inputs)

app = Flask(__name__, static_folder='./galaxy-web/dist', static_url_path='/')

# Define a folder for uploaded images
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        print('received')
        return 'Image received and saved!'

if __name__ == '__main__':
    app.run(debug=True)