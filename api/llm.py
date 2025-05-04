import google.generativeai as genai
import pandas as pd
import re
import json

genai.configure(api_key="AIzaSyDkcG9lVOt6LSg4y29rnKdsKdCMp-37I_I")
model = genai.GenerativeModel("gemini-2.0-flash")

mcc_riesgos_df = pd.read_csv("mcc_riesgos.csv", dtype={"mcc": str})
mcc_riesgos = {row["mcc"]: row.to_dict() for _, row in mcc_riesgos_df.iterrows()}


def evaluate_behavior(historial, nueva_tx):
    # Preprocess the data
    historial = pd.DataFrame(historial)
    nueva_tx = pd.DataFrame(nueva_tx).to_csv

    def describir_transaccion(tx):
        mcc = str(tx["mcc"])
        riesgo_info = mcc_riesgos.get(mcc, {})
        return {
            "mcc": mcc,
            "description": riesgo_info.get("description", "Unknown"),
            "risk": riesgo_info.get("risk", "Unknown"),
            "explanation": riesgo_info.get("explanation", "Unavailable"),
            "monto": round(tx["amount"], 2)
        }

    historial_info = [describir_transaccion(tx) for _, tx in historial.iterrows()]
    nueva_tx_info = describir_transaccion(nueva_tx)

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

    response = model.generate_content(prompt)
    texto = response.text.strip()

    match = re.search(r'{.*}', texto, re.DOTALL)
    if match:
        json_data = json.loads(match.group())
        return json_data
    else:
        print("Could not extract valid JSON from the response:")
        return {
            "mcc": nueva_tx_info["mcc"],
            "description": nueva_tx_info["description"],
            "risk": nueva_tx_info["risk"],
            "explanation": nueva_tx_info["explanation"],
            "justified": "no",
            "reasoning": "Could not extract valid JSON from the response."
        }
