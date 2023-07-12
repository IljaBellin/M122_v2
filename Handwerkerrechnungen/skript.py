import csv

def generate_invoice_txt(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        
        # Extract data from CSV rows
        rechnung_nr, auftrag_nr, ort, datum, uhrzeit, zahlungsziel = rows[0]
        _, _, kundennummer, kunde, strasse, plz_ort, ust_id, email = rows[1]
        _, _, endkunde, endkunde_adresse, endkunde_plz_ort = rows[2]
        rechnungspositionen = rows[3:]
        
        # Create the invoice text
        invoice_text = '-------------------------------------------------\n\n'
        invoice_text += f'{kunde}\n{strasse}\n{plz_ort}\n\n'
        invoice_text += f'{ust_id}\n\n'
        invoice_text += f'{ort}, den {datum}                           {endkunde}\n'
        invoice_text += f'                                                {endkunde_adresse}\n'
        invoice_text += f'                                                {endkunde_plz_ort}\n\n'
        invoice_text += f'Kundennummer:      {kundennummer}\n'
        invoice_text += f'Auftragsnummer:    {auftrag_nr}\n\n'
        invoice_text += f'Rechnung Nr       {rechnung_nr}\n'
        invoice_text += '-----------------------\n'
        
        total_amount = 0.0
        for pos in rechnungspositionen:
            _, _, beschreibung, menge, einzelpreis, gesamtpreis, mwst = pos
            invoice_text += f'{menge}   {beschreibung.ljust(35)}{einzelpreis.rjust(6)}  CHF      {gesamtpreis}\n'
            total_amount += float(gesamtpreis)
        
        invoice_text += f'{" " * 54}{"-" * 11}\n'
        invoice_text += f'{" " * 43}Total CHF     {total_amount}\n\n'
        invoice_text += f'{" " * 43}MWST  CHF        0.00\n\n'
        invoice_text += f'Zahlungsziel ohne Abzug {zahlungsziel} Tage ({datum})\n\n'
        invoice_text += 'Empfangsschein             Zahlteil\n\n'
        invoice_text += f'{kunde}{" " * (29 - len(kunde))}------------------------  {kunde}\n'
        invoice_text += f'{strasse}{" " * (29 - len(strasse))}|  QR-CODE             |  {strasse}\n'
        invoice_text += f'{plz_ort}{" " * (29 - len(plz_ort))}|                      |  {plz_ort}\n\n'
        invoice_text += f'{" " * 29}|                      |\n{" " * 29}|                      |\n'
        invoice_text += '00 00000 00000 00000 00000 |                      |  00 00000 00000 00000 00000\n\n'
        invoice_text += f'{endkunde}{" " * (29 - len(endkunde))}|                      |  {endkunde}\n'
        invoice_text += f'{endkunde_adresse}{" " * (29 - len(endkunde_adresse))}|                      |  {endkunde_adresse}\n'
        invoice_text += f'{endkunde_plz_ort}{" " * (29 - len(endkunde_plz_ort))}|                      |  {endkunde_plz_ort}\n'
        invoice_text += ' ' * 28 + '------------------------\n'
        invoice_text += 'Waehrung  Betrag            Waehrung  Betrag\n'
        invoice_text += f'CHF      {total_amount}           CHF      {total_amount}\n\n'
        invoice_text += '-------------------------------------------------\n'

        return invoice_text


# Hauptprogramm

import os

# Verzeichnis, in dem sich das Skript befindet
skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))

# Verzeichnis, in dem sich die CSV-Dateien befinden
csv_verzeichnis = os.path.join(skript_verzeichnis, 'data')

# Verzeichnis für die Ausgabe der TXT-Dateien
ausgabe_verzeichnis = os.path.join(skript_verzeichnis, 'ausgaben')

# Liste aller CSV-Dateien im Verzeichnis
csv_dateien = [f for f in os.listdir(csv_verzeichnis) if f.endswith('.data')]

# Erstellen des Ausgabeordners, falls er nicht vorhanden ist
if not os.path.exists(ausgabe_verzeichnis):
    os.makedirs(ausgabe_verzeichnis)

# Für jede CSV-Datei das Textdokument generieren
for csv_datei in csv_dateien:
    csv_pfad = os.path.join(csv_verzeichnis, csv_datei)
    invoice_text = generate_invoice_txt(csv_pfad)
    
    # Name der TXT-Datei
    txt_datei = f'{os.path.splitext(csv_datei)[0]}.txt'
    
    # Pfad zur TXT-Datei
    txt_pfad = os.path.join(ausgabe_verzeichnis, txt_datei)
    
    # TXT-Datei schreiben
    with open(txt_pfad, 'w') as file:
        file.write(invoice_text)
    
    print(f'{txt_datei} wurde erfolgreich generiert.')