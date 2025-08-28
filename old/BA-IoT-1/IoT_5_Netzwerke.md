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

# Netzwerke


---

##  Kommunikation von binären Daten

### 🎯 Lernziele

Nach dieser Einheit sind Sie in der Lage dazu
* drei Elemente zum Aufbau von Computernetzen beschreiben
* die Analog-Digitalwandlung zur Signalisierung zu beschreiben
* die Wichtigkeit von Übertragungskapazität und Latenz verschiedener Anwendungsfälle abzuschätzen
*  das Konzept der Amplituden und Frequenzmodulation zu erklären 

---

### 🧠 3 zwingend nötige Elemente für Computernetzwerk

* Mindestens **2 Rechner** mit Netzwerkdiensten und Datenstationen
    * **Server** bietet Dienst an
    * **Client** nutzt Dienst (Rolle kann tauschen)
* **Kanal / Übertragungsmedium**
    * Dient dem Austausch von Daten
* **Netzwerkprotokolle**
    * Regeln, die festlegen, wie Rechner miteinander kommunizieren können

![bg h:180 right:33%](images/client_server.png)

---

#### Beispiele Rechnernetze

* PCs zu geteiltem Netzwerklaufwerk
* Smartphone zu Internet
* Sensor zu SPS
* SPS zur MQTT-Broker


![bg right h:470](images/DatenkommunikationBeispiele.png)


---



### Übermittlung von Signalen durch Analog-Digital-Wandlung

![h:300](images/Signalisierung.svg)

- Die binäre Information wird zur Übertragung in ein Analogsignal gewandelt
    ```01011010101010100...```
* in Welleneigenschaften einer elektromagnetischen Welle (Frequenz, Wellenlänge und/oder Amplitude) z.B. WLan, Bluetooth
* oder ein Spannungswert auf einem Leiter z.B. Ethernet

---

#### Frequenz und Amplituden-Modulation

![bg h:350 right](images/FMAM.png)

* Bits können in Wellen über die **Frequenz, Amplitude** oder die Phase codiert werden.

---

##### Frequenzspektren

![bg left:60% w:720](images/spektrum-vergleich-5g.webp)

###### https://www.5g-anbieter.info/technik/5g-mmwave.html

* geringe Frequenz: lange Reichweite, geringe Bandbreite
* hohe Frequenz: geringe Reichweite, hohe Bandbreite


---

#### 🧠 Signalisierung auf Kabeln

![h:300](images/Signalisierung.svg)

* Bits auf Kabeln als Leitungscodes z.B. über Spannungen signalisiert
    * **Non-Return-to-Zero** (Abbildung oben)
    * jeder Bit-Wert hat genau ein Leitungszustand (z.B. hohe Spannung vs. niedrige Spannung)



---

##### 🧠 Kennzahlen für die Übertragungsqualität

- **Übertragungskapazität** (Übertragungsrate, engl.: transfer rate, throughput): Datenmenge pro Zeit in Bits pro Sekunde

* **Latenz** (Übertragungsverzögerung, engl.: latency): **Verzögerung** zwischen dem
Versenden und der Ankunft des ersten Datenbits einer Meldung in Millisekunden. 
    * `ping www.google.com` gibt die Zeit vom absenden der Nachricht bis zur Rückkehr der Antwort an

![bg h:350 right:40%](images/qt7fwxo5kvboxuhzjmlb.jpeg)

###### https://dev.to/nbosco/latency-vs-throughput-2bn6


---


#### Entwicklung der Übertragungskapazitäten

<center>

![h:450](images/übertragugnskapa.png)

</center>

---


#### ✍️ Frage

Bei manchen Anwendungen ist die Latenz zweitrangig (z.B. Versenden von Emails.) Bei welcher Anwendung ist die Latenz wichtig?
* Telefon
* Online-Spiele


---

## Rechnernetze

<center>

![h:400](images/Keller_lan.jpg)

</center>

