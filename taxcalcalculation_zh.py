import pandas as pd

def select_tariftabelle(year, tax_type, tarif):
    # Construct the filename
    filename = f"./tariftabellen/{year}-{tax_type}-{tarif}.csv"
    names_einkommen = ['Einkommensbereich (CHF)', 'Steuer Grundtarif (CHF)', 'Zusätzlicher Steuerbetrag pro 100 CHF']
    names_vermoegen = ['steuerbares Vermögen (CHF)', 'Steuer (CHF)', 'für je weitere 1000. Vemögen']
    names = names_einkommen if tax_type == 'einkommen' else names_vermoegen
    # Read the CSV file
    try:
        data = pd.read_csv(filename, names=names, skiprows=1, header=None)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found. Please check the file path.")
        return None

# Use the function
year = 2018
tax_type = 'einkommen'
# tax_type = 'vermoegen'
# tarif = 'verheiratetentarif'
tarif = 'grundtarif'
data = select_tariftabelle(year, tax_type, tarif)
print(data)