#!/bin/bash

# Überprüfen, ob ein Argument übergeben wurde
if [ "$#" -ne 1 ]; then
    echo "Fehler: Genau ein Argument erforderlich. Benutzung: $0 <Port>"
    exit 1
fi

PORT=$1

# Findet den Prozess, der den angegebenen Port nutzt
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    kill $PID && echo "Server auf Port ${PORT} gestoppt."
else
    echo "Kein Prozess auf Port ${PORT} gefunden."
fi
