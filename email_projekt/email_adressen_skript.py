import pandas as pd
import re
import random
from datetime import datetime

# Funktion zum Entfernen von Sonderzeichen und Ersetzen von Umlauten und Akzenten
#def normalize_string(s):
  #  s = s.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('é', 'e').replace('è', 'e').replace('ë', 'e').replace('à', 'a').replace('á', 'a').replace('ç', 'c').replace('ì', 'i')
 #   return s.lower()


def normalize_string(s):
    replacements = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'é': 'e',
        'è': 'e',
        'ë': 'e',
        'à': 'a',
        'á': 'a',
        'ç': 'c',
        'ì': 'i',
        'ï': 'i',
        'ò': 'o',
        'ó': 'o',
        'å': 'a',
        'ú': 'u',
        'ù': 'u',
        'ô': 'o',
        'ê': 'e',
        'î': 'i',
        'û': 'u',
        'ÿ': 'y',
        'ñ': 'n',
        'ß': 'ss',
        'æ': 'ae',
        'œ': 'oe',
        'Æ': 'AE',
        'Œ': 'OE',
        'Ø': 'O',
        'ø': 'o',
        'Å': 'A',
        'Û': 'U',
        'Ï': 'I',
        'Í': 'I',
        'É': 'E',
        'Á': 'A',
        'È': 'E',
        'Â': 'A',
        'Ú': 'U',
        'Ò': 'O',
        'Ì': 'I',
        'Ç': 'C',
        'Ñ': 'N',
        'Ê': 'E',
        'Ô': 'O',
        'Î': 'I',
        'Ý': 'Y',
        'Ù': 'U',
        'Ä': 'A',
        'Ö': 'O',
        'Ü': 'U',
        'Ÿ': 'Y'
    }
    for char, replacement in replacements.items():
        s = s.replace(char, replacement)
    return s.lower()


# Funktion zum Generieren eines zufälligen Passworts
def generate_password():
    # Hier können Sie die Anforderungen an das Passwort anpassen
    allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password_length = 8
    password = ''.join(random.choice(allowed_characters) for _ in range(password_length))
    return password

# Funktion zum Überprüfen einer E-Mail-Adresse
def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

# Laden der Daten aus der CSV-Datei
data = pd.read_csv('MOCK_DATA.csv', delimiter=',')

# Erstellen der neuen E-Mail-Adressen und Passwörter
email_addresses = []
passwords = []

for index, row in data.iterrows():
    first_name = normalize_string(row['Vorname'])
    last_name = normalize_string(row['Nachname'])
    email = f'{first_name}.{last_name}@edu.tbz.ch'
    email = email if is_valid_email(email) else ''
    password = generate_password()
    email_addresses.append(email)
    passwords.append(password)

# Erstellen der Ausgabedatei
output_filename = datetime.now().strftime('%Y-%m-%d_%H-%M') + '_mailimports.csv'
output_data = {'E-Mail-Adresse': email_addresses, 'Passwort': passwords}
output_df = pd.DataFrame(output_data)

# Speichern der Ausgabedatei
output_df.to_csv(output_filename, sep=';', index=False)

print('Die Datei', output_filename, 'wurde erfolgreich erstellt.')