###### https://de.wikipedia.org/wiki/LAN-Party#/media/Datei:Keller_lan.jpg

---


### 🎯 Lernziele


Nach dieser Einheit sind Sie in der Lage dazu
* verschiedene Kriterien zu beschreiben, nach denen Rechnernetze unterschiedenen werden können
* Vor- und Nachteile verschiedener Netzwerk-Topologien zu beschreiben


---


### 🧠 Strukturelle Kriterien

*  **Netzwerktopologie** definiert, welche **Datenstationen (Knoten)** in einem
Netzwerk mittels **Kommunikations-verbindungen (Kanten)** physisch miteinander verbunden sind

![bg h:150 right](images/netztopologien.png)


---


#### 🧠 Stern-Topologie 

* Alle Knoten sind direkt an einer zentralen Komponente (**Hub oder Switch**) angeschlossen
* Ausfall der zentralen Komponente führt zum Ausfall des kompletten Netzes
* Leicht **verständlich** und erweiterbar 
* Ausfall eines Knotens führt nicht zum Ausfall des Netzes
* z.B. Heimnetzwerke, Infrastruktur-Wlan mit zentralem (Access Point)

![bg h:250 right:33%](images/stern.png)

---

<center>

![](images/zte_mc801a_router_5g__1.png)

</center>

###### https://www.educom.at/hardware/router/zte-mc801a-router

---

#### 🧠 Bus-Topologie

* Alle Knoten sind mit demselben Übertragungsmedium (dem **Bus**) verbunden
* Keine aktiven Komponenten zwischen Knoten und Medium
* Ausfall einzelner Knoten führt nicht zum Ausfall des Netzes
* Geringe Kosten für Aufbau (Switches waren mal teuer!)
* **Störung des Übertragungsmediums blockiert den gesamten Bus**
* Zu jedem Zeitpunkt kann nur eine Station Daten senden. Ansonsten kommt es zu Kollisionen
* z.B. Feldbusse: CAN, Profibus

![bg h:250 right:23%](images/bustopo.png)

---

<center>

![](images/mbusLinie.png)

</center>

###### https://www.molline.de/fileadmin/content/content/Downloads/Info-Datenbl%C3%A4tter/iDB1011_MBus_Installationshinweise.pdf

---


#### 🧠 Maschen-Topologie

* jeder Teilnehmer mit einem oder **mehreren anderen Teilnehmern** verbunden 
* Fällt ein Teilnehmer oder eine Verbindung aus, ist die Kommunikation
durch **Umleiten (Routing)** der Daten im Regelfall weiter möglich
* **Ausfallsicher** (abhängig vom Verkabelungsaufwand)
* Hoher **Verkabelungsaufwand** und Energieverbrauch
* Komplexes Routing (Wegfindung für Information)
* z.B. WWW, Ad-hoc-(Funk-)Netze

![bg h:250 right:30%](images/maschentopo.png)

---
#### 🧠 Baum-Topologie 

* Von einer Wurzel gehen eine oder mehrere Kanten aus
* Jede Kante führt zu einem Blattknoten oder zu Wurzeln weiterer Bäume
* **Gute Erweiterbarkeit** und große Entfernungen realisierbar
* Beim **Ausfall eine Wurzel** ist der komplette davon ausgehende (Unter)Baum nicht mehr erreichbar
* z.B. Verbindungen zwischen den Verteilern (Hub, Switch) werden mittels eines Uplinks hergestellt

![bg h:250 right:33%](images/baum.png)


---

#### 🧠 Zellen-Topologie

* Kommt hauptsächlich bei **drahtlosen** Netzen zum Einsatz
* Zelle: Bereich (*Reichweite*) um eine Basisstation (z.B. WLAN Access Point), in dem eine Kommunikation zwischen den Endgeräten und der Basisstation möglich ist
* Keine Störung durch Ausfall von Teilnehmern
* Störanfällig abhängig von der Qualität der Basisstation(en)
* z.B. **Wireless LAN** (IEEE 802.11), Global System for Mobile Communications (**GSM**)


