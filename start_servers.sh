#!/bin/bash

# Überprüft, ob mindestens zwei Argumente übergeben wurden
if [ "$#" -lt 2 ]; then
    echo "Fehler: Zu wenige Argumente. Benutzung: $0 <Basisname> <Anzahl der Server>"
    exit 1
fi

# Nimmt den Basisnamen und die Anzahl der Server von den Befehlszeilenargumenten
baseServerName=$1
serverCount=$2

# Definiert Start- und Endport
startPort=27015
endPort=27050 # Stellen Sie sicher, dass dieser Wert den Startport und die mögliche Anzahl von Servern berücksichtigt

# Pfad zur ausführbaren Datei des Spiels
gameExecutable="$HOME/serverfiles/game/bin/linuxsteamrt64/cs2"

# Schleife zum Starten der geforderten Anzahl von Spielservers
for (( i=0; i<serverCount; i++ ))
do
    port=$((startPort + i))
    if (( port > endPort )); then
        echo "Maximale Portanzahl erreicht, kann keine weiteren Server starten."
        break
    fi

    # Generiert den Servernamen basierend auf dem eingegebenen Basisnamen und fügt die Nummer hinzu
    serverName="${baseServerName}_${i}"
    echo "Starte Server: $serverName auf Port $port..."

    # Führt den Befehl zum Starten des Servers aus
    $gameExecutable -dedicated -ip 0.0.0.0 -port $port +servername "$serverName" &
    sleep 1 # Kurze Pause, um dem Server Zeit zum Starten zu geben
done

echo "$i Server(s) gestartet unter Basisnamen $baseServerName."
