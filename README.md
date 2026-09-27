# Convertitore file da XML a PDF
Applicazione desktop sviluppata in Python per convertire i dati contenuti in un file XML in un report PDF.
Il programma utilizza una semplice interfaccia grafica realizzata con Tkinter, che permette di selezionare il file XML da convertire e il percorso in cui salvare il PDF generato.

## Funzionalità principali
- Selezione del file XML tramite finestra di dialogo
- Selezione del percorso di salvataggio del PDF
- Conversione del file XML in un file PDF

## Gestione degli errori
- mancata selezione del file XML
- mancata indicazione del percorso per il salvataggio del file PDF 
- file XML non valido
- file XML inesistente
- impossibilità di scrivere il PDF

# Requisiti
Utilizzare la seguente versione di Python:
- versione 3.13.3

# Avvio applicazione
python main.py oppure py main.py

# Tecnologie utilizzate
- Tkinter
- xml.etree.ElementTree
- ReportLab