# Data Challanges - Numismatic 2021 Repository
Dieses Repository beinhaltet alle Skripte und Experimente, die im Rahmen der Vorlesung Data Challenges erstellt wurden. Im Folgenden wird dabei kurz auf die einzelnen Verzeichnisse eingegangen.
Der Quellcode ist unter https://github.com/codehering/data_challanges_2021 frei verfügbar. 
## Technische Umsetzung
Für die technische Umsetzung des Projektes wurden die Programmiersprache Python und die statistische Skriptsprache R verwendet. Dabei wurde vor allem im ersten Schritt für die jeweiligen Experimente und explorativen Analysen Python mit der Erweiterung Jupyter Notebook verwendet. Für das interaktive Dashboard wurde wiederum das sehr einfach gehaltene High-level Framework Shiny verwendet. 

## Verzeichnisstruktur:

### dashboard:
Beinhaltet alle Skripte, die für das Dashboard benötigt werden. Inklusive der Skripte, die die Daten in geeigneter Weise aufbereiten, so dass diese vom Dashboard verarbeitet werden können. Dabei wird unterschieden zwischen:

**-Frontend:**

Unter Frontend sind nur Skripte, die für das das Dashboard selbst benötigt werden. Also alle Skripte, die für die interaktive Darstellung notwendig sind (inklusive Login, das Laden der Daten und Aggregation der Daten).

**-Backend:**

Unter Backend sind alle Skripte, die notwendig sind, um die Daten in ein für das Dashboard geeignetes Format zu bringen (rds format) (ETL.R). Des Weiteren liegt in diesem Verzeichnis rf_classifer.R. Dieses Skript trainiert die RandomForest Modelle, die für den Coin Finder des Dashboards notwendig sind, um ähnliche Münzen anhand bestimmter Kriterien finden zu können.
### data_prep:
Unter data_prep finden sich alle Skripte, die für die Aufbereitung der Daten notwendig waren. Dabei existieren entitätsspezifische Skripte, wie auch Skripte, die sich mit der Aufbereitung des RDF-Datensatzes beschäftigen. Das Skript data_preperation_for_analysis.py bereitet die über eine SPARQL-Query gezogenen Daten für die weiteren Analyseschritte auf. Das Skript dimension_reduction.py beinhaltet die kompletten Schritte für die UMAP Dimensionsreduzierung. In der Datei timperiods_clustering.py ist die gesamte Logik der Clusteringverfahren gespeichert.
### experiments:
In dem Verzeichnis experiments liegen alle Skripte, welche uns geholfen haben entweder die Daten an sich oder verschiedene datengetriebene Methoden zu verstehen. Wichtig ist, dass nicht alle Ideen und Methoden, die in diesem Verzeichnis angewandt wurden, auch später weiter verfolgt und ausgebaut wurden. Insofern kann dieses Verzeichnis als Sammelstelle aller für das Projekt essenziell wichtigen Teile betrachtet werden, auch wenn vieles keinen direkten Einfluss auf die Ergebnisse unseres Projektes hatte. Wir unterscheiden dabei zwischen vanilla Python und jupyter notebook Experimenten. Letztere sind deutlich besser aufbereitet und können dadurch auch leichter verstanden werden. Besonders interessant sind dabei die Notebooks Dimesion_reduction_analysis.ipynb (geht auf die verschiedenen Dimensionsreduzierungsalgorithmen ein und vergleicht diese), different_timeperiods_umap_analysis.ipynb (ein erster Versuch die verschiedenen kMeans-Cluster nach der UMAP-Transformation zu interpretieren) und predict_coin_data_with_entitys_experiments.ipynb (Vorhersage von Münzdaten, wie z.B. enddate nur mit Hilfe der Entitäten).
### plots:
Im plots Verzeichnis sind unsere Bilder (wie etwa Korrelationsmatrix, Ergebnisse aus kMeans, etc.) gespeichert.

