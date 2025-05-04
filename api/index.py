from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import llm

app = Flask(__name__, static_folder='../public', static_url_path='')

expenses = [
    {'id': 1, 'category': 'Food', 'amount': 50, 'date': '2023-10-01'},
    {'id': 2, 'category': 'Transport', 'amount': 20, 'date': '2023-10-02'},
    {'id': 3, 'category': 'Entertainment', 'amount': 100, 'date': '2023-10-03'},
]

balance = 4275.50


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

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/get_balance', methods=['GET'])
def get_balance():
    return str(balance)

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

@app.route('/get_behavior_analysis/<value>', methods=['GET'])
def get_behavior_analysis(value):
    # historial = data.get('historial')
    # nueva_tx = data.get('nueva_tx')
    # Hardcoded example for testing
    historial = [
        {'mcc': 1234, 'description': 'Food', 'risk': 'low', 'explanation': 'Low risk', 'amount': 50},
        {'mcc': 5678, 'description': 'Transport', 'risk': 'medium', 'explanation': 'Medium risk', 'amount': 20},
        {'mcc': 9101, 'description': 'Entertainment', 'risk': 'high', 'explanation': 'High risk', 'amount': 100}
    ]
    nueva_tx = {'mcc': 1234, 'description': 'Food', 'risk': 'low', 'explanation': 'Low risk', 'amount': value}

    # if not historial or not nueva_tx:
    #     return jsonify({'error': 'Invalid input'}), 400

    result = llm.evaluate_behavior(historial, nueva_tx)
    return jsonify(result)

@app.route('/add_money', methods=['POST'])
def add_money():
    # Simulate adding money to the balance
    global balance
    amount = 100
    balance += amount

    return jsonify({'message': f'Added {amount} to balance', 'new_balance': balance})

@app.route('/remove_money', methods=['POST'])
def remove_money():
    # Simulate removing money from the balance
    global balance
    amount = 50
    balance -= amount

    return jsonify({'message': f'Removed {amount} from balance', 'new_balance': balance})

@app.route('/about', methods=['GET'])
def about():
    return 'About'