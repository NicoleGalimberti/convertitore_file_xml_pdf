import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET 
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  
from reportlab.lib import colors
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent
WINDOW_SIZE = "600x500"
BG = "#F5F5F5"
FONT = ("Arial", 10)
ENCODING= "utf-8"
FAVICON = FILE_PATH / "icona_conv.ico"
PADDING_Y = 5

root = tk.Tk()
root.title("Convertitore XML - PDF")
root.geometry(WINDOW_SIZE)
root.configure(bg=BG)
root.iconbitmap(FAVICON)

def addWidget(element):
    element.pack(pady = PADDING_Y)

def seleziona_xml():
    file_path = filedialog.askopenfilename(title="Seleziona file XML", filetypes=[("XML Files", "*.xml")])
    entry_file_xml.delete(0, tk.END) 
    entry_file_xml.insert(0, file_path)

def salva_pdf():
    file_path = filedialog.asksaveasfilename(title="Salva PDF come", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    entry_file_pdf.delete(0, tk.END)
    entry_file_pdf.insert(0, file_path)

def conversione():
    xml_file = entry_file_xml.get().strip()
    pdf_file = entry_file_pdf.get().strip()
    if not xml_file or not pdf_file:
        messagebox.showwarning("Attenzione", "Selezionare sia il file XML che il percorso per il PDF.")
        return
    if not Path(xml_file).exists():
        messagebox.showerror("Errore", "Il file XML selezionato non esiste.")
        return
    if not xml_file.lower().endswith(".xml"):
        messagebox.showerror("Errore", "Il file selezionato non è valido.")
        return
    if not pdf_file.lower().endswith(".pdf"):
        messagebox.showerror("Errore", "Il file PDF deve avere estensione .pdf")
        return
    xml_a_pdf(xml_file, pdf_file)

def xml_a_pdf(xml_file, pdf_file):
    try:
        with open(xml_file, "r", encoding= ENCODING) as file:
            xml_contenuto= file.read()
        xml_root = ET.fromstring(xml_contenuto)
        
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading1']

        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []

        elements.append(Paragraph("Report di Produzione", title_style))
        elements.append(Spacer(1, 12))

        header = xml_root.find('Report_Header')
        if header is not None:
            elements.append(Paragraph("Intestazione Report", heading_style))
            data_header = []
            for child in header:
                data_header.append([child.tag, child.text or ""])
            table_header = Table(data_header, colWidths=[150, 250])
            table_header.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black), 
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey) 
            ]))
            elements.append(table_header)
            elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph("Nessun dato disponibile", styles['Normal']))

        production = xml_root.find('Production')
        if production is not None:
            elements.append(Paragraph("Dati di Produzione", heading_style))
            data_prod = []
            for child in production:
                data_prod.append([child.tag, child.text or ""])
            table_prod = Table(data_prod, colWidths=[150, 250])
            table_prod.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
            ]))
            elements.append(table_prod)
        else:
            elements.append(Paragraph("Nessun dato disponibile", styles['Normal']))
        try:
            doc.build(elements) 
        except PermissionError:
            messagebox.showerror("Errore", "Impossibile scrivere il PDF.\nChiudere il file se è già aperto e riprovare.")  
            return  
        messagebox.showinfo("Successo", f"PDF creato: {pdf_file}")
    except ET.ParseError:
        messagebox.showerror("Errore", "Impossibile convertire il file")
        return

file_xml = tk.Label(root, text="File XML:", font=(FONT, 12))
addWidget(file_xml)
entry_file_xml = tk.Entry(root, width=80)
addWidget(entry_file_xml)
button_file_xml = tk.Button(root, text="Sfoglia", font=(FONT), command=seleziona_xml)
addWidget(button_file_xml)

file_pdf = tk.Label(root, text="File PDF:", font=(FONT, 12))
addWidget(file_pdf)
entry_file_pdf = tk.Entry(root, width=80)
addWidget(entry_file_pdf)
button_file_pdf = tk.Button(root, text="Salva come", font=(FONT), command=salva_pdf)
addWidget(button_file_pdf)

convert_button = tk.Button(root, text="Converti in PDF", command=conversione, bg="#036C03", font= FONT, fg="#F5F5F5")
addWidget(convert_button)

root.mainloop()