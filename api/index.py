from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import google.generativeai as genai
import csv
import json
import re

# Configure the Generative AI model
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

# Load MCC risk data from CSV into a dictionary
mcc_riesgos = {}
with open("mcc_riesgos.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mcc = row["mcc"]
        mcc_riesgos[mcc] = row

def evaluate_behavior(historial, nueva_tx):
    # Helper function to describe a transaction
    def describir_transaccion(tx):
        mcc = str(tx.get("mcc", ""))
        riesgo_info = mcc_riesgos.get(mcc, {})
        return {
            "mcc": mcc,
            "description": riesgo_info.get("description", "Unknown"),
            "risk": riesgo_info.get("risk", "Unknown"),
            "explanation": riesgo_info.get("explanation", "Unavailable"),
            "monto": round(tx.get("amount", 0), 2)
        }

    # Process historical transactions
    historial_info = [describir_transaccion(tx) for tx in historial]

    # Process the new transaction
    nueva_tx_info = describir_transaccion(nueva_tx)

    # Construct the prompt for the AI model
    prompt = f"""
You are a financial advisor expert in spending behavior, meant to criticize the user's transaction history and analyze a new transaction in a funny, grumpy way if they're spending too much.

Analyze whether the following transaction is justifiable for the user, based on their spending history and the risk classification of the MCC code.

User's transaction history (last 10 transactions):
{json.dumps(historial_info, indent=2, ensure_ascii=False)}

New transaction:
{json.dumps(nueva_tx_info, indent=2, ensure_ascii=False)}

Is this transaction consistent with the user's history and expected prediction? VERY briefly justify your analysis based on the MCC risk and prior behavior. Return the final analysis in JSON with the following fields:

- mcc  
- description  
- risk  
- explanation  
- justified (yes/no)  
- reasoning  
"""

    # Generate the response from the AI model
    response = model.generate_content(prompt)
    texto = response.text.strip()

    # Extract JSON from the response
    match = re.search(r'{.*}', texto, re.DOTALL)
    if match:
        try:
            json_data = json.loads(match.group())
            return json_data
        except json.JSONDecodeError:
            pass

    # Fallback response if JSON extraction fails
    return {
        "mcc": nueva_tx_info["mcc"],
        "description": nueva_tx_info["description"],
        "risk": nueva_tx_info["risk"],
        "explanation": nueva_tx_info["explanation"],
        "justified": "no",
        "reasoning": "Could not extract valid JSON from the response."
    }


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
    value = float(value)
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

    result = evaluate_behavior(historial, nueva_tx)
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