![bg h:250 right:33%](images/funkzelle.png)


---

#### Struktur des Internets

![bg right height:500](images/StrukturInternet.png)

- Kommandozeile: ```tracert <url>```
* Der Befehl zeichnet den Weg zum erreichen des Ziels nach

---

![](images/Tracert_Eingabeaufforderung.png)


---

### 🧠 Geografische Kriterien

* räumliche Netzausdehnung
* **Personal area network** (PAN)
    ein Quadratmeter um eine Person z.B.: Smart Watch + Smartphone
* **Local area network** (LAN) für eine Betriebsstätte
* **Metropolitan area network** (MAN)  für ein städtisches Ballungszentrum 
* **Wide area network** (WAN) als Weitverkehrsnetz

![bg h:300 right:50%](images/netzeausdehung.png)

###### Distanzen in der Grafik gelten eher der Orientierung als der genauen Definition




---

## Kommunikationsprotokolle

<center>

![h:400 right](images/Kommunikationsmodelle-Reden-Verstehen-Gespaechsebenen-Grafik.jpg)

</center>

###### https://karrierebibel.de/kommunikationsmodelle/

---

### 🎯 Lernziele

Nach dieser Einheit sind Sie in der Lage dazu
* die Bedeutung von Kommunikationsprotokollen zu beschreiben
- eine Entscheidung für verbindungslose und verbindungs-orientierte Protokolltypen für verschiedene Anwendungsfälle zu treffen
* die Bedeutung der Schichten im OSI-Modell zu erläutern
* wichtige Netzwerkkomponenten zu unterscheiden 

---

### 🧠 Kommunikationsprotokolle

* **festgeschriebene Konvention** für die Kommunikation zwischen Datenstationen.
* regelt den **Aufbau von Meldungen** (Syntax, Repräsentationsgrößen, notwendige Inhalte)
* **welche Antworten auf Meldungen** erfolgen müssen/können.
* Codierung
* Wann gibt es Feedback?

![bg h:300 right](images/Sender-Empfänger-Modell.svg)

###### https://de.wikipedia.org/wiki/Kommunikationsmodell

---


#### Menschliche Kommunikationsprotokolle


* Sprache
    * Es spricht eine **nach der anderen**
    * Sprecher:innen müssen die **gleiche Sprache** / Schrift benutzen
* Prozesse und Formulare:
    * Steuererklärung beim Finanzamt braucht bestimmte **Formulare** 
    * Auf einem Brief muss Adressat mit Namen und Adresse stehen




---


#### Kommunikationsprotokolle für Computer

Zu den Vereinbarungen gehören:
* Welche Station sendet an wen und aus welchem **Anlass**?
* Was ist die **maximale Länge** einer Nachricht?
* Was geschieht bei Fehlern?
* Wie erkennt man das **letzte Bit** einer Nachricht?
* Wie erkennt man, dass eine Nachricht **verloren** wurde?
* Wie kann man eine verlorene Nachricht erneut anfordern?

---


### Beispiel TCP/IP-Proktoll für die Kommunikation im Netzwerk

<center>

![h:400](images/nachrichtbauentcpip.png)

</center>

---

![](images/OSI-Examlpe/Folie1.PNG)

---

![](images/OSI-Examlpe/Folie2.PNG)

---

![](images/OSI-Examlpe/Folie3.PNG)

---

![](images/OSI-Examlpe/Folie4.PNG)

---

![](images/OSI-Examlpe/Folie5.PNG)

---

![](images/OSI-Examlpe/Folie6.PNG)

---

![](images/OSI-Examlpe/Folie7.PNG)

---

![](images/OSI-Examlpe/Folie8.PNG)

---

![](images/OSI-Examlpe/Folie9.PNG)

---

![](images/OSI-Examlpe/Folie10.PNG)

---

