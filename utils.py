def row_to_search_result(row):
    """Convert a row into full NAMC + ICD mapping for search endpoint."""
    return {
        "NAMC_ID": row.get("NAMC_ID") or None,
        "NAMC_term": row.get("NAMC_term") or None,
        "NAMC_shortDef": row.get("NAMC_shortDef") or None,
        "NAMC_longDef": row.get("NAMC_longDef") or None,
        "mapping": {
            "ICD_Code": row.get("ICD_Code") or None,
            "ICD_Title": row.get("ICD_Title") or None,
            "Similarity": (
                float(row["Similarity"]) 
                if row.get("Similarity") not in (None, "", "NaN") else None
            )
        }
    }

def row_to_mapping(row):
    """Convert a Pandas row into a structured ICD mapping dict for JSON response."""
    return {
        "ICD_Code": row.get("ICD_Code") or None,
        "ICD_Title": row.get("ICD_Title") or None,
        "Similarity": (
            float(row["Similarity"])
            if row.get("Similarity") not in (None, "", "NaN") else None
        )
    }

def row_to_namc(row):
    """Convert a row into a NAMC dict for /translate/icd endpoint."""
    return {
        "NAMC_ID": row.get("NAMC_ID") or None,
        "NAMC_term": row.get("NAMC_term") or None,
        "NAMC_shortDef": row.get("NAMC_shortDef") or None,
        "NAMC_longDef": row.get("NAMC_longDef") or None
    }
