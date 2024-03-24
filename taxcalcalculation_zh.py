import pandas as pd

def select_tariftabelle(year, tax_type, tariff):
    # Construct the filename
    filename = f"./tariftabellen/{year}-{tax_type}-{tariff}.csv"

    # Read the CSV file
    try:
        data = pd.read_csv(filename, names=['Einkommensbereich (CHF)', 'Steuer Grundtarif (CHF)', 'Zusätzlicher Steuerbetrag pro 100 CHF'], skiprows=1, header=None)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found. Please check the file path.")
        return None

# Use the function
year = 2018
tax_type = 'einkommen'
# tarif = 'verheiratetentarif'
tarif = 'grundtarif'
data = select_tariftabelle(year, tax_type, tarif)
print(data)