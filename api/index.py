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

@app.route('/get_monthly_budget')
def get_monthly_budget():
    return '1500'

@app.route('/get_days_under_budget')
def get_days_under_budget():
    return '19'

@app.route('/get_latest_category_expenses/<n>')
def get_latest_category_expenses(n):
    return '19'

@app.route('/get_latest_spending_categories/<n>')
def get_latest_spending_categories(n):
    return '19'

@app.route('/get_latest_savings/<months>')
def about(months):
    return str([200, 300, 400, 500, 600, 700, 800, 900, 1000])

@app.route('/about')
def about():
    return 'About'