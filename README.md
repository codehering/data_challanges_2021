# Data Challanges - Numismatic 2021 Repository
Dieses Repository beinhaltet alle Skripte und Experimente, die im Rahmen der Vorlesung Data Challenges erstellt wurden. Im Folgenden wird dabei kurz auf die einzelnen Verzeichnisse eingegangen.

## Technische Umsetzung
Für die technische Umsetzung des Projektes wurden die Programmiersprache Python und die statistische Skriptsprache R verwendet. Dabei wurde vor allem im ersten Schritt für die jeweiligen Experimente und explorativen Analysen Python mit der Erweiterung Jupyter Notebook verwendet. Für das interaktive Dashboard wurde wiederum das sehr einfach gehaltene High-level Framework Shiny verwendet. 

## Verzeichnisstruktur:

### dashboard:
Beinhaltet alle Skripte die für das Dashboard benötigt werden, inklusive der Skripte, die die Daten in geeigneter Weise aufbereiten, so dass diese vom Dashboard verarbeitet werden können. Dabei wird unteschieden zwischen:

**-Frontend:**

Unter Frontend sind nur Skripte die für das das Dashboard selbst benötigt werden. Also alle Skripte die für die interaktive Darstellung notwendig sind (inklusive Login, das Laden der Daten und Aggregation der Daten.

**-Backend:**

Unter Backend sind alle Skripte die notwendig sind, um die Daten in ein für das Dashboard geeignetes Format zu bringen (rds format) (ETL.R). Des Weiteren liegt in diesem Verzeichnis rf_classifer.R. Dieses Skript trainiert die RandomForest modelle die für den Coin Finder des Dashboards notwendig sind, um ähnliche Münzen anhand bestimmter Kriterien finden zu können.
### data_prep:


