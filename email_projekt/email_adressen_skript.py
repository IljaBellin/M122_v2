import pandas as pd
import re
import random
import os
import shutil
from datetime import datetime
import zipfile


# alte datei verscheiben

src_dir = r"C:\Daten\TBZ\Module\M122\email_projekt"
dst_dir = r"C:\Daten\TBZ\Module\M122\email_projekt\mailimport_archive"

for filename in os.listdir(src_dir):
    if "mailimports" in filename:
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        shutil.move(src_file, dst_file)
        print('alte Datein verschoben')

# Daten Normalisieren 


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
        'Ä': 'Ae',
        'Ö': 'Oe',
        'Ü': 'Ue',
        'Ÿ': 'Y'
    }
    for char, replacement in replacements.items():
        s = s.replace(char, replacement)
    
    #lowercase
    return s.lower()


# Passwort generator
def generate_password():
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

print('datei wurde erstellt')




# Archiv Datei


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

folder_to_zip = 'C:/Daten/TBZ/Module/M122/email_projekt/ausgaben'
output_zip_file = 'C:/Daten/TBZ/Module/M122/email_projekt/ausgaben'
zip_folder(folder_to_zip, output_zip_file)




