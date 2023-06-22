import pandas as pd
import re
import random
from datetime import datetime

# Funktion zum Entfernen von Sonderzeichen und Ersetzen von Umlauten und Akzenten
def normalize_string(s):
    s = re.sub('[^a-zA-Z0-9_.@-]', '', s)
    s = s.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('é', 'e').replace('à', 'a').replace('ç', 'c')
    return s.lower()

# Erstellen der neuen E-Mail-Adressen und Passwörter
email_addresses = []


for index, row in data.iterrows():
    first_name = normalize_string(row['Vorname'])
    last_name = normalize_string(row['Nachname'])
    email = f'{first_name}.{last_name}@edu.tbz.ch'
    email = email if is_valid_email(email) else ''
   
    email_addresses.append(email)
  

output_filename = datetime.now().strftime('%Y-%m-%d_%H-%M') + '_mailimports.csv'
output_data = {'E-Mail-Adresse': email_addresses, 'Passwort': passwords}
output_df = pd.DataFrame(output_data)

# Speichern der Ausgabedatei
output_df.to_csv(output_filename, sep=';', index=False)