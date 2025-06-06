
import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO

def calculate_human_months(periods):
    total_months = set()
    results = []
    
    for period in periods:
        start_str, end_str = period.split('-')
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
    
    df['Ανθρωπομήνες'] = [months for _, months in results]
    df.loc['Σύνολο'] = df.sum(numeric_only=True)
    
    st.write("### Ανθρωπομήνες ανά περίοδο:")
    st.dataframe(df)
    
    st.write(f"### Συνολικοί Ανθρωπομήνες: {total}")
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="Κατεβάστε το αρχείο Excel με τους ανθρωπομήνες",
        data=output.getvalue(),
        file_name="anthropomines_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
