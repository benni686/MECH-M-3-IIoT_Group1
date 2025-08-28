# Abgabe: Industrial IoT – Echtzeitdaten & Analyse

## Einleitung

Im Rahmen dieser Abgabe zeigen Sie Ihr Verständnis für die Kernkonzepte des Industrial IoT, insbesondere die Erfassung, Übertragung, Speicherung und analyse von Sensordaten in Echtzeit, sowie deren Verschlüsselung und Umgang mit Datenversionierung und Zertifikaten. Sie werden einen Raspberry Pi Pico Mikrocontroller verwenden, um Sensordaten zu erfassen, über MQTT an eine zentrale Plattform zu senden und anschließend eine Echtzeitanalyse dieser Daten durchzuführen.

## Aufgabenstellung

Ihre Abgabe besteht aus zwei Hauptkomponenten:

### Raspberry Pi Pico Firmware:

Entwicklung der Software für Ihren Raspberry Pi Pico, die Sensorwerte erfasst und im vorgegebenen JSON-Format über MQTT an den zentralen Broker streamt. Die Firmware soll zudem eine REST-Schnittstelle zur Konfiguration bereitstellen.

### Echtzeitanalyse-Skript:

Entwicklung eines Python-Skripts zur Abfrage der Sensordaten von der zentralen API und Durchführung einer Echtzeitanalyse, inklusive einfacher prädiktiver Elemente oder Anomalieerkennung.

### Ordnerstruktur für die Abgabe

Bitte organisieren Sie Ihre Abgabe in der folgenden Struktur. Dies hilft uns bei der Bewertung und gewährleistet, dass alle notwendigen Dateien vorhanden sind.

```plaintext
.
├── README.md
├── .gitignore                      // Wichtig! Enthält Einträge für .env und config.h
├── esp32_firmware/
│   ├── include/                    // Neuer Ordner für private Header
│   │   └── config.h                // (ignoriert von Git)
│   ├── src/
│   │   ├── main.cpp
│   │   └── sensors/
│   │       └── my_sensor.h
│   ├── platformio.ini              // Liest aus .env und definiert Build-Flags
│   ├── .env                        // Enthält Ihre geheimen Daten (ignoriert von Git)
│   └── .env.example                // Vorlage für die .env-Datei (wird eingecheckt)
├── data_analysis/                      // Ordner für Ihre Datenanalyse-Skripte
│   ├── real_time_analysis.py           // Ihr Haupt-Analyse-Skript
│   ├── requirements.txt                // Python-Pakete, die für Ihr Skript benötigt werden
│   └── analysis_report.ipynb           // (Optional) Jupyter Notebook für detaillierte Analyse/Visualisierung
├── config/                             // Konfigurationsdateien (NICHT mit Git getrackt!)
│   ├── .gitignore                      // Stellt sicher, dass sensible Daten nicht hochgeladen werden
│   └── esp_credentials.env.example         // Beispiel für MQTT-Zugangsdaten, WLAN-SSID/Passwort etc.
└── doc/                                // (Optional) Weitere Dokumentation
    └── architecture_sketch.png         // (Optional) Skizze Ihrer Lösung/Datenflusses
```

## Abgabe-Checkliste

Bitte stellen Sie sicher, dass Sie alle folgenden Punkte in Ihrer Abgabe berücksichtigt haben. Kreuzen Sie die Punkte an, indem Sie [x] verwenden.

1. ESP32-Firmware
[ ] Der ESP32-Firmware-Code befindet sich im Ordner esp32_firmware/.
[ ] Die Firmware erfasst Daten von Ihrem zugewiesenen Sensor in regelmäßigen Intervallen.
[ ] Die Daten werden im vorgegebenen JSON-Format an den zentralen MQTT-Broker gesendet.
Stellen Sie sicher, dass das Datenformat den Anforderungen der zentralen Visualisierungsplattform entspricht.
[ ] Die MQTT-Kommunikation ist mit den bereitgestellten Zertifikaten gesichert.
[ ] Eine REST-Schnittstelle auf dem ESP32 ist implementiert.
[ ] Über die REST-Schnittstelle kann das Sendeintervall des Sensors geändert werden.
[ ] Über die REST-Schnittstelle kann zwischen Datenversionsnummern (falls in Ihrer Aufgabe vorgesehen) gewechselt werden.
[ ] Sensible Informationen (WLAN-Zugangsdaten, MQTT-Anmeldedaten) werden nicht direkt im Code hinterlegt, sondern über eine Konfigurationsdatei oder Umgebungsvariablen geladen. Ein .env.example oder credentials.env.example ist im config/ Ordner oder esp32_firmware/ Ordner vorhanden, das die Struktur dieser Konfigurationsdatei zeigt, aber keine echten Zugangsdaten enthält.
[ ] Der Ordner config/ enthält eine .gitignore-Datei, die sensible Konfigurationsdateien vom Git-Tracking ausschließt.
2. Echtzeitanalyse-Skript
[ ] Ihr Python-Analyse-Skript befindet sich im Ordner data_analysis/ (real_time_analysis.py).
[ ] Das Skript kann Sensordaten über die bereitgestellte API abrufen.
Geben Sie im Skript an, welche API-Endpunkte Sie nutzen.
[ ] Das Skript führt eine Echtzeitanalyse der abgerufenen Daten durch.
[ ] Implementieren Sie mindestens eine der folgenden Funktionen:
Anomalieerkennung (z.B. Schwellenwert-basierend, statistisch).
Einfache prädiktive Analyse (z.B. kurzfristige Vorhersage mittels linearer Regression oder gleitendem Mittelwert).
Mustererkennung oder einfache Zustandsüberwachung.
[ ] Ihr Skript visualisiert die Analyseergebnisse (z.B. mit matplotlib oder seaborn) oder gibt sie in einer aussagekräftigen Textform aus.
[ ] Eine requirements.txt-Datei im Ordner data_analysis/ listet alle benötigten Python-Bibliotheken auf.
[ ] (Optional) Ein Jupyter Notebook (analysis_report.ipynb) zeigt die Schritte Ihrer Analyse und Visualisierung detailliert.
3. Dokumentation & Projektmanagement
[ ] Dieses README.md ist vollständig ausgefüllt und die Checkliste ist entsprechend Ihrer Abgabe aktualisiert.
[ ] (Optional) Kurze Erläuterung (max. 1-2 Absätze) im README.md zu den Design-Entscheidungen Ihrer ESP32-Firmware (z.B. wie Sie mit Fehlern umgehen, warum Sie bestimmte Bibliotheken gewählt haben).
[ ] (Optional) Kurze Erläuterung (max. 1-2 Absätze) im README.md zu den Ansatzpunkten Ihrer Echtzeitanalyse und den erwarteten Ergebnissen.
Hinweise zur Abgabe
Bitte stellen Sie sicher, dass Ihr Code kommentiert und gut lesbar ist.
Testen Sie Ihre Lösung gründlich, bevor Sie sie abgeben.
Bei Fragen oder Problemen nutzen Sie bitte die bereitgestellten Kommunikationskanäle (Forum, Sprechstunde).