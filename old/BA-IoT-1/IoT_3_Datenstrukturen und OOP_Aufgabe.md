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

# Aufgaben 2: Use Case Entwicklung

---

## 🏆 P4: Erzeugen Sie ein Klassendiagramm welches den folgenden Sachverhalt abbildet  (6pkt)

- Eine Abfüllanlage besteht aus bis zu drei Pellet Dispensern und einer Waage. Jeder der Pellet Dispenser hat einen Füllstand und kann eine Menge an Pellets abfüllen. Abgefüllt wird in Flaschen, welche jeweils einem Rezept (drei verschiedene Gewichte bei jedem Dispenser) zugeordnet sind. Jeder Falsche kann an der Wage ein Endgewicht und ein Abschlusszeitpunkt zugeordnet werden.
- Zu jedem Pellet Dispenser gibt es einen Überwachungsservice, der den aktuellen Füllstand überprüft und abhängig von einem Mindestfüllstand eine Nachfüllaufforderung ausführen kann.
- Zudem gibt es einen Qualitäts-Überprüfungs-Service, der für jede Flasche das Gewicht überprüft und ab einer gewissen Abweichung (als Attribut setzbar) eine Warnmeldung geben kann.

---

### Der folgende Flow [3.1.1](flows\3\Beispiel_3_1_1.json) simuliert diesen Prozess

- Nutzen Sie diesen, um die folgenden beiden Aufgaben zu erfüllen

```
[
    {
        "id": "298a25d26e5be7ee",
        "type": "tab",
        "label": "IoT 3_1_1 DataSimulator",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "a0b9e936b2f2b5d0",
        "type": "mqtt in",
        "z": "298a25d26e5be7ee",
        "name": "",
        "topic": "iot1/teaching_factory/#",
        "qos": "2",
        "datatype": "auto-detect",
        "broker": "5ccc439f00914349",
        "nl": false,
        "rap": true,
        "rh": 0,
        "inputs": 0,
        "x": 240,
        "y": 140,
        "wires": [
            [
                "eded6429e6babaa0"
            ]
        ]
    },
    {
        "id": "4f06c8d570eecc18",
        "type": "debug",
        "z": "298a25d26e5be7ee",
        "name": "green",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 790,
        "y": 160,
        "wires": []
    },
    {
        "id": "eded6429e6babaa0",
        "type": "switch",
        "z": "298a25d26e5be7ee",
        "name": "",
        "property": "topic",
        "propertyType": "msg",
        "rules": [
            {
                "t": "eq",
                "v": "iot1/teaching_factory/dispenser_green",
                "vt": "str"
            },
            {
                "t": "eq",
                "v": "iot1/teaching_factory/dispenser_blue",
                "vt": "str"
            },
            {
                "t": "eq",
                "v": "iot1/teaching_factory/dispenser_red",
                "vt": "str"
            },
            {
                "t": "eq",
                "v": "iot1/teaching_factory/scale/final_weight",
                "vt": "str"
            }
        ],
        "checkall": "true",
        "repair": false,
        "outputs": 4,
        "x": 490,
        "y": 260,
        "wires": [
            [
                "4f06c8d570eecc18"
            ],
            [
                "790a276b805751d2"
            ],
            [
                "be55fb6476e39a3d"
            ],
            [
                "284ebfc028448b13"
            ]
        ]
    },
    {
        "id": "790a276b805751d2",
        "type": "debug",
        "z": "298a25d26e5be7ee",
        "name": "blue",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 790,
        "y": 200,
        "wires": []
    },
    {
        "id": "be55fb6476e39a3d",
        "type": "debug",
        "z": "298a25d26e5be7ee",
        "name": "red",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 790,
        "y": 240,
        "wires": []
    },
    {
        "id": "284ebfc028448b13",
        "type": "debug",
        "z": "298a25d26e5be7ee",
        "name": "scale",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 790,
        "y": 340,
        "wires": []
    },
    {
        "id": "a3efe667ee365c5b",
        "type": "comment",
        "z": "298a25d26e5be7ee",
        "name": "Collects Data from MQTT",
        "info": "",
        "x": 250,
        "y": 60,
        "wires": []
    },
    {
        "id": "f332c659bf5cd22a",
        "type": "comment",
        "z": "298a25d26e5be7ee",
        "name": "Sorts by Topic",
        "info": "",
        "x": 490,
        "y": 60,
        "wires": []
    },
    {
        "id": "17fa5c2a2be952f0",
        "type": "comment",
        "z": "298a25d26e5be7ee",
        "name": "Dispensers",
        "info": "",
        "x": 800,
        "y": 100,
        "wires": []
    },
    {
        "id": "cd2a2b2f14b02c86",
        "type": "comment",
        "z": "298a25d26e5be7ee",
        "name": "Scale",
        "info": "",
        "x": 790,
        "y": 300,
        "wires": []
    },
    {
        "id": "5ccc439f00914349",
        "type": "mqtt-broker",
        "name": "oracle_docker",
        "broker": "158.180.44.197",
        "port": "1883",
        "clientid": "",
        "autoConnect": true,
        "usetls": false,
        "protocolVersion": "4",
        "keepalive": "60",
        "cleansession": true,
        "birthTopic": "",
        "birthQos": "0",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willPayload": "",
        "willMsg": {},
        "userProps": "",
        "sessionExpiry": ""
    }
]
```