![](images/OSI-Examlpe/Folie11.PNG)

---

![](images/OSI-Examlpe/Folie12.PNG)

---

![](images/OSI-Examlpe/Folie13.PNG)

---

![](images/OSI-Examlpe/Folie14.PNG)

---

![](images/OSI-Examlpe/Folie15.PNG)

---

![](images/OSI-Examlpe/Folie16.PNG)

---

![](images/OSI-Examlpe/Folie17.PNG)

---

![](images/OSI-Examlpe/Folie18.PNG)

---

![](images/OSI-Examlpe/Folie19.PNG)

---

![](images/OSI-Examlpe/Folie20.PNG)



---


### 🧠 Open Systems Interconnection (OSI) Model

![bg h:500 right](images/osi.png)

- Wenn sie eine Email schicken, soll dies **unabhängig** davon sein, ob sie mit dem Handy im LTE-Netz verbunden oder an einem PC über ihr heimisches WLAN und glasfaser-gebunden mit dem Internet verbunden sind.
* Die Anwendung ist ident, auch wenn die Bitübertragung völlig anders ist.

---



![bg h:500 right](images/osi.png)

* Das  gliedert die Teilaufgaben der Kommunikation in sieben Funktionsschichten. 
* Auf jeder Schicht sind entsprechende Protokolle vorgesehen, für die es mehrere Alternativen geben kann.

---

#### 🧠 1 Bitübertragungsschicht (Physical Layer)

![bg w:400 right:35%](images/nachrichtbauentcpip.png)

* physikalisch-technischen Eigenschaften
* **Darstellung der Zustände "1" und "0"**
* Das bestimmt:
    * z.B. Art der Modulation oder Leitungscode
    * Wie viele Bits können pro Sekunde gesendet werden?
    * Kann die Übertragung in beide Richtungen gleichzeitig stattfinden?

* Hardware: Repeater, Hubs, Leitungen, Stecker, u. a.


---

#### 🧠 2 Sicherungsschicht (Data Link Layer)

![bg w:400 right:35%](images/nachrichtbauentcpip.png)

* Zugangsverfahren für das Kommunikationsmedium (z.B. Senderechten)
* potenziell auftretende **Übertragungsfehler** erkennen und behandeln
* Verkehrspolizist  im Dorf
* Hardware auf dieser Schicht: Bridge, Switch
* Protokolle und Normen: IEEE 802.11 (WLAN), Ethernet-Protokoll, ...
* Adressierung der Geräte mit physischen Adressen (MAC-Adressen)

---


#### 🧠 3 Vermittlungsschicht (Network Layer)

![bg w:400 right:35%](images/nachrichtbauentcpip.png)

* Adressierung von Zielsystemen (Rechnern) über mehrere Teilstrecken hinweg sowie die **Steuerung der Wegwahl**.
* Der kürzeste Weg ist nicht immer optimal
* **Internet Protocol**: jedes IP-Paket wird unabhängig an sein Ziel vermittelt (geroutet)
* Adressierung der Geräte mit logischen Adressen (IP-Adressen)

---

##### 🧠 Vermittlungsschicht ist vor allem bei vermaschten Topologien relevant

<center>

![h:250](images/netztopologien.png)

</center>

---



#### 🧠 4 Transportschicht (Transport Layer)

![bg w:400 right:35%](images/nachrichtbauentcpip.png)

* Verbindungen zwischen zwei Anwendungen
* empfangenen Nachrichten werden in die **korrekte Reihenfolge** gebracht
* verloren gegangene Nachrichten werden neu angefordert
* Die zwei wichtigsten Transportprotokolle:
    * TCP (Transport Control Protocol): verbindungsorientiert
    * UDP (Universal Datagram Protocol): verbindungslos


---

##### 🧠 4 Transportschicht: Verbindungslose Protokolle

