#!/bin/bash

# API-URL für die Schweizer Feiertage
api_url="https://date.nager.at/api/v3/NextPublicHolidays/CH"

# Verzeichnis für die Rohdaten
data_dir="/home/mario/m122/projekte/ProjektF"

# Rohdatendatei
data_file="$data_dir/rohdaten.txt"

# API-Aufruf und Speichern der Antwort in der Rohdatendatei
curl -s "$api_url" > "$data_file"