---

### Der folgende Flow [3.1.2](flows\3\Beispiel_3_1_2.json) bietet einige Beispiele als Hilfestellung

```
[
    {
        "id": "95f4f9117035b03c",
        "type": "tab",
        "label": "IoT 3_1_2 Hilfestellung",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "e3271ec2c02103c4",
        "type": "inject",
        "z": "95f4f9117035b03c",
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
        "payload": "42.3333",
        "payloadType": "num",
        "x": 360,
        "y": 200,
        "wires": [
            [
                "5e8962e43e803749"
            ]
        ]
    },
    {
        "id": "b01bba3705ecfe36",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Kommastellen anpassen",
        "info": "",
        "x": 390,
        "y": 140,
        "wires": []
    },
    {
        "id": "5e8962e43e803749",
        "type": "function",
        "z": "95f4f9117035b03c",
        "name": "auf 2 Nachkommastellen",
        "func": "msg.payload = msg.payload.toFixed(2)\n\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 610,
        "y": 200,
        "wires": [
            [
                "298188c9def4583b"
            ]
        ]
    },
    {
        "id": "298188c9def4583b",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Zwei Nachkommastellen",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 890,
        "y": 200,
        "wires": []
    },
    {
        "id": "839e8384efded1e9",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Unix to Timestamp",
        "info": "",
        "x": 370,
        "y": 300,
        "wires": []
    },
    {
        "id": "2cd2f4bc21e495ac",
        "type": "inject",
        "z": "95f4f9117035b03c",
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
        "x": 360,
        "y": 380,
        "wires": [
            [
                "66e25e61262c74dd"
            ]
        ]
    },
    {
        "id": "66e25e61262c74dd",
        "type": "function",
        "z": "95f4f9117035b03c",
        "name": "Timestamp",
        "func": "var timeString = new Date(msg.payload).toLocaleTimeString(\"de-DE\")\n\nmsg.payload = timeString\n\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 570,
        "y": 380,
        "wires": [
            [
                "8321bb2fa6613570"
            ]
        ]
    },
    {
        "id": "8321bb2fa6613570",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Formattet Time",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 860,
        "y": 380,
        "wires": []
    },
    {
        "id": "ed467e1675bae9cf",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Nachricht unterdrücken",
        "info": "",
        "x": 380,
        "y": 480,
        "wires": []
    },
    {
        "id": "55afce67945c964e",
        "type": "inject",
        "z": "95f4f9117035b03c",
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
        "x": 360,
        "y": 560,
        "wires": [
            [
                "2278a58abc2cf8b3"
            ]
        ]
    },
    {
        "id": "2278a58abc2cf8b3",
        "type": "function",
        "z": "95f4f9117035b03c",
        "name": "Nur gerade",
        "func": "// Wenn die Payload gerade ist.\n\nif (msg.payload % 2 == 0) {\n    // Setze die payload zu \"Test\"\n    msg.payload = msg.payload\n}\nelse {\n    // Gib keine Nachricht aus\n    msg = undefined\n}\n\nreturn msg",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 570,
        "y": 560,
        "wires": [
            [
                "5afb0241c472f308"
            ]
        ]
    },
    {
        "id": "5afb0241c472f308",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Nur gerade Nachrichten",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 890,
        "y": 560,
        "wires": []
    },
    {
        "id": "89f742d55c3e55a0",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Letzte 5",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 900,
        "y": 780,
        "wires": []
    },
    {
        "id": "fb9b794cf7595db6",
        "type": "ui_template",
        "z": "95f4f9117035b03c",
        "group": "b2f754bba4dbda5a",
        "name": "",
        "order": 3,
        "width": "6",
        "height": "7",
        "format": "<table>\n    <tr>\n        <th>Zeit</th>\n        <th>Flaschennummer</th>\n        <th>Gewicht</th>\n    </tr>\n    <tr>\n        <td>{{msg.payload[0].time}}</td>\n        <td>{{msg.payload[0].flaschennummer}}</td>\n        <td>{{msg.payload[0].gewicht_letzte_flasche_in_g}}</td>\n    </tr>\n    <tr>\n        <td>{{msg.payload[1].time}}</td>\n        <td>{{msg.payload[1].flaschennummer}}</td>\n        <td>{{msg.payload[1].gewicht_letzte_flasche_in_g}}</td>\n    </tr>\n    <tr>\n        <td>{{msg.payload[2].time}}</td>\n        <td>{{msg.payload[2].flaschennummer}}</td>\n        <td>{{msg.payload[2].gewicht_letzte_flasche_in_g}}</td>\n    </tr>\n    <tr>\n        <td>{{msg.payload[4].time}}</td>\n        <td>{{msg.payload[4].flaschennummer}}</td>\n        <td>{{msg.payload[4].gewicht_letzte_flasche_in_g}}</td>\n    </tr>\n    <tr>\n        <td>{{msg.payload[5].time}}</td>\n        <td>{{msg.payload[5].flaschennummer}}</td>\n        <td>{{msg.payload[5].gewicht_letzte_flasche_in_g}}</td>\n    </tr>\n</table>",
        "storeOutMessages": false,
        "fwdInMessages": true,
        "resendOnRefresh": true,
        "templateScope": "local",
        "x": 900,
        "y": 840,
        "wires": [
            []
        ]
    },
    {
        "id": "912978e8c90e3ace",
        "type": "join",
        "z": "95f4f9117035b03c",
        "name": "",
        "mode": "custom",
        "build": "array",
        "property": "payload",
        "propertyType": "msg",
        "key": "topic",
        "joiner": "\\n",
        "joinerType": "str",
        "accumulate": false,
        "timeout": "",
        "count": "5",
        "reduceRight": false,
        "reduceExp": "",
        "reduceInit": "",
        "reduceInitType": "",
        "reduceFixup": "",
        "x": 590,
        "y": 800,
        "wires": [
            [
                "89f742d55c3e55a0",
                "fb9b794cf7595db6"
            ]
        ]
    },
    {
        "id": "177b9990a07eb3a0",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Tabelle",
        "info": "",
        "x": 330,
        "y": 740,
        "wires": []
    },
    {
        "id": "a2e30ea63dc654bd",
        "type": "inject",
        "z": "95f4f9117035b03c",
        "name": "",
        "props": [
            {
                "p": "topic",
                "vt": "str"
            },
            {
                "p": "payload"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "{\"time\":1,\"flaschennummer\":\"1\",\"gewicht_letzte_flasche_in_g\":10}",
        "payloadType": "json",
        "x": 350,
        "y": 800,
        "wires": [
            [
                "912978e8c90e3ace",
                "ba391b53116780f3"
            ]
        ]
    },
    {
        "id": "ba391b53116780f3",
        "type": "function",
        "z": "95f4f9117035b03c",
        "name": "VergleicheZielgewicht",
        "func": "var maximaleAbweichungWarnung = global.get(\"maximaleAbweichungWarnung\")\n\nif (maximaleAbweichungWarnung < msg.payload.gewicht_letzte_flasche_in_g) {\n    //  block of code to be executed if the condition is true\n    msg.payload.warning = true\n} else {\n    //  block of code to be executed if the condition is false\n    msg.payload.warning = false\n}\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 600,
        "y": 1320,
        "wires": [
            [
                "22d88bcacfbc93d9"
            ]
        ]
    },
    {
        "id": "b8db44ab1f3225b6",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Globale Variablen",
        "info": "",
        "x": 360,
        "y": 980,
        "wires": []
    },
    {
        "id": "2425225ff0b88a68",
        "type": "ui_numeric",
        "z": "95f4f9117035b03c",
        "name": "",
        "label": "Zielgewicht",
        "tooltip": "",
        "group": "b2f754bba4dbda5a",
        "order": 4,
        "width": 0,
        "height": 0,
        "wrap": false,
        "passthru": true,
        "topic": "set.test",
        "topicType": "global",
        "format": "{{value}}",
        "min": 0,
        "max": 10,
        "step": "0.5",
        "x": 550,
        "y": 1060,
        "wires": [
            [
                "0633ce30431fd699",
                "7926480d672fc18f"
            ]
        ]
    },
    {
        "id": "0633ce30431fd699",
        "type": "function",
        "z": "95f4f9117035b03c",
        "name": "SetGlobalZielgewicht",
        "func": "global.set(\"Zielgewicht\", msg.payload)\n\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 820,
        "y": 1060,
        "wires": [
            []
        ]
    },
    {
        "id": "0a04f67e8a491e9b",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "User Eingaben",
        "info": "",
        "x": 540,
        "y": 1000,
        "wires": []
    },
    {
        "id": "7926480d672fc18f",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Global",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 770,
        "y": 1140,
        "wires": []
    },
    {
        "id": "1768b401d8b60a73",
        "type": "inject",
        "z": "95f4f9117035b03c",
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
        "once": true,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "4",
        "payloadType": "num",
        "x": 370,
        "y": 1040,
        "wires": [
            [
                "2425225ff0b88a68"
            ]
        ]
    },
    {
        "id": "2075fd79c3bf2d6b",
        "type": "comment",
        "z": "95f4f9117035b03c",
        "name": "Sammelt die letzten Nachrichten und sendet erst dann",
        "info": "",
        "x": 740,
        "y": 740,
        "wires": []
    },
    {
        "id": "22d88bcacfbc93d9",
        "type": "debug",
        "z": "95f4f9117035b03c",
        "name": "Warning Zielgewicht",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 920,
        "y": 1320,
        "wires": []
    },
    {
        "id": "b2f754bba4dbda5a",
        "type": "ui_group",
        "name": "IoT1_1",
        "tab": "fbf5c038.d632b",
        "order": 2,
        "disp": true,
        "width": "6",
        "collapse": false
    },
    {
        "id": "fbf5c038.d632b",
        "type": "ui_tab",
        "name": "Beispiele",
        "icon": "dashboard",
        "disabled": false,
        "hidden": false
    }
]
```
---