* Analog zum **Briefkasten** ohne Einschreiben
* Kein Verbindungsaufbau notwendig
* Nachrichten werden vom Sender verschickt, wenn Sie vorliegen, ohne eine Verbindung aufzubauen
* Keine Zustellungsgarantie, dafür schneller
* z.B. **Streaming von Videos**


---


##### 🧠 4 Transportschicht: Verbindungsorientierte Protokolle 
    
* Analog zum **Schnur-Telefon**
* Eine Verbindung zwischen Sender und Empfänger wird aufgebaut, dann werden Daten ausgetauscht und handeln das zu verwendende Protokoll aus. Anschließend wird die Verbindung abgebaut
* Es gibt eine **Zustellungsgarantie**
* Diese ist aber **zeitaufwendig**
* Für alles andere

![bg h:400 right:33%](images/Schnurtelefon.jpg)

---

<center>

![h:600](images/tcp-verbindungsaufbau-drei-wege-handshake.jpg)

</center>

###### https://www.ionos.de/digitalguide/server/knowhow/tcp-vorgestellt/

---


#### 🤓 5 Sitzungsschicht 

![bg h:300 right:35%](images/osi.png)

* Die Sitzungsschicht wird in der Praxis kaum benutzt
* Typischerweise besteht eine Sitzung aus einem Verbindungsaufbau (**Anmeldung**), dem Austausch von Daten und dem Verbindungsabbau (**Abmeldung**)

    

---


#### 🤓 6 Darstellungsschicht


![bg h:300 right:35%](images/osi.png)

*  Die Darstellungsschicht wird in der Praxis kaum benutzt
* Daten in eine **standardisierte Darstellung** gebracht. 
* In dieser Schicht werden beispielsweise Zeichensätze von (heterogenen) Kommunikationspartnern angeglichen


---


#### 🧠 7 Anwendungsschicht

![bg w:400 right:35%](images/nachrichtbauentcpip.png)

* Kommunikationsprotokolle für **Dateitransfer, E-Mail** oder der Zugriff auf **Webserver** 
* Protokolle z.B.: 
    * HTTP - Websites (später)
    * SSH - Secure Shell (Kommandozeile)
    * FTP - File Transfer
    * SMTP - E-mails
    * LDAP - Rechteverwaltung

---

### 🧠 Anwendungsschicht

- In der Anwendungsschicht laufen **Dienste (Prozesse)**
- Diese werden neben der IP über eine *Portnummer* gekennzeichnet
![bg h:350 right](images/webdienst.png)
* z.B. **Port 80** für die Bereitstellung einer Website als **HTML**
* Dieser wird mit```:``` an die IP angehängt 
    * z.B. läuft die Facebook-Website auf:  ```31.13.84.36```**```:80```**
    * z.B. node-red auf ```localhost:1880```
    * z.B. MQTT auf ```158.180.44.197:1883```
