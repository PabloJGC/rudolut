from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

CORS(app)  # Enable CORS for all routes

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

@app.route('/get_monthly_budget', methods=['GET'])
def get_monthly_budget():
    return '1200'

@app.route('/get_days_under_budget', methods=['GET'])
def get_days_under_budget():
    return '19'

@app.route('/get_latest_category_expenses/<n>', methods=['GET'])
def get_latest_category_expenses(n):
    return jsonify({'latest_category_expenses':  [100, 50, 80, 30, 40]})

@app.route('/get_latest_spending_categories/<n>', methods=['GET'])
def get_latest_spending_categories(n):
    return jsonify({'latest_spending_categories':  ['Food', 'Entertainment', 'Transportation', 'Subscriptions', 'Other']})

@app.route('/get_latest_savings/<months>', methods=['GET'])
def get_latest_savings(months):
    return jsonify({'latest_savings': [200, 300, 400, 500, 600, 700, 800, 900, 1000]})
    # return str([200, 300, 400, 500, 600, 700, 800, 900, 1000])

@app.route('/about', methods=['GET'])
def about():
    return 'About'