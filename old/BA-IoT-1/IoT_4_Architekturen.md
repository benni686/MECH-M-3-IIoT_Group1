---
marp: true
author: Julian Huber
size: 16:9
footer: Internet of Things 1

header: 
theme: lemon 

# Strg+[ ] for Options 

---

<!-- paginate: true -->


# 4 Architekturen für Kommunikationsparadigmen

---

## 🧠 Client-Server-Architektur

- **Client** sendet **Anfangen**
- **Server**: Bearbeitet Anfragen und sendet **Antworten**
- es gibt verschiedene Server für Anwendungsfälle
    - Echo-Server
    - Email-Server
    - Datenbank-Server
    - Web-Server
    - Wert eines Sensors
    - ...

![bg right width:600](images/ClientServer.svg)


---


## Message Broker


- **Producer** sendet **Nachrichten**
- **Message Broker**: Speichert Nachrichten zwischen und vermittelt diese
- **Consumer** erhält **Nachrichten** der von ihm abonnierten Queue
- **Producer** können zu **Consumern** werden und umgekehrt

![bg right width:400](images/0_ubsIB5P8egtyni9g.webp)




---

<center>

![](images/BrokerSequence.svg)

</center>

---


## REST-Interfaces

### 🎯 Lernziele

Nach dieser Einheit sind Sie in der Lage dazu
* die Eingenschaften einer REST-Schnittstelle zu beschreiben
* Teile einer URL zu identifizieren
* Rückgaben eines REST-Befehls zu verarbeiten


---

### Representational State Transfer (REST)

* Client-Server: Dabei stellt der Server einen Dienst bereit, der bei Bedarf vom Client angefragt werden kann. 
* **Zustandslosigkeit:** Jede REST-Nachricht enthält alle Informationen, die für den Server bzw. Client notwendig sind, um die Nachricht zu verstehen. Weder der Server noch die Anwendung soll Zustandsinformationen zwischen zwei Nachrichten speichern. 
* **Adressierbarkeit von Ressourcen**: Jeder REST-konforme Dienst hat eine eindeutige Adresse, den Uniform Resource Locator (URL). Diese „Straße und Hausnummer im Netz“ standardisiert den Zugriffsweg zum Angebot eines Webservices für eine Vielzahl von Anwendungen (Clients).

###### https://de.wikipedia.org/wiki/Representational_State_Transfer

---


#### Websites mittels HTTP (HyperText Transport Protocol)

- PC mit Browser als Client startet Anfrage
- Spezielle Webserver geben Websites als Antwort auf einen GET-Befehl
- Antwort ist eine HTML-Datei (spezielle Zeichenkette vergleichbar JSON)

<center>

![height:400](images/MCIweb.png)

</center>


---

#### HTTP (HyperText Transport Protocol)

- Protokoll auf Anwendungsschicht mit dem Webserver und Browser kommunizieren
- Immer die gleiche Abfolge
    - Request dann Response

```Python
# Paket mit dem Python wie ein Browser agieren kann
import requests

# Request an Server mit MCI-Website
response = requests.get('https://www.mci.edu/de/')

# HTML Status
print(response.status_code) # 200 - heiß alles OK

print(response.headers['content-type']) # text/html; charset=utf-8 # Also ein HTML-Dokument

print(response.text) # <!doctype html> <html lang="de" class="no-js"> 	<head> ...
```

---

#### 🤓 HTTP Status Codes

| Fehlercode |                        | Beispiel                          |
|------------|------------------------|-----------------------------------|
| 1xx        | Informationen          | 102 - Zeitintensive Anfrage läuft |
| 2xx        | Erfolgreiche Operation | 200 - OK                          |
| 3xx        | Umleitung              | 308 - Permanente Umleitung        |
| 4xx        | Client-Fehler          | 404 - Anfrage nicht gefunden      |
| 5xx        | Server-Fehler          | 503 - Überlastung                 |
| 9xx        | Proprietäre Fehler     |                                   |

