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


# Visualisierung und Data Analytics

## Data Analytics

![](images/datasciencevsdataanalyticsdachevronsshort2xupdate.png)

![](images/datasciencevsdataanalyticsdschevronsshort2xupdate.png)

###### https://www.qlik.com/us/data-analytics/data-science-vs-data-analytics

---

### Zieldefinition

![bg right:45% h:720](images/iot_use-cases.png)

* Automatisierung: z.B. Intralogistik
* Bessere Entscheidungen: z.B. Predictive Maintenance
* nicht immer ist das Ziel schon vor der Datensammlung bekannt 

---

#### Intralogistik

![](images/220222_smart_logistics_iot.svg)

###### https://leogistics.com/internet-of-things/

---


#### Predictive Maintenance

![](images/anacisionpm.png)


---

### Datensammlung

* Anbinden vorhandener Systeme
    * Maschinendaten mit [OPC UA](https://de.wikipedia.org/wiki/OPC_Unified_Architecture)
    * SPS-Daten z.B. über [MQTT](https://infosys.beckhoff.com/index.php?content=../content/1031/tf6701_tc3_iot_communication_mqtt/3518541195.html&id=) 
    * Bestehende Bussysteme z.B. Submetering Stromverbrauch
* Datenerfassung per Telemetrie (VL 8)
* AutoID (VL 5)

---

### Daten-Integration und Management

* Dokumentation von Rohdaten
* Vereinheitlichung und Vorverarbeitung
* Daten auf gemeinsamer Plattform (VL 7)
* Verknüpfbare Daten in gemeinsamer Datenstruktur (z.B. über Datenbankdesign)
* Zuverlässige Datenerfassung (VL 6) mit Qualitätskontrolle

---

#### Beispiel: Modern Data Stack

![](images/dbt-ecosystem-overview-Analytics8-scaled.webp)

---

### Data-Exploration und Analyse

**Deskriptive Statistik**
- Beschreibung eines Datensatzes
- anhand von statischen Kennzahlen
- und Visualisierungen
- Berücksichtigung von Domänenwissen


---

## Datensätze und Variablentypen

- Datensätze sind Sammlungen von Beobachtungen
- gibt es verschieden Tabellen, müssen diese sinnvoll miteinander verknüpft werden (ggf. setzten wir wieder zusammen, was wird davor mühsam aufgetrennt haben)
- Variablen im Datensatz haben bestimmte Variablentypen, die bestimmen, was damit möglich ist

![](images/tidy.png)


---

### ✍️ Aufgabe

- Wie lassen sich die folgenden Listen von Variablen
    - in aufsteigender Reihenfolge sortiert werden?
    - durch einen zentralen Wert beschrieben werden?
    - Beziehung zwischen zwei Werten beschrieben?


- ```gender = ["Male", "Female", "Female", "Female", "Male"]```
- ```education = ["M.Sc.", "B.Sc.", "B.Sc.", "PhD", "none"]```
- ```body_temperature_celsius = [37.85, 39.85, 38.85, 36.85, 37.85]```
- ```points_in_exam = [0, 100, 80, 80, 40]```


---


#### Nominale Variablen

- ```gender = ["Male", "Female", "Female", "Female", "Male"]```

- in aufsteigender Reihenfolge sortiert?
    * Es gibt keine inhärente Möglichkeit, sie in eine Reihenfolge zu bringen
- durch einen zentralen Wert beschrieben?
    * ``"Weiblich"`` ist der häufigste Wert (Modus)
- Was beschreibt die Beziehung zwischen zwei Werten?
    * Sie gehören zur gleichen Kategorie oder nicht

---


#### Ordinale Variablen

- in aufsteigender Reihenfolge sortiert?
    * ```education = ["none", "B.Sc.", "B.Sc.", "M.Sc.", "PhD",]```
- durch einen zentralen Wert beschrieben?
    * Modus
    * 50 % haben "B.Sc." oder weniger (Median)
- Was beschreibt das Verhältnis zwischen zwei Werten?
    * sie sind auf irgendeine Weise niedriger oder höher

---


#### Intervall-Skalierte Variablen

- in aufsteigender Reihenfolge sortiert?
    *  ```body_temperature_celsius = [36.85, 37.85, 37.85, 38.85, 39.85]```
- durch einen zentralen Wert beschrieben?
    * Modus, Median
    * arithmetisches Mittel $38.25=\mu=\frac{1}{n}\sum x_i$
- Wie wird die Beziehung zwischen zwei Werten beschrieben?
    * wir kennen den Abstand (Intervall) zwischen ihnen

---

#### Nominal-Skalierte Variablen

- in aufsteigender Reihenfolge sortiert?
    *  ```points_in_exam = [0, 40, 80, 80, 100]```
- durch einen zentralen Wert beschrieben?
    * Modus, Median, Mittelwert
- Was beschreibt das Verhältnis zwischen zwei Werten?
    * Wir kennen das Verhältnis zwischen (80 ist doppelt so hoch wie 40)

###### We cannot say this about the Celsius scale but the Kelvin scale


---


### Kenngrößen der Deskriptive Statistik

![h:500](images/Deskriptive-Statistik.webp)

###### https://www.scribbr.de/statistik/deskriptive-statistik/

---

#### Lageparameter

![](images/0_wHMvuwRa_YF9SFwY.webp)

* mean / Mittelwert: Arithmetischer Mittelwert $\mu=\frac{1}{n} \sum_{i=i}^{n} x_{i}$
* median / Median: Wert der eine geordnete Liste von Werten in zwei Hälften teilt
* mode / Modus: Häufigster Wert in einer Liste von Werten


---

```Python
import pandas as pd
df = pd.DataFrame({"points_in_exam" : [0, 40, 60, 80, 80, 100] })

df.mean()   # 60 - was ist das gewichtete Mitte
df.median() # 70 - welche Punktzahl beschreibt den Durchschnittsstudent
df.mode()   # 80 - welche Punktzahl ist die häufigste
```


---

#### Streuungsmaße

* variance / Varianz: Summe der quadratischen vom Abweichungen von Mittelwert 
    $\sigma^2 = \frac{\sum_{i=1}^{n}(x_i - \mu)^2}{n}$
* standard deviation / Standardabweichung : $\sigma = \sqrt{\sigma^2}$
* Minimum und Maximum ergeben Spannweite

![h:250](images/streuungsmaße.png)

###### https://datatab.de/tutorial/standardabweichung-varianz-spannweite

---

```Python
import pandas as pd
df = pd.DataFrame({"Weigth" : [0, 40, 60, 80, 80, 100] })

df.var()            # 1280.0
df.std()            # 35.777088
df.max()-df.min()   # 100

```

---


#### Zusammenhangsmaße und Korrelation

- Wie gut kann ein lineares Modell den Zusammenhang der Variablen erklären
- Keine Aussage über Kausalität (Ursache-Wirkung-Beziehung)
- z.B. gemessen als Bravais-Pearson-Korrelationskoeffizient

![h:400](images/Korrelationskoeffizient.png)


###### https://datatab.de/tutorial/korrelation

---



## Visualisierungen von Verteilungen



### Scatter Plot zweier Variablen

- lässt Aussage über Korrelation und Streuung zu

```Python
import pandas as pd
df =pd.DataFrame({"points_in_exam" : 
                    [0, 40, 60, 80, 80, 100],
                  "body_temperature_celsius" : 
                    [39.85, 37.85,  38.05, 36.85, 38.85, 38.35]})
import seaborn as sns

sns.regplot(data=df, 
                x="body_temperature_celsius", 
                y="points_in_exam",  scatter=True, 
                fit_reg=True)
df.corr(method='pearson') # -0.554871	
```

![bg right:40% 90%](images/regression.png)


---

### Histogram

* angenäherte Darstellung der Verteilung
* Informationen über Varianz und Verteilung
* Daten einer einzelnen intervall-skalierten Variablen

![bg right h:350](images/Travel_time_histogram_total_1_Stata.png)



###### https://en.wikipedia.org/wiki/Karl_Pearson, https://en.wikipedia.org/wiki/Histogram

---

#### Konstruieren eines Histogramms

* Alle Werte der beobachteten Variable $x_i$ in eine Reihe von Intervallen einteilen.
* Zählen, wie viele Werte in jedes Intervall fallen (z. B. 5 % der Werte)
* Die Intervalle sind aufeinanderfolgend, überschneiden sich nicht und haben oft die gleiche Breite oder Größe.
* Stellt die Anzahl der Elemente im Intervall auf der y-Achse dar (dividiert durch den Stichprobenumfang für die relative Häufigkeit)

![bg right:45% h:300](images/Travel_time_histogram_total_1_Stata.png)

###### https://en.wikipedia.org/wiki/Histogram

---

```Python
import pandas as pd
df = pd.DataFrame({"points_in_exam" : 
                    [0, 40, 60, 80, 80, 100]})
df.hist(bins = 3)

bucket_0_bis_35 =   [0]
bucket_35_bis_65 =  [40, 60]
bucket_65_bis_100 = [80, 80, 100]
```

![bg right w:80%](images/histogram.png)


