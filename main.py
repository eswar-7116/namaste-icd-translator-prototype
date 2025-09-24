from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import pandas as pd
import os

from utils import *

# CSV file path
csv_file = "namaste_icd_mapping.csv"

app = Flask(__name__)

CORS(app)

def load_csv_data(path):
    """Load the NAMASTE ICD mapping CSV into a Pandas DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at: {path}")

    df = pd.read_csv(path, dtype=str).fillna("")
    df.columns = [c.strip().strip('-') for c in df.columns]  # clean column names

    # Add lowercase & normalized columns for searching
    df["namc_term_lower"] = df.get("NAMC_term", "").str.lower()
    df["icd_title_lower"] = df.get("ICD_Title", "").str.lower()
    df["icd_code_clean"] = df.get("ICD_Code", "").str.strip()
    df["namc_id_clean"] = df.get("NAMC_ID", "").str.strip()
    return df

# Try to load CSV at startup
try:
    dataframe = load_csv_data(csv_file)
except Exception as e:
    dataframe = None
    abort(500, description=f"Could not load terminology CSV: {e}")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/search", methods=["GET"])
def search():
    """
    Search NAMC_term, ICD_Title, or ICD_Code for a keyword.
    Example: /search?term=arthritis&limit=10
    """
    search_text = request.args.get("term", "").strip().lower()
    if not search_text:
        return jsonify({"error": "query param 'term' required"}), 400
    
    limit = int(request.args.get("limit", 20))
    
    # Match in term, title, or code
    condition = (
        dataframe["namc_term_lower"].str.contains(search_text, na=False)
        | dataframe["icd_title_lower"].str.contains(search_text, na=False)
        | dataframe["icd_code_clean"].str.lower().str.contains(search_text, na=False)
    )
    
    matches = dataframe[condition].head(limit)
    results = [row_to_search_result(r) for _, r in matches.to_dict(orient="index").items()]
    return jsonify({"query": search_text, "count": len(results), "results": results})

@app.route("/translate/namc/<namc_id>", methods=["GET"])
def translate_from_namc(namc_id):
    if not namc_id:
        return jsonify({"error": "namc_id required"}), 400
    
    matches = dataframe[dataframe["namc_id_clean"] == namc_id.strip()]
    if matches.empty:
        return jsonify({"namc_id": namc_id, "mappings": []}), 200
    
    mappings = [row_to_mapping(r) for _, r in matches.iterrows()]
    return jsonify({"namc_id": namc_id, "mappings": mappings})

@app.route("/translate/icd/<icd_code>", methods=["GET"])
def translate_from_icd(icd_code):
    if not icd_code:
        return jsonify({"error": "icd_code required"}), 400
    
    code = icd_code.strip()
    matches = dataframe[dataframe["icd_code_clean"].str.lower() == code.lower()]
    
    if matches.empty:
        matches = dataframe[dataframe["icd_code_clean"].str.contains(code, case=False, na=False)]
    
    namc_terms = [row_to_namc(r) for _, r in matches.iterrows()]
    return jsonify({"icd_code": icd_code, "namc_terms": namc_terms})

@app.route("/namc/<namc_id>", methods=["GET"])
def namc_details(namc_id):
    """
    Get full details for a specific NAMC_ID (term, definitions, ICD mappings).
    """
    id_filter = dataframe["namc_id_clean"] == namc_id.strip()
    matches = dataframe[id_filter]
    
    if matches.empty:
        return jsonify({"namc_id": namc_id, "found": False}), 200
    
    first_row = matches.iloc[0].to_dict()
    details = {
        "NAMC_ID": first_row.get("NAMC_ID"),
        "NAMC_term": first_row.get("NAMC_term"),
        "NAMC_longDef": first_row.get("NAMC_longDef"),
        "NAMC_shortDef": first_row.get("NAMC_shortDef"),
        "mappings": []
    }
    
    for _, r in matches.to_dict(orient="index").items():
        details["mappings"].append({
            "ICD_Code": r.get("ICD_Code") or None,
            "ICD_Title": r.get("ICD_Title") or None,
            "Similarity": (float(r.get("Similarity")) if r.get("Similarity") not in (None, "") else None)
        })
    
    return jsonify({"namc_id": namc_id, "found": True, "data": details})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
