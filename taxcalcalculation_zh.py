import pandas as pd
from enum import Enum

class TaxType(Enum):
    EINKOMMEN = 1
    VERMOEGEN = 2

class Tarif(Enum):
    GRUNDTARIF = 1
    VERHEIRATETENTARIF = 2


def select_tariftabelle(year, tax_type: TaxType, tarif: Tarif):
    filename = f"./tariftabellen/{year}-{tax_type.name.lower()}-{tarif.name.lower()}.csv"
    names_einkommen = ['Einkommensbereich (CHF)', 'Steuer Grundtarif (CHF)', 'Zusätzlicher Steuerbetrag pro 100 CHF']
    names_vermoegen = ['steuerbares Vermögen (CHF)', 'Steuer (CHF)', 'für je weitere 1000. Vemögen']
    names = names_einkommen if tax_type == 'einkommen' else names_vermoegen
    try:
        data = pd.read_csv(filename, names=names, skiprows=1, header=None)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found. Please check the file path.")
        return None
    
def calculate_einfache_steuer_einkommen(year, tarif: Tarif, income, satzbestimmend):
    data = select_tariftabelle(year, TaxType.EINKOMMEN, tarif)
    first_bracket = data.iloc[0]
    if satzbestimmend <= first_bracket.iloc[0]:
        return 0
    
    current_bracket = first_bracket
    for bracket in data.itertuples():
        if satzbestimmend < bracket[1]:
            break
        else:
            current_bracket = bracket
    berechnete_steuer = current_bracket[2] + (satzbestimmend - current_bracket[1]) / 100 * current_bracket[3]
    satz = berechnete_steuer / (satzbestimmend / 100) # pro 100 CHF
    betrag = einkommen / 100 * satz
    return {
        'satz': satz,
        'betrag': betrag
    }


def calculate_einfache_steuer_vermoegen(year, tarif: Tarif, wealth):
    data = select_tariftabelle(year, TaxType.VERMOEGEN, tarif)
    first_bracket = data.iloc[0]
    if wealth <= first_bracket.iloc[0]:
        return 0
    current_bracket = first_bracket
    for bracket in data.itertuples():
        if wealth < bracket[1]:
            break
        else:
            current_bracket = bracket
    betrag = current_bracket[2] + (wealth - current_bracket[1]) / 1000 * current_bracket[3]
    satz = betrag / (wealth / 100)
    return {
        'satz': satz,
        'betrag': betrag
    }


def calculate_staats_gemeinde_steuern(year, tarif: Tarif, einkommen, satzbestimmend, wealth):
    einfache_steuer_einkommen = calculate_einfache_steuer_einkommen(year, tarif, einkommen, satzbestimmend)['betrag']
    einfache_steuer_vermoegen = calculate_einfache_steuer_vermoegen(year, tarif, wealth)['betrag']
    staatssteuerfuss = 0.99 #TODO add steuerfuss to file
    gemeindesteuerfuss = 1.19
    return einfache_steuer_einkommen * staatssteuerfuss + einfache_steuer_einkommen * gemeindesteuerfuss + einfache_steuer_vermoegen * staatssteuerfuss + einfache_steuer_vermoegen * gemeindesteuerfuss
    

einkommen = 79800
satzbestimmend = 79800
wealth = 159000

einfache_steuer_einkommen_grundtarif = calculate_einfache_steuer_einkommen(2018, Tarif.GRUNDTARIF, einkommen, satzbestimmend)
einfache_steuer_einkommen_verheiratetentarif = calculate_einfache_steuer_einkommen(2018, Tarif.VERHEIRATETENTARIF, einkommen, satzbestimmend)
einfache_steuer_vermoegen_grundtarif = calculate_einfache_steuer_vermoegen(2018, Tarif.GRUNDTARIF, wealth)
einfache_steuer_vermoegenx_verheiratetentarif = calculate_einfache_steuer_vermoegen(2018, Tarif.VERHEIRATETENTARIF, wealth)

staats_gemeinde_steuern_grundtarif = calculate_staats_gemeinde_steuern(2018, Tarif.GRUNDTARIF, einkommen, satzbestimmend, wealth)
staats_gemeinde_steuern_verheiratetentarif = calculate_staats_gemeinde_steuern(2018, Tarif.VERHEIRATETENTARIF, einkommen, satzbestimmend, wealth)


print("Einkommen: ", "{:,.2f}".format(einkommen))
print("Satzbestimmend: ", "{:,.2f}".format(satzbestimmend))
print("Vermögen: ", "{:,.2f}".format(wealth))
print("")
print("== Einfache Steuer == ")
print("Satz GT: ", "{:,.3f}".format(einfache_steuer_einkommen_grundtarif['satz']), " pro 100 CHF")
print("Einkommen GT: ", "{:,.2f}".format(einfache_steuer_einkommen_grundtarif['betrag']))
print("Vermögen GT:  ", "{:,.2f}".format(einfache_steuer_vermoegen_grundtarif['betrag']))
print("")
print("Satz VT: ", "{:,.3f}".format(einfache_steuer_einkommen_verheiratetentarif['satz']), " pro 100 CHF")
print("Einkommen VT: ", "{:,.2f}".format(einfache_steuer_einkommen_verheiratetentarif['betrag']))
print("Vermögen VT:  ", "{:,.2f}".format(einfache_steuer_vermoegenx_verheiratetentarif['betrag']))
print("")
print("== Staats- und Gemeindesteuern ==")
print("GT: ", "{:,.2f}".format(staats_gemeinde_steuern_grundtarif))
print("VT: ", "{:,.2f}".format(staats_gemeinde_steuern_verheiratetentarif))