## 🏆 P5: Setzen Sie den folgenden Use Case um

##### UseCase 1: Dashboard (10pkt)

- Der Schichtleiter möchte die Füllstände des Dispensers in Echtzeit in einem Chart überwachen können. 
- Zudem soll der letzte Füllzeitpunkt angezeigt werden
- Zudem sollen alle abgefüllten Flaschen in einer Tabelle dokumentiert werden, so dass Falschen mit zu geringem Gewicht anhand ihrer Flaschennummer aussortiert werden können.


---

## 🏆 P6: Setzen Sie den folgenden Use Case um (10pkt)

##### UseCase 2: Automatisierte Benachrichtigung

- Da der Schichtleiter nicht ständig neben dem Dashboard steht, möchte er über Probleme automatisiert gewarnt werden
- Hierzu kann er im Dashboard die Abweichungen für kritische und Warnmeldungen einstellen

- Warnung : Anzeige einer Benachrichtigung im Dashboard
    - Gewicht weicht mehr als x g vom Zielgewicht ab
    - Zielgewicht und zulässige akzeptiere Abweichung bis zur Warnung wird über Dashboard eingegeben
    - Füllstand eines Dispensers < 25%

- Kritisch = Anzeige im Dashboard + Benachrichtigung
    - Gewicht weicht mehr als x g vom Zielgewicht ab
    - Zielgewicht und zulässige akzeptiere Abweichung wird über Dashboard eingegeben

---

## Dokumentation

#### UML-Klassen-Diagramm

- Sie können den folgenden [Editor](https://mermaid.live/edit) nutzen
- Speichern Sie die Grafik als `UMLClassDiagramm.svg`

#### UseCase 1

- Speichern Sie den Flow als `UseCase1Flow.json`
- Speichen Sie eine funktionierende Aufzeichnung als Gif oder Video `UseCase1Video.gif/mp4`

#### UseCase 2
- Speichern Sie den Flow als `UseCase2Flow.json`
- Speichen Sie eine funktionierende Aufzeichnung als Gif oder Video `UseCase2Video.gif/mp4`

## Tipps

- Über `payload.topic` lässt sich evtl. die Implementierung vereinfachen
- Nutzen Sie `global.get` und `global.set` um Variablen global zu speichern