* [Liste der standardisierten Ports](https://de.wikipedia.org/wiki/Liste_der_standardisierten_Ports)

---

### Netzwerkkomponenten

- um diverse Netzwerktopologien umzusetzen gibt es neben den Computern noch weitere Netzwerkkomponenten mit bestimmten Aufgaben

![bg h:250 right:33%](images/stern.png)


---


#### 🧠 Repeater

- Verstärkung des Signal, wenn maximale Strecke erreicht
- Signale werden verstärkt, aber Daten nicht verändert
- meist keine Konfiguration notwendig

![bg right height:600](images/Repeater.png)



---

#### Beispiel Repeater

![bg right height:600](images/41a97ae1e08bec5816b9e02ca0ba54fe.large.jpg)

###### https://www.preisvergleich.at/tag/WLAN-Repeater.html

---

#### 🧠 Bridges

![bg right height:600](images/Bridges.png)


- Verbindung zweier oder mehrerer lokaler Netze z.B. mit unterschiedlichen Buszugriffsverfahren
- Netzwerke müsse auf der oberen Teilebene der Sicherungsschicht (Logical Link Control der OSI-Schicht 2) mit denselben Protokollen arbeiten

---

##### Beispiel Bridge

<center>

![](images/SF10759-005_EN_v1.png)

</center>

###### https://www.belkin.com/de/support-article?articleNum=10759

---

#### 🧠 Router

- Führt Datenpakete auf ihrem Weg zwischen mehreren Netzwerken (routing) 
- arbeitet auf Schicht 3 (Vermittlungsschicht) des OSI-Modells


![bg right height:600](images/router.png)

---

##### Beispiel Router

![bg right height:600](images/202101140028.jfif)


---

#### 🤓 Gateway

* allgemein: Komponente (Hard- oder Software), welche zwischen zwei Systemen eine Verbindung herstellt. 
* auf allen Schichten des OSI-Modells denkbar
* im Kontext des Internet
    *  früher z.B. Verbindung vom lokalen Netz zum Internet
    * heute hier vor allem Router
    * **Default Gateway**: leitet alle nicht zu einem Subnetz gehörenden Netzwerkanfragen in ein anderes Subnetz weiter 

![bg right w:500](images/Flilius_Gateway.png)

---

## TCP/IP-Protokoll

<center>

![](images/1_hUb4hQKbQkw4fo8wkcAO-w.gif)

</center>

###### https://medium.com/software-engineering-roundup/tcp-ip-protocol-suite-ec7ed4888d5d

---

### 🎯 Lernziele

Nach dieser Einheit sind Sie in der Lage dazu
* valide IP-Adressen zu erkennen
* Netzwerk- und Host-Adresse einer IP-Adresse mittels 
Subnetzmaske zu erkennen
* zwischen MAC und IP-Adressen zu unterscheiden


---



### 🧠 IP-Adressen

* Zentrales Protokoll des Internets
* Aufgebaut in mehreren Schichten (OSI-Schichtenmodell)
* Die **IP-Adresse** eine Rechneradresse auf der **OSI-Vermittlungsschicht** (vergleichbar mit **Telefonnummern**). 
* Interessant in der Software-Entwicklung ist vor allem die **Anwendungsschicht**

![bg h:400 right](images/TCPIPschicht.png)


---

#### 🧠 Aufbau IP-Adressen 

<center>

![h:300](images/ipaufbau.png)

</center>


* 4 Byte (mit je 0 bis 255 Zuständen!) also 32 Bits

---


#### ✍️ Wie viele IPv4-Adressen gibt es?

* $2^{32}=4.294.967.296$
* 2020 über 27 Mrd. vernetze Geräte 
* Es gibt auch IPv6: z.B. `2a03:2880:f107:83:face:b00c:25de` (128 Bits)

###### Die Buchstaben bei IPv6 folgen aus der Hexadezimaldarstellung der Bits

---


### 🧠 IP-Pakete

- Die IP-Adresse dient der Adressierung (vgl. Absender und Adressat auf einem Brief)
* IP-Nutzdaten werden in IP-Paketen verschickt.

![bg h:300 right](images/ippaket.png)


---


#### ✍️ Aufgabe
- Kann Ihr Browser die IPs erreichen?
    - `31.13.84.36`
    - `31.13.84.36:80`
    - `[2a03:2880:f107:83:face:b00c:25de]:80`

* Menschen können eher mit Worten als mit Bits arbeiten
    * Übersetzung symbolische Adressen auf IP-Adressen erfolgt über den **Internet-Dienst DNS** (domain name service): [facebook.com](www.facebook.com)

⌛ 3 Minuten

---

### 🧠 Internet-Dienst DNS

<center>

![](images/DNS-cache_1_netbeez_blog.png)

</center>



###### https://netbeez.net/blog/how-dns-cache-works/

---


#### Externe vs Lokale IP-Adressen

![bg right h:720](images/Avast-IP-Addresses-DE.png)

###### https://www.avast.com/de-de/c-what-is-an-ip-address#:~:text=Eine%20IP%2DAdresse%20besteht%20aus,die%20Netzwerk%2DID%20und%20die%20.

- der Router nimmt die Übersetzung mittels Network Address Translation (NAT) vor
- finden der lokalen IP: Eingabeaufforderung ```ipconfig```
- finden der öffentlichen IP: [externe Websites](https://myexternalip.com/raw)

---

#### Network Address Translation

* Üblicherweise durch Router (Default-Gateway eines Hosts).
* Rechner im lokalen Netzwerk können nicht über ihre Interne IP von außen angesprochen werden
* Bei Verbindungsaufbau durch einen internen Client wird die interne Quell-IP-Adresse durch die öffentliche IP-Adresse des Routers ersetzt. Quellport des internen Clients wird durch einen freien Port des Routers ersetzt
* Zuordnung in der Session-Table (NAT-Table) des Routers:

<center>

![](images/NATExample.JPG)

</center>


###### https://www.thenetworkdna.com/2020/05/introduction-to-nat-network-address.html

---

#### 🧠 Netzwerkadresse für IPv4 im Lokalen Netz

<center>

![h:200](images/ipaufbau.png)

</center>


* legt fest welche IP-Adressen ein Gerät im eigenen Netz ohne die Zuhilfenahme eines Routers erreichen kann (vgl. Ortsvorwahl beim Telefon)
* Der Netzwerkteil muss bei allen Geräten des jeweiligen Netzes gleich sein

---

#### 🧠 Was bedeutet das?

<center>

![h:300](images/SubNetzMaske.png)

</center>

* Subnetzmaske is ```255.255.254.0```
* In Bit-Schreibweise: ```1111 1111.1111 1111.1111 1110.0000 0000```
* IP wird zerlegt ```193.171.235.190```
* In Bit-Schreibweise: ```1100 0001.1010 1011.1110 1011.1011 1110```

---

#### 🧠 Beispiel Netzwerkmaske

* gibt die Bits an, die Teil der Netzwerkadresse sind
* Nur die letzten drei Stellen sind Teil der Hostadresse:

|  | IPv4-Adresse |  192.168.173.134 |
|---|---|---|
| UND | Netzmaske     | 255.255.255.0 |
| = | Netzwerkteil  | 192.168.173.0 |

* Nur die letzten drei Stellen sind Teil der letzten sechs Stellen:

|  | IPv4-Adresse |  192.168.173.134 |
|---|---|---|
| UND | Netzmaske     | 255.255.0.0 |
| = | Netzwerkteil  | 192.168.0.0 |

---

#### 🧠 Übereinanderlegen von Adresse und Maske

1) ```1111 1111.1111 1111.1111 1110.0000 0000``` (Maske)
1) ```1100 0001.1010 1011.1110 1011.1011 1110``` (Adresse)
1) ```1100 0001.1010 1011.1110 101________``` (Netzwerkteil)
1) ```____________________________1.1011 1110```  (Host-Adresse) 
* Wie viele Teilnehmer kann das Netzwerk haben?
    * Host-Adresse hat 9 Stellen
    * maximal $2^9=512$ Teilnehmer
