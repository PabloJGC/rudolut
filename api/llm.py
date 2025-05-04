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
