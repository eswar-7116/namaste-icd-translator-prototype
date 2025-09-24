# NAMASTE - ICD Code Translator API Prototype

A prototype API to translate between **AYUSH NAMASTE codes** and **ICD codes** built with **Python**, **Flask**, and **Pandas**.

---

## Setup

### 1. Clone repo & install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the prototype server

* On **Windows**:

  ```bash
  python app.py
  ```
* On **Linux / Mac**:

  ```bash
  python3 app.py
  ```

> The server runs by default on:
> 👉 `http://127.0.0.1:5000`

---

## API Routes

### 1. Health Check

**Endpoint:**

```
GET /health
```

**Usage:**

Visit: `http://127.0.0.1:5000/health`

**Response:**

```json
{ "status": "ok" }
```

---

### 2. Search for Terms

Search across **NAMC\_term**, **ICD\_Title**, or **ICD\_Code**.

**Endpoint:**

```
GET /search?term=<keyword>&limit=<number>
```

**Usage:**

Visit: `http://127.0.0.1:5000/search?term=arthritis&limit=5`

**Response (sample):**

```json
{
  "query": "arthritis",
  "count": 2,
  "results": [
    {
      "NAMC_ID": "12",
      "NAMC_term": "sandhivata",
      "ICD_Code": "M19",
      "ICD_Title": "Other arthritis",
      "Similarity": 0.89
    },
    {
      "NAMC_ID": "34",
      "NAMC_term": "amavata",
      "ICD_Code": "M06",
      "ICD_Title": "Other rheumatoid arthritis",
      "Similarity": 0.92
    }
  ]
}
```

---

### 3. Translate from NAMC\_ID → ICD Codes

Get ICD mappings for a given **NAMC\_ID**.

**Endpoint:**

```
GET /translate/namc/<namc_id>
```

**Usage:**

Visit: `http://127.0.0.1:5000/translate/namc/1`

**Response (sample):**

```json
{
  "namc_id": "1",
  "mappings": [
    {
      "NAMC_ID": "1",
      "NAMC_term": "vyAdhi-viniScayaH",
      "ICD_Code": "SS5F",
      "ICD_Title": "Aiya-predominant Vaḷi body constitution pattern (TM2)",
      "Similarity": 0.2007
    }
  ]
}
```

---

### 4. Translate from ICD\_Code → NAMC Terms

Get NAMC terms linked to a given **ICD\_Code**.

**Endpoint:**

```
GET /translate/icd/<icd_code>
```

**Usage:**

Visit: `http://127.0.0.1:5000/translate/icd/SS5F`

**Response (sample):**

```json
{
  "icd_code": "SS5F",
  "mappings": [
    {
      "NAMC_ID": "1",
      "NAMC_term": "vyAdhi-viniScayaH",
      "ICD_Code": "SS5F",
      "ICD_Title": "Aiya-predominant Vaḷi body constitution pattern (TM2)",
      "Similarity": 0.2007
    }
  ]
}
```

---

### 5. Get NAMC Term Details

Get **full details** for a NAMC\_ID, including definitions and ICD mappings.

**Endpoint:**

```
GET /namc/<namc_id>
```

**Usage:**

Visit: `http://127.0.0.1:5000/namc/2`

**Response (sample):**

```json
{
  "namc_id": "2",
  "found": true,
  "data": {
    "NAMC_ID": "2",
    "NAMC_term": "vikAraH",
    "NAMC_longDef": null,
    "NAMC_shortDef": null,
    "mappings": [
      {
        "ICD_Code": "SR10",
        "ICD_Title": "Vitiation of vāta pattern (TM2)",
        "Similarity": 0.1932
      },
      {
        "ICD_Code": "SM9B",
        "ICD_Title": "Vaginismus disorder (TM2)",
        "Similarity": 0.1648
      }
    ]
  }
}
```