* Zwei spezielle IPs für Hostanteil:
    * ```0.0000 0000``` - Netzadresse: erreicht beschreibt das Netzwerk
    + ```1.1111 1111``` - Broadcast: erreicht alle IPs im Netz

---

##### Frage

- Welche der folgenden Zahlen sind valide Subnetzmasken?
* ```255.0.0.0```
    * `1111 1111.0000 0000.0000 0000.0000 0000`
    * Ja
* ```0.255.255.0```
    * ```0000 0000.1111 1111.1111 1111.0000 0000```
    * Nein, da die Maske zu Beginn aus `1` bestehen muss
* ```255.255.255.253```
    * `1111 1111.1111 1111.1111 1111.1111 1101`
    * Nein, da die Maske mit einer Folge von `0` Enden muss

---

#### [CIDER](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing) Darstellung

* `192.168.2.7/24` 
    * $24$ ist die Anzahl an Bits in der Netzmaske
    * `192.168.2.7` IP 
    * `255.255.255.0` Subnetzmaske hat 24 Bit gesetzt
    * `11000000.10101000.00000010.00000111` IP
    * `11111111.11111111.11111111.00000000` Netzmaske

---

### 🧠 MAC-Adressen

![h:200](images/UMTS_Router_Surf@home_II,_o2-0017.jpg)

