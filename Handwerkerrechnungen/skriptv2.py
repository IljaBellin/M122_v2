import csv
import os
import xml.etree.ElementTree as ET

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


def generate_invoice_xml(csv_file):
    tree = ET.ElementTree()
    root = ET.Element('XML-FSCM-INVOICE-2003A')

    interchange = ET.SubElement(root, 'INTERCHANGE')
    ic_sender = ET.SubElement(interchange, 'IC-SENDER')
    ET.SubElement(ic_sender, 'Pid').text = '41010000001234567'
    ic_receiver = ET.SubElement(interchange, 'IC-RECEIVER')
    ET.SubElement(ic_receiver, 'Pid').text = '41301000000012497'
    ET.SubElement(interchange, 'IR-Ref')

    invoice = ET.SubElement(root, 'INVOICE')
    header = ET.SubElement(invoice, 'HEADER')
    function_flags = ET.SubElement(header, 'FUNCTION-FLAGS')
    ET.SubElement(function_flags, 'Confirmation-Flag')
    ET.SubElement(function_flags, 'Canellation-Flag')

    # Extract data from CSV rows
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        rechnung_nr, auftrag_nr, _, datum, _, _ = rows[0]
        _, _, kundennummer, _, _, _, ust_id, _ = rows[1]

    message_reference = ET.SubElement(header, 'MESSAGE-REFERENCE')
    reference_date = ET.SubElement(message_reference, 'REFERENCE-DATE')
    ET.SubElement(reference_date, 'Reference-No').text = rechnung_nr
    ET.SubElement(reference_date, 'Date').text = datum

    # ... continue building the XML structure

    tree._setroot(root)
    xml_string = ET.tostring(root, encoding='unicode', method='xml')

    return xml_string


# Hauptprogramm

# Verzeichnis, in dem sich die CSV-Dateien befinden
csv_verzeichnis = os.path.join(skript_verzeichnis, 'data')

# Liste aller CSV-Dateien im Verzeichnis
csv_dateien = [f for f in os.listdir(csv_verzeichnis) if f.endswith('.data')]

# Für jede CSV-Datei das Textdokument und die XML-Datei generieren
for csv_datei in csv_dateien:
    csv_pfad = os.path.join(csv_verzeichnis, csv_datei)
    invoice_text = generate_invoice_txt(csv_pfad)
    invoice_xml = generate_invoice_xml(csv_pfad)

    # Name der TXT-Datei
    txt_datei = f'{os.path.splitext(csv_datei)[0]}.txt'
    # Name der XML-Datei
    xml_datei = f'{os.path.splitext(csv_datei)[0]}.xml'

    # Pfad zur TXT-Datei
    txt_pfad = os.path.join(ausgabe_verzeichnis, txt_datei)
    # Pfad zur XML-Datei
    xml_pfad = os.path.join(ausgabe_verzeichnis, xml_datei)

    # TXT-Datei schreiben
    with open(txt_pfad, 'w') as file:
        file.write(invoice_text)
    
    # XML-Datei schreiben
    with open(xml_pfad, 'w') as file:
        file.write(invoice_xml)

    print(f'{txt_datei} und {xml_datei} wurden erfolgreich generiert.')
