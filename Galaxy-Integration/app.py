from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='./galaxy-web/dist', static_url_path='/')

@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
