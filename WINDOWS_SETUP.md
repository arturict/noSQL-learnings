# MongoDB M165 Project - Installation Guide
# =========================================

## Windows Setup

Dieses Projekt bietet drei verschiedene Setup-Optionen für Windows:

### 1. Command Prompt (CMD) - setup.bat
```cmd
setup.bat
```

### 2. PowerShell - setup.ps1
```powershell
.\setup.ps1
```

### 3. Manual Setup
```cmd
# Umgebungsvariable für die aktuelle Session setzen
set MONGODB_URI=mongodb://192.168.1.157:27017/

# Oder permanent für den Benutzer (als Administrator):
setx MONGODB_URI "mongodb://192.168.1.157:27017/" /M
```

## Voraussetzungen

### Python Installation
1. Python 3.x von https://python.org herunterladen
2. Bei Installation "Add Python to PATH" aktivieren

### Abhängigkeiten installieren
```cmd
pip install -r requirements.txt
```

### MongoDB Server
- MongoDB Server muss auf 192.168.1.157:27017 laufen
- Oder Connection String in den Setup-Dateien anpassen

## Anwendungen starten

Nach dem Setup können folgende Anwendungen gestartet werden:

1. **Environment Demo**: `python environment_demo.py`
2. **Database Explorer**: `python database_explorer.py`
3. **Restaurant CRUD**: `python restaurant_crud.py`
4. **Power Monitor**: `python power_monitor.py`
5. **Power Grapher**: `python power_grapher.py`

## Troubleshooting

### PowerShell Execution Policy
Falls PowerShell-Skript nicht ausgeführt werden kann:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python nicht gefunden
1. Python Installation überprüfen
2. PATH Umgebungsvariable kontrollieren
3. `python --version` in CMD/PowerShell testen

### MongoDB Verbindung
1. MongoDB Server Status prüfen
2. IP-Adresse und Port kontrollieren
3. Firewall-Einstellungen überprüfen

## Cross-Platform Kompatibilität

- **Linux/macOS**: `./setup.sh`
- **Windows CMD**: `setup.bat`
- **Windows PowerShell**: `.\setup.ps1`

Alle Setup-Skripte bieten die gleiche Funktionalität mit plattformspezifischen Anpassungen.
