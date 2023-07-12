import pandas as pd
import re
import random
import os
import shutil
import zipfile
import smtplib
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, date

# alte Dateien verschieben
src_dir = r"C:\Daten\TBZ\Module\M122\email_projekt"
dst_dir = r"C:\Daten\TBZ\Module\M122\email_projekt\ausgaben"
arc_dir = r"C:\Daten\TBZ\Module\M122\email_projekt\mailimport_archive"

for filename in os.listdir(src_dir):
    if "mailimports" in filename:
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(arc_dir, filename)
        shutil.move(src_file, arc_dir)

# Daten Normalisieren 
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

# Passwort Generator
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
data = pd.read_csv(os.path.join(src_dir, 'MOCK_DATA.csv'), delimiter=',')

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
output_df.to_csv(os.path.join(dst_dir, output_filename), sep=';', index=False)

# Briefe für jede E-Mail in der generierten CSV-Datei erstellen
for index, row in data.iterrows():
    first_name = row['Vorname']
    last_name = row['Nachname']
    Strasse = row['Strasse']
    StrNummer = row['StrNummer']
    Ort = row['Ort']
    email = email_addresses[index]
    password = passwords[index]

# Anpassung der Anrede basierend auf dem Geschlecht
    gender = row['Geschl']
    if gender.lower() == 'male':
        salutation = 'Lieber'
    elif gender.lower() == 'female':
        salutation = 'Liebe'
    else:
        salutation = 'Liebes'


# Postleitzahl existiert?
    keine = ""

    Postleitzahl = row['Postleitzahl']
    if not Postleitzahl:
        Postleitzahl = 'keine'
    else:
        Postleitzahl = Postleitzahl



    # Formulieren Sie den Brief
    letter = f"""
    Technische Berufsschule Zürich
    Ausstellungsstrasse 70
    8005 Zürich

    Zürich, den {datetime.now().day}.{datetime.now().month}.{datetime.now().year}

                            {first_name} {last_name}
                            {Strasse} {StrNummer}
                            {Postleitzahl} {Ort}

    {salutation} {first_name}
    Es freut uns, Sie im neuen Schuljahr begrüssen zu dürfen.
    
    Damit Sie am ersten Tag sich in unsere Systeme einloggen
    können, erhalten Sie hier Ihre neue Emailadresse und Ihr
    Initialpasswort, das Sie beim ersten Login wechseln müssen.
    
    Emailadresse:   {email}
    Passwort:       {password}


    Mit freundlichen Grüssen
    
    Ilja Bellin
    TBZ-IT-Service


    admin.it@tbz.ch, Abt. IT: +41 44 446 96 60
    """

    # Erstellen Sie eine neue Datei und schreiben Sie den Brief hinein
    with open(os.path.join(dst_dir, f'{first_name}_{last_name}.brf'), 'w', encoding="utf-8") as f:
        f.write(letter)

print('Die Datei und Briefe wurden erstellt.')

# Archiv Datei

def zip_folder(folder_path, output_path, class_name, last_name):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{timestamp}_newMails_{class_name}_{last_name}.zip"
    output_file = os.path.join(output_path, file_name)

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


folder_to_zip = 'C:/Daten/TBZ/Module/M122/email_projekt/ausgaben'
output_folder = 'C:/Daten/TBZ/Module/M122/email_projekt/'
class_name = 'PE22d'
last_name = 'Bellin'
zip_folder(folder_to_zip, output_folder, class_name, last_name)

#email

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable TLS
        server.login(sender_email, sender_password)
        server.send_message(message)

# server
smtp_server = 'mail.gmx.net'
smtp_port = 587 

# an wen
sender_email = 'rc.hero@gmx.ch'
sender_password = '4evwv3#@LTXQdC3y'
recipient_email = 'ilja.bellin@gmx.ch'
subject = 'Test Email'
body = 'test.'

# schicken
send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body)