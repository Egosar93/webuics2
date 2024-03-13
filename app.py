from flask import Flask, render_template, request, redirect, url_for
import subprocess
import socket

app = Flask(__name__)

# Beispielhafte Serverkonfiguration
servers = [
    {'name': 'Server 1', 'port': 27015},
    {'name': 'Server 2', 'port': 27016},
    # Fügen Sie hier zusätzliche Server mit ihren entsprechenden Ports hinzu
]

def is_server_online(port):
    """Überprüft, ob ein Server online ist, indem versucht wird, eine Socket-Verbindung herzustellen."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Timeout, um die Überprüfung zu beschleunigen
            result = sock.connect_ex(('127.0.0.1', port))
            return result == 0
    except socket.error as e:
        print(f"Fehler beim Überprüfen des Ports {port}: {e}")
        return False

@app.route('/')
def index():
    """Zeigt das Hauptformular zum Starten und Stoppen der Server und eine Liste der Server mit ihrem Status an."""
    for server in servers:
        server['online'] = is_server_online(server['port'])
    return render_template('index.html', servers=servers)

@app.route('/start_server', methods=['POST'])
def start_server():
    """Startet Server basierend auf den Benutzereingaben."""
    server_name = request.form['serverName']
    server_count = request.form['serverCount']
    script_path = '$HOME/web/start_servers.sh'  # Pfad zum Start-Skript anpassen

    try:
        subprocess.run([script_path, server_name, server_count], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Starten der Server: {e}")

    return redirect(url_for('index'))

@app.route('/stop_server', methods=['POST'])
def stop_server():
    """Stoppt einen Server basierend auf dem angegebenen Port."""
    port = request.form['serverPort']
    script_path = '"$HOME/web/stop_server_by_port.sh"'  # Pfad zum Stop-Skript anpassen

    try:
        subprocess.run([script_path, port], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Stoppen des Servers auf Port {port}: {e}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