## Das Dashboard
Zentraler Bestandteil unserer Arbeit war neben der explorativen Analyse der Münzdaten auch ein R Shiny Dashboard, welches als self-service Analysetool gesehen werden kann. Das Dashboard wurde von uns eingeführt, da wir Probleme hatten einzelne Cluster oder Gruppen von Münzen mit klassischen Plots und Tabellen zu analysieren. Insbesondere die zeitliche Untersuchung verschiedener Entitäten ist mit einem einfachen Plot und der Tatsache, dass über 500 verschiedene Entitäten existieren, sehr schwierig. Aus diesen Gründen haben wir uns dazu entschieden ein einfaches Dashboard mit interaktiven Elementen und verschiedenen Filtern zu programmieren. Eventuell können auch Numismatiker von diesem Dashboard profitierern, indem sie eigenständige Analysen durchführen können. Dabei ist das Dashboard in verschiedene Tabs unterteilt.  Diese werden durch einen Help-Tab unterstützt, der  den Umgang mit dem Tool kurz erklärt. Die Tabs sind:
### Coin Explorer
Der Coin Explorer hat das Ziel, die Ergebnisse der Clusteranalyse und insbesondere der UMAP-Dimensionsreduzierung darzustellen. Zentrales Element bildet dabei der erste Plot, bei dem die Ergebnisse der UMAP-Dimensionsreduzierung mit verschiedenen Clustering-Algorithmen dargestellt werden können. Je nachdem welche Punkte über Linksklick und Ziehen im Plot ausgewählt werden, passen sich die anderen Elemente, wie Top10 Entitäten an. Der Coin Explorer ist dafür gedacht in die Daten "rein zu drillen" und zu verstehen, wie sich die Verteilung der einzelnen Punkte und Cluster ergibt. Dabei ist zu beachten, dass je näher Punkte (Münzen) zueinander stehen, desto ähnlichr sind diese auch.
### Entity Explorer
Der Entity Explorer hat das Ziel dne zeitlichen Verlauf von Entitätne aufzuzeigen. Dabei können mit dem oberen Filter einzelne Entitäten ausgewählt werden und miteinander verglichen werden. Insbesondere die Analyse mit Hilfe des Zeitreihenplottes auf diesem Tab bietet die einmalige Möglichkeit unzählige Entitäten gleichzeitig zu analyiseren. Das war auch eines der Hauptargumente dieses Dashboard zu erstellen.
### Coin Finder
Der Coin Finder bietet die Möglichkeit Werte einer Münze für einen gegebenen Datenstaz einzugeben und die ähnlichsten Münzen auf Basis der UMAP-Dimensionsreduzierung auszugeben. Dafür wurde für jeden gegebenen Zeitraum ein Classifier trainiert, welcher für eine Münze die x- und y-Koordinate (im UMAP-Koordinatensystem, siehe Coin Explorer) vorhersagen kann. In der daraus resultierenden Tabelle kann anhand des Feature "dist" bestimmt werden, wie "weit" die eingegebenen Werte von der jeweiligen in der Tabelle aufgeführten Münze entfernt sind. Achtung: Alle Werte müssen gefüllt sein, damit der Classifier damit umgehen kann.
## Zugriff auf das Dashboard
Das Dashboard ist momentan unter https://cnminerva.shinyapps.io/coin/ verfügbar. Die jeweiligen Credentials wurden per Mail versendet oder sind in der Abgabe unter dashboard/frontend/credentials.R zu finden.
Die Performance des gehosteten Dashboards ist jedoch deutlich schlechter, als bei einer lokalen Ausführung. Insbesondere der Entity Explorer läd sehr lange, da über 150.000 Datenpunkte geladen werden müssen. Des Weiteren sollte bei der Nutzung darauf geachtet werden, dass der Ladevorgang der Tabellen und Plots abgeschlossen ist, bevor weitere Veränderungen vorgenommen werden. 
Insofern empfehlen wir das Dashboard lokal zu starten. Um alle notwendigen Packages zu installieren, muss das Skript dashboard/install_all_packages.R ausgeführt werden. Im nächsten Schritt muss die Datei dashboard/frontend/app.R ausgeführt werden. Wichtig: Die notwendigen Daten müssen noch in das Verzeichnis dashboard/frontend/cnn kopiert werden. Um an die Daten zu gelangen, muss der Link aus download_link_for_dashboard_data.txt (nicht auf github) geöffnet und alle Daten heruntergladen werden. 