* IP-Adresse: 
    * konfigurierbar je nach Netzwerk (vgl. Kennzeichen beim KFZ)
    * Schicht 3: Vermittlungsschicht
* MAC-Adresse: 
    * in der Regel unveränderbar (vgl. Fahrwerksnummer beim KFZ)
    * Schicht 2: Sicherungsschicht

###### https://de.wikipedia.org/wiki/MAC-Adresse#/media/Datei:UMTS_Router_Surf@home_II,_o2-0017.jpg


---


#### Zuordnung MAC (physikalische) und IP-Adressen


<center>

![h:400](images/ZurordnungMACIP.png)

</center>


---

### 🧠 Address Resolution Protocol (ARP)-Protokoll

* Media Access Code (Physikalische Adresse):  Nummer eines Gerätes auf einer Datenverbindung. Anhand dieser Nummer werden über die Verbindung laufende Daten den Geräten zugeordnet.
* Jede Ethernet-, WLAN- oder Bluetooth-Netzwerkkarte besitzt solch eine eindeutige MAC-Adresse, unter der sie angesprochen werden kann. Obwohl sie effektiv nur in lokalen Netzen eine Bedeutung haben, sind MAC-Adressen üblicherweise global eindeutig und besitzen keinerlei Strukturmerkmale, die für die Wegewahl (Routing) genutzt werden können.
* Sicherungsschicht (Schicht 2) des OSI-Modells
* Die IP-Adresse wird vom Betriebssystem konfiguriert. Die physische Adresse, auch MAC-Adresse genannt, befindet sich im ROM der Netzwerkkarte.

---

#### Ermittlung von MAC-Adressen für IP-Adressen

* über das ARP-Protokoll 
* Der Absender sendet einen **Broadcast** (Meldung an alle) im lokalen Subnetz, mit dem er die MAC-Adresse zu einer IP erfragt.  
    * Ist die Zieladresse im lokalen Subnetz, antwortet der Zielrechner. 
    * Ist der Rechner in einem anderen lokalen Subnetz, so antwortet der Vermittlungsknoten (**Defaultgateway**), der die Weiterleitung für die Daten übernimmt.

![bg h:300 right:40%](images/arp.png)


---


#### Beispiel ARP-Protokoll

* Wenn A an die IP-Adresse von B Daten verschicken möchte, kann B direkt auf diesen Broadcast antworten.

* Möchte A an die IP-Adresse von C Daten verschicken und C liegt in einem anderen Teilnetz, so antwortet der Vermittlungsknoten R1 mit seiner MAC-Adresse, die dann von A für die Verschickung von Daten an C genutzt wird.

![bg h:400 right](images/arp.png)


---

<center>

![](images/no_place_like_home.png)


</center>

* Spezielle IP: ```127.0.0.1``` - genannt *Localhost*: zieht sich immer 



---

#### ✍️ Netzwerke mit Windows

- Wie lautet Ihre lokale IPv4-Adresse?
- Wie lautet Ihre MAC-Adresse?
- Wie lautet die Subnetzmaske des Netzwerks?

* Hinweis: Nutzen Sie ggf. die google-Suche, um an Ihr Ziel zu gelangen

⌛ 15 Minuten

---

##### Netzwerkverbindungen anzeigen / Details

<center>

![h:600](images/ipConfigNetzwerkCenter.png)

</center>


---

##### Eingabeaufforderung / ipconfig

<center>

![h:600](images/ipconfig.png)

