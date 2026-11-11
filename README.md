# MedStock AI — DATA THIRAN Prototype

A Streamlit working prototype for **DT-HLT-04: Identifying Patterns in Medicine Demand**.

## Features
- Overview dashboard with inventory KPIs and stock-status charts
- Medicine inventory table, search, category/status filters
- Add a demo medicine during the current session
- Historical usage visualization and transparent baseline demand forecast
- Rule-based stock-risk alerts
- Suggested reorder quantities and estimated order cost
- CSV downloads for inventory and reorder recommendations

## Important
All initial values are **illustrative demo data**, generated inside the app. This is not connected to a real hospital, pharmacy, supplier, or live database. The forecast is a simple baseline method, not a trained or clinically validated AI model. Do not use the outputs for real medicine ordering without review by qualified staff.

## Run in VS Code

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the app:
   ```bash
   python -m streamlit run app.py
   ```

7. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Suggested hackathon demo flow
1. Start on Overview Dashboard.
2. Show Critical/Low stock indicators.
3. Open Medicine Inventory and search for a medicine.
4. Open Demand Forecast and select a medicine.
5. Open Stock Risk & Reorder and explain how the suggested quantity is calculated.
6. Download the reorder CSV to show a practical output.

## Suggested next improvements
- Upload a real, anonymized CSV using a documented schema
- Validate forecast accuracy with MAE/RMSE and a held-out time period
- Add expiry-risk alerts and role-based access
- Store inventory changes in SQLite/PostgreSQL
- Test reorder rules with pharmacy staff before any operational use
