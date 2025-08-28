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


# Aufgaben 7: SQL



## 🏆 P12: SQLite Tabelle anlegen (4pkt)

- Nutzen Sie Ihre Relations-Tabellen (aus 🏆 P10), um die benötigten Tabellen mittels SQL-Statement anzulegen. Die können Sie direkt in [DB Browser for SQLite](https://sqlitebrowser.org/) oder über einen node-red Flow vornehmen
- Nutzen Sie die [SQLite Dokumentation](https://www.sqlite.org/docs.html)
- Deklarieren Sie auch die Schlüsselattribute und die Fremdschlüsselbeziehungen
- Legen Sie die Tabellen in einer Datenbank `prozessdaten.db` an und geben Sie diese ab

---

## 🏆 P13: SQLite Werte Speichern (10pkt)

- Befüllen Sie eine Datenbank `prozessdaten.db`  
- Legen Sie dazu die geeigneten [SQLite nodes](https://mpolinowski.github.io/docs/IoT-and-Machine-Learning/Home_Automation/2018-11-12--nodered-sqlite/2018-11-12/) in Node-red an.
- Folgende Tabellen sollen befüllt werden:
  - `BOTTLE`, `DISPENSER`, `DROPVIBRATION`, `FILLLEVEL`, `RECIPE`, `TEMPERATURE`, `FILLSBOTTLE`
- Integrieren Sie automatischen Bestellungen und Bestellbestätigungen in die Datenbank!
 - Speichern sie Ihre Datenbank `prozessdaten.db` nachdem einige Daten in der Datenbank gespeichert wurden
 - Laden Sie Ihren flow `database_flow.json` als Ergebnis hoch
---

## Erstellen des aktuellen Datums und Uhrzeit:

```javascript
// als Strings mit Ortszeit

var currentDate = new Date();

var date = currentDate.toLocaleDateString();

var time = currentDate.toLocaleTimeString();

 

// als Int in Unix-Time

var currentDate = Date.now();
```

---

## Weiterführende Literatur & Ressourcen 

Die folgenden Ressourcen sind für diese Woche relevant:

- [DB Browser for SQLite](https://sqlitebrowser.org/) erlaubt es SQLite Datenbanken zu öffnen und grafisch, so wie mit SQL-Befehlen zu editieren
- ggf. bietet es sich auch an manuell SQL-Befehle und in die Datenbank einzügen, anstelle node-red zu verwenden, wenn es sich um einmalige Befehle handelt
- Sofern node-red mit sehr hohen Frequenzen arbeitet, kann es dazu kommen, dass DB Browser for SQLite abstürzt, in diesem Fall bietet es sich an eine Kopie der Datenbank  anzulegen und diese mit dem DB Browser zu öffnen

---

## Beispiel Flows

```JSON
[
    {
        "id": "6024655be18e42e7",
        "type": "sqlite",
        "z": "723f736d83e11b08",
        "mydb": "a658782dc71b9e66",
        "sqlquery": "msg.topic",
        "sql": "",
        "name": "",
        "x": 950,
        "y": 260,
        "wires": [
            [
                "2482e43d14c62155"
            ]
        ]
    },
    {
        "id": "2482e43d14c62155",
        "type": "debug",
        "z": "723f736d83e11b08",
        "name": "debug 25",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "false",
        "statusVal": "",
        "statusType": "auto",
        "x": 1240,
        "y": 260,
        "wires": []
    },
    {
        "id": "28df9585f5062b76",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "INSERT",
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
        "topic": "INSERT INTO dhtreadings(temperature, humidity, currentdate, currenttime, device) values(22.4, 48, date('now'), time('now'), 'manual')",
        "payload": "",
        "payloadType": "date",
        "x": 320,
        "y": 460,
        "wires": [
            [
                "832b6a173c5a9d64"
            ]
        ]
    },
    {
        "id": "ab8e0d0cea3a6ac8",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "SELECT",
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
        "topic": "SELECT * FROM dhtreadings",
        "payload": "",
        "payloadType": "date",
        "x": 340,
        "y": 540,
        "wires": [
            [
                "6024655be18e42e7"
            ]
        ]
    },
    {
        "id": "2cc76842180a7217",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "DELETE",
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
        "topic": "DELETE from dhtreadings",
        "payload": "",
        "payloadType": "date",
        "x": 340,
        "y": 620,
        "wires": [
            [
                "6024655be18e42e7"
            ]
        ]
    },
    {
        "id": "cacff1be2a55fa87",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "DROP",
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
        "topic": "DROP TABLE wiegevorgang",
        "payload": "",
        "payloadType": "date",
        "x": 330,
        "y": 700,
        "wires": [
            [
                "6024655be18e42e7"
            ]
        ]
    },
    {
        "id": "032ee50ce191c7f1",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "VIEW RECORD",
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
        "topic": "SELECT * FROM dhtreadings",
        "payload": "",
        "payloadType": "date",
        "x": 380,
        "y": 820,
        "wires": [
            [
                "a980b7389ecdf535"
            ]
        ]
    },
    {
        "id": "a980b7389ecdf535",
        "type": "sqlite",
        "z": "723f736d83e11b08",
        "mydb": "a658782dc71b9e66",
        "sqlquery": "msg.topic",
        "sql": "",
        "name": "",
        "x": 650,
        "y": 820,
        "wires": [
            [
                "d7a5158676939ec2",
                "f764c63551b2b415"
            ]
        ]
    },
    {
        "id": "d7a5158676939ec2",
        "type": "ui_template",
        "z": "723f736d83e11b08",
        "group": "fbbb0e3ff7aee22c",
        "name": "",
        "order": 1,
        "width": 0,
        "height": 0,
        "format": "<table style='width:100%'>\n    <tr>\n        <th>Time</th>\n        <th>Temp</th>\n        <th>Hum</th>\n    </tr>\n    <tr ng-repeat='x in msg.payload | limitTo:2'>\n        <td>{{msg.payload[$index].currenttime}}</td>\n        <td>{{msg.payload[$index].temperature}}</td>\n        <td>{{msg.payload[$index].humidity}}</td>\n    </tr>\n</table>",
        "storeOutMessages": true,
        "fwdInMessages": true,
        "resendOnRefresh": true,
        "templateScope": "local",
        "x": 960,
        "y": 740,
        "wires": [
            []
        ]
    },
    {
        "id": "f764c63551b2b415",
        "type": "debug",
        "z": "723f736d83e11b08",
        "name": "debug 53",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "false",
        "statusVal": "",
        "statusType": "auto",
        "x": 940,
        "y": 860,
        "wires": []
    },
    {
        "id": "832b6a173c5a9d64",
        "type": "function",
        "z": "723f736d83e11b08",
        "name": "Create SQL-String",
        "func": "// If You have a Payload that is a JSON\nmsg.payload = {\"Temp\" : 22.5, \"Humidity\" : 50}\n\n// You can build a string using ${} as placeholders\nmsg.topic = `INSERT INTO dhtreadings(temperature, humidity, currentdate, currenttime, device) values(${msg.payload.Temp}, ${msg.payload.Humidity}, date('now'), time('now'), 'manual')`\n\n// Note that the databse node after this node takes the topic and plugs it in as the SQL-Statement\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 790,
        "y": 480,
        "wires": [
            [
                "6024655be18e42e7"
            ]
        ]
    },
    {
        "id": "bf1b6cb14a14a8cb",
        "type": "comment",
        "z": "723f736d83e11b08",
        "name": "Tabellen für Aufgabe",
        "info": "",
        "x": 350,
        "y": 20,
        "wires": []
    },
    {
        "id": "dbffe699a2305d6f",
        "type": "comment",
        "z": "723f736d83e11b08",
        "name": "Beispieltabellen und DB Managemet",
        "info": "",
        "x": 400,
        "y": 340,
        "wires": []
    },
    {
        "id": "7234279674f8535d",
        "type": "comment",
        "z": "723f736d83e11b08",
        "name": "Datenabfrage",
        "info": "",
        "x": 330,
        "y": 760,
        "wires": []
    },
    {
        "id": "a21d7bd582abf98c",
        "type": "inject",
        "z": "723f736d83e11b08",
        "name": "CREATE dhtreadings",
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
        "once": true,
        "onceDelay": 0.1,
        "topic": "CREATE TABLE dhtreadings(id INTEGER PRIMARY KEY AUTOINCREMENT, temperature NUMERIC, humidity NUMERIC, currentdate DATE, currenttime TIME, device TEXT)",
        "payload": "",
        "payloadType": "date",
        "x": 360,
        "y": 400,
        "wires": [
            [
                "6024655be18e42e7"
            ]
        ]
    },
    {
        "id": "a658782dc71b9e66",
        "type": "sqlitedb",
        "db": "C:\\code\\node-red\\sql.db",
        "mode": "RWC"
    },
    {
        "id": "fbbb0e3ff7aee22c",
        "type": "ui_group",
        "name": "Standard",
        "tab": "6552b14fe0a7d180",
        "order": 1,
        "disp": true,
        "width": "6",
        "collapse": false
    },
    {
        "id": "6552b14fe0a7d180",
        "type": "ui_tab",
        "name": "Thema3",
        "icon": "dashboard",
        "order": 2,
        "disabled": false,
        "hidden": false
    }
]
```