[Vollständige Liste mit Codes](https://de.wikipedia.org/wiki/HTTP-Statuscode)


---

### REST-Schnittstelle

![bg h:500 right](images/osi.png)

* Auf Anwendungsschicht im OSI-Modell
* Ansprache einer bestimmten Schnittstelle über die URL
* `https:<ip/url>:<port>/<name_der_schnittstelle>?<daten_an_die_schnittstelle>`
* Wie __Funktionen__ geben **Schnittstellen** (meist) etwas zurück und stellen einen von außen erreichbaren **Service** bereit


---

#### Adressierung über URL

* Uniform Resource Locator
* identifiziert und lokalisiert eine Ressource, beispielsweise eine Webseite, über die zu verwendende Zugriffsmethode (zum Beispiel das verwendete Netzwerkprotokoll wie HTTP oder FTP) 

`<scheme>:<scheme-specific-part>`

```
      |-------------------- Schema-spezifischer Teil ----------------------|
      |                                                                    |
https://maxmuster:geheim@www.example.com:8080/index.html?p1=A&p2=B#ressource
\___/   \_______/ \____/ \_____________/ \__/\_________/ \_______/ \_______/
  |         |       |           |         |       |          |         |
Schema Benutzer Kennwort      Host      Port    Pfad      Query    Fragment
```
---

#### GET

* Fordert die angegebene Ressource vom Server an 
* GET weist keine Nebeneffekte auf. Der Zustand am Server wird nicht verändert, weshalb GET als sicher bezeichnet wird.
* Rückgabe kann eine JSON sein

```Python
# Paket mit dem Python wie ein Browser agieren kann
import requests

# Request an Server mit MCI-Website
response = requests.get(url = 'http://api.citybik.es/v2/networks/stadtrad-innsbruck')
# > {"network":{"company":["Nextbike GmbH"],"href":"/v2/networks/stadtrad-innsbruck","id":"stadtrad-innsbruck"," <...>
```

---

#### POST

* Fügt eine neue (Sub-)Ressource unterhalb der angegebenen Ressource ein. Da die neue Ressource noch keinen URI besitzt, adressiert der URI die übergeordnete Ressource. Als Ergebnis wird der neue Ressourcenlink dem Client zurückgegeben. 

```Python
my_data = """{
  "contact": {
      "id": "1",
      "firstName": "Julian",
      "lastName": "Huber"
    }
}"""

response = requests.post(url = 'https://3d3m9.mocklab.io/v1/contacts', data = my_data)

response.text
# > Created a new contact!
```


---

### Response Object

- text/json: Antwort auf die Anfrage
- status_code: Erfolgsbestätigung oder Fehlernummer
- encoding: Codierung der Antwort (UTF, ASCII, ...)


###### https://www.w3schools.com/python/ref_requests_response.asp

---

### ✍️ Aufgabe: 

* Wie viele freie Räder gibt es in der Höttinger Au /West?
* Nutzen Sie den folgenden [Flow](flows\4\Beispiel_4_1_1.json), um die REST-API abzufragen
```JSON
[
    {
        "id": "6ceec8886e628181",
        "type": "inject",
        "z": "60b580c694dab5d7",
        "name": "",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 280,
        "y": 240,
        "wires": [
            [
                "1ff324762314b4a8"
            ]
        ]
    },
    {
        "id": "1ff324762314b4a8",
        "type": "http request",
        "z": "60b580c694dab5d7",
        "name": "",
        "method": "GET",
        "ret": "txt",
        "paytoqs": "ignore",
        "url": "http://api.citybik.es/v2/networks/stadtrad-innsbruck",
        "tls": "",
        "persist": false,
        "proxy": "",
        "insecureHTTPParser": false,
        "authType": "",
        "senderr": false,
        "headers": [],
        "x": 530,
        "y": 240,
        "wires": [
            [
                "ddd577abecebf1ba"
            ]
        ]
    },
    {
        "id": "ddd577abecebf1ba",
        "type": "debug",
        "z": "60b580c694dab5d7",
        "name": "Netzwerk Innsbruck",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 870,
        "y": 240,
        "wires": []
    },
    {
        "id": "e8fee1f485da561a",
        "type": "comment",
        "z": "60b580c694dab5d7",
        "name": "Anfrage an Netzwerk Innsbruck",
        "info": "",
        "x": 350,
        "y": 160,
        "wires": []
    }
]
```

---

* Ändern Sie die Rückgabe des HTTP-Requests in ein JSON-Objekt
* Schreiben Sie eine Funktion, die die Anzahl der freien Räder in der Höttinger Au /West oder einem Ort Ihrer Wahl zurückgibt
* Optional können Sie diese auch auf einer [Karte](https://flows.nodered.org/node/node-red-contrib-maps) anzeigen


---


### [Alternativen zu HTTP](https://nourhan-m-s-youssef.medium.com/web-service-apis-rest-soap-vs-websocket-api-55697cc9fa1c)

- Simple Objects Access Protocol (SOAP)
  - SOAP API analog zu REST (Anfrage und Antwort)
  - Austausch immer als XML-Format (bei REST offen)
- Web Sockets
  - bidirektional
  - echtzeitfähig

![bg right](images/1_tUl17TzyAAkQQ3xrFVdD4g.webp)


---

### Anwendungsbeispiele

<center>

![](images/Offene_Schnittstellen_ChargePilot_c_The_Mobility_House.webp)

</center>


###### https://www.mobilityhouse.com/de_de/magazin/e-mobility/offene-schnittstellen-rest-api-wenn-die-cloud-mit-dem-elektroauto-spricht.html


---

### Anwendungsbeispiele

* SPS mit [REST-APIs](https://www.beckhoff.com/de-at/produkte/automation/twincat/tfxxxx-twincat-3-functions/tf6xxx-tc3-connectivity/tf6760.html)
* List of [Open-Rest-APIs](https://github.com/public-apis/public-apis)

---


## Message Broker am Beispiel MQTT

### 🎯 Lernziele

Nach dieser Einheit sind Sie in der Lage dazu
* Die Funktion von Message Broken zu beschreiben

---

### Herausforderungen Rest

* REST ist für ein Client-Server-Paar optimiert
* REST-Anfragen gehen immer von Client aus und müssen von diesem explizit angestoßen werden
* Es die Übertragung gestört werden nicht-erfolgreiche Anfragen nicht nachgeholt
* zunehmend sind mehrere Systeme vernetzt

![bg right:33% width:400](images/ClientServer.svg)

---

### Message Broker

<center>

![](images/1_vDE8StT8wJQL46yL4LWMww.png)

</center>


###### https://medium.com/@jaydev.dave93/what-is-mqtt-protocol-c6a0cafffa8c

---

### MQTT

* offenes Netzwerkprotokoll für Machine-to-Machine-Kommunikation 
* leichtgewichtig und häufig für IoT Sensoren 
* Viele weitere [Alternativen](https://en.wikipedia.org/wiki/Message_broker): Apache Kafka, etc.

![bg right:33% w:300](images/mqtt-logo.png)

---


* Zentrale Instanz (Server), welche Nachrichten verteilt
* Mehrere Akteure können sich als Clients verbinden
* Producer sind Clients, welche Nachrichten erzeugen
* Consumer sind Clients, die Nachrichten abrufen

![bg right:33% w:400](images/1_vDE8StT8wJQL46yL4LWMww.png)


###### https://medium.com/@jaydev.dave93/what-is-mqtt-protocol-c6a0cafffa8c

---

#### Nachrichten


* Beliebige Bitfolgen
  * für uns: UTF-codierte Texte im JSON-Format 
* topic: thematische Zuordnung (Liste der Empfänger)
  * Struktur ähnlich Dateisystem
  * Hierarchie-Ebenen mit `/` getrennt
* payload: Inhalt der Nachricht (Text einer Email)
* Entsprechend werden diese auch von `node-red` verarbeitet
```JSON
{
  "topic" : "building_1/smart_meter/messwerte",
  "payload" : {
    "energy_consumption" : 600,
    "unit" : "W"
    }
}
```

---

#### Producer

* Definieren Verbindung zu einem Broker/Server über URL
* veröffentlichen Nachrichten zu einem Topic
* Push-Prinzip: Producer legen selbst, wann sie eine Nachricht veröffentlichen
* z.B. eine Smarte Steckdose die Messwerte

![bg right](images/shelly_mqtt.png)

---

#### Consumer

* Definieren Verbindung zu einem Broker/Server über URL
* Empfangen alle Nachrichten zu von ihnen definierten Topics

![bg right w:600](images/node-red-mqtt-publish-config-1.jpg)

###### http://stevesnoderedguide.com/configuring-the-mqtt-publish-node

---

### MQTT-Wildcards

* Möchte man mehr als ein Topic erhalten
  ```
  building_1/smart_meter/messwerte
  building_2/smart_meter/messwerte
  building_1/raum_1/temperatur
  building_1/raum_2/temperatur
  building_2/raum_1/temperatur
  building_2/raum_2/temperatur
  ```
* Single Level: Temperatur in allen Räumen von Gebäude 1
  ```  building_1/+/temperatur  ```
* Multi Level: Alles zu Gebäude 1
  ```  building_1/#  ```


---

### Hosting von MQTT-Brokern

* Zentraler Anlaufpunkt
* Konfiguration von Sicherheitseinstellungen
  * Username und Passwort der Clienten
  * Asymmetrische Verschlüsselung
* Definiert durch IP und Port
* Fremd gehostet in der Could z.B. mit [hivemq](https://console.hivemq.cloud/)
* Selbst gehostet z.B. mit [Mosquitto](https://mosquitto.org/) z.B. auch lokal auf einer Soft-SPS

![bg right w:600](images/MQTT_hive.png)

###### https://console.hivemq.cloud/

---

### Quality of Service (QoS)

* **QoS 0:** *'Fire and Forget'*
* **QoS 1:** Mindestens ein zweites Senden nach Time-out (Duplikate möglich!) 
* **QoS 2:** Sicherste Möglichkeit, jedoch hoher Overhead

![bg right w:600](images/MQTT_QoS_mobile.jpg)

###### https://www.techtarget.com/iotagenda/definition/MQTT-MQ-Telemetry-Transport

---

### Retain Flag

* Einzelne Nachrichten können mit Flag versehen werden
* Der Broker speichert die letzte Nachricht des Topics
* zum Überschreibe: leere Message

![h:200](images/1_BGq8wqT3PeBng84v2csOkg.webp)

* Neue Subscriber bekommen mit, wann die letzte Nachricht kam (z.B. bei seltenen Ereignissen (z.B. Fensterkontakte))
* Beschreibung eines Topics soll dokumentiert werden (z.B. `building_1/smart_meter/messwerte/$unit`)

###### https://emqx.medium.com/mqtt-5-0-features-retain-message-104698b070d1

---

#### Beispiel `node-red`

![bg right h:500](images/QoS__Retain_example.png)

* für einzelne `msg` kann man die ```QoS``` und ```Retain```-Einstellungen setzen
  * `msg.qos = 1`
  * `msg.retain = true`
* Zudem kann man für eine MQTT-Verbindung die Einstellungen und das Verhalten bei Verbindungsabbruch setzen

