from flask import Flask, render_template
import json

app = Flask(__name__)

# Funktion zum Laden der Feiertagsdaten aus der Rohdatendatei
def load_feiertage(data_file):
    with open(data_file, "r") as file:
        data = file.read()
    feiertage = json.loads(data)
    return feiertage

# Funktion zum Formatieren der Feiertagsdaten
def format_feiertage(feiertage):
    formatted_feiertage = []
    for feiertag in feiertage:
        date = feiertag["date"]
        name = feiertag["name"]
        local_name = feiertag["localName"]
        formatted_feiertage.append({
            "Datum": date,
            "Name": name,
            "LokalerName": local_name
        })
    return formatted_feiertage

# Route für die Feiertagsseite
@app.route("/")
def feiertage():
    # Pfad zur Rohdatendatei
    data_file = "rohdaten.txt"

    # Feiertagsdaten laden
    feiertage = load_feiertage(data_file)

    # Feiertagsdaten formatieren
    formatted_feiertage = format_feiertage(feiertage)

    # Feiertagsseite rendern und formatierte Daten übergeben
    return render_template("feiertage.html", feiertage=formatted_feiertage)

if __name__ == "__main__":
    app.run()

