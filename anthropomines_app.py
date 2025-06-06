
import pandas as pd
import streamlit as st
from datetime import datetime

def calculate_human_months(periods):
    total_months = set()
    results = []
    
    for period in periods:
        start_str, end_str = period.split('-')
        
        # Προσπάθεια αναγνώρισης μορφής ημερομηνίας
        try:
            start_date = datetime.strptime(start_str.strip(), '%d/%m/%Y')
        except ValueError:
            start_date = datetime.strptime(start_str.strip(), '%m/%Y')
        
        try:
            end_date = datetime.strptime(end_str.strip(), '%d/%m/%Y')
        except ValueError:
            end_date = datetime.strptime(end_str.strip(), '%m/%Y')
        
        months = pd.date_range(start_date, end_date, freq='MS').strftime('%Y-%m').tolist()
        total_months.update(months)
        results.append((period, len(months)))
    
    return results, len(total_months)

# Streamlit App
st.title('Υπολογισμός Ανθρωπομηνών από Περιόδους')

uploaded_file = st.file_uploader("Ανεβάστε το αρχείο Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    periods = df.stack().dropna().astype(str).tolist()
    
    results, total = calculate_human_months(periods)
    
    st.write("### Ανθρωπομήνες ανά περίοδο:")
    for period, months in results:
        st.write(f"Περίοδος: {period} → {months} ανθρωπομήνες")
    
    st.write(f"### Συνολικοί Ανθρωπομήνες: {total}")
