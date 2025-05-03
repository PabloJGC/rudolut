from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# @app.route('/<path:path>')
# def serve_static_file(path):
#     file_path = os.path.join(app.static_folder, path)
#     if os.path.isfile(file_path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return 'File not found', 404

@app.route('/about')
def about():
    return 'About'