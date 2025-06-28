import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz
import spacy
import re
import os
import csv
import webbrowser

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Regex patterns
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_PATTERN = r'\b\d{10}\b'
AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'
PAN_PATTERN = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'

# App setup
root = tk.Tk()
root.title("Sensitive Document Auto-Sanitizer")
root.geometry("1000x700")
dark_mode = [False]

# Ensure docs folder exists
def ensure_docs_folder():
    if not os.path.exists("docs"):
        os.makedirs("docs")

# Redact logic
def redact_text(text):
    doc = nlp(text)
    entities = []

    if var_person.get():
        entities += [(ent.text, "PERSON") for ent in doc.ents if ent.label_ == "PERSON"]
    if var_gpe.get():
        entities += [(ent.text, "GPE") for ent in doc.ents if ent.label_ == "GPE"]
    if var_email.get():
        entities += [(e, "EMAIL") for e in re.findall(EMAIL_PATTERN, text)]
    if var_phone.get():
        entities += [(p, "PHONE") for p in re.findall(PHONE_PATTERN, text)]
    if var_aadhaar.get():
        entities += [(a, "AADHAAR") for a in re.findall(AADHAAR_PATTERN, text)]
    if var_pan.get():
        entities += [(p, "PAN") for p in re.findall(PAN_PATTERN, text)]

    redacted = text
    for ent, _ in entities:
        redacted = redacted.replace(ent, "[REDACTED]")

    return redacted, entities

# Logging
def log(message):
    log_box.insert(tk.END, f"> {message}\n")
    log_box.see(tk.END)

# Apply dark/light mode
def apply_theme():
    bg = "#2E2E2E" if dark_mode[0] else "#f5f5f5"
    fg = "#FFFFFF" if dark_mode[0] else "#000000"
    style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg)
    style.configure("Treeview.Heading", background="#444444" if dark_mode[0] else "#B0C4DE", foreground="white")
    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass
    log("Dark Mode On" if dark_mode[0] else "Light Mode On")

# Dark mode toggle
def toggle_dark_mode():
    dark_mode[0] = not dark_mode[0]
    apply_theme()

# Upload PDF and process
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    ensure_docs_folder()
    log("Reading PDF...")
    original_doc = fitz.open(file_path)
    text = "".join(page.get_text() for page in original_doc)

    log("Extracting entities...")
    redacted_text, entities = redact_text(text)

    log("Redacting PDF...")
    redacted_doc = fitz.open()
    for page in original_doc:
        new_page = redacted_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_text((72, 72), redacted_text, fontsize=10)

    redacted_path = "docs/redacted_output.pdf"
    redacted_doc.save(redacted_path)
    redacted_doc.close()
    original_doc.close()

    log("Filling table...")
    clear_table()
    for ent, typ in entities:
        tree.insert("", "end", values=(ent, typ))

    log("Saving entity CSV...")
    with open("docs/entities_summary.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entity", "Type"])
        writer.writerows(entities)

    status_label.config(text=f"Redacted saved: {redacted_path}")
    log("Saved redacted PDF and CSV.")

# Open redacted PDF
def open_redacted_pdf():
    path = "docs/redacted_output.pdf"
    if os.path.exists(path):
        webbrowser.open_new(path)
    else:
        messagebox.showerror("Error", "No redacted PDF found.")

# Preview PDF content
def preview_pdf_pages():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not path:
        return
    doc = fitz.open(path)
    text = ""
    for i, page in enumerate(doc, 1):
        text += f"\n--- Page {i} ---\n" + page.get_text()
    doc.close()

    preview_window = tk.Toplevel(root)
    preview_window.title("PDF Preview")
    preview_window.geometry("800x600")
    txt = tk.Text(preview_window, wrap=tk.WORD, font=("Courier", 10))
    txt.insert(tk.END, text)
    txt.pack(fill="both", expand=True)

# Filter table
def filter_entities(event=None):
    key = search_var.get().lower()
    for row in tree.get_children():
        values = tree.item(row)["values"]
        entity_text = str(values[0]).lower()
        entity_type = str(values[1]).lower()
        if key in entity_text or key in entity_type:
            tree.item(row, tags=("match",))
        else:
            tree.item(row, tags=("no_match",))
    tree.tag_configure("match", background="#3B9C9C", foreground="white")
    tree.tag_configure("no_match", background="#2E2E2E" if dark_mode[0] else "#f5f5f5", foreground="#999999")

# Clear filters
def clear_highlights():
    search_var.set("")
    for row in tree.get_children():
        tree.item(row, tags=("show",))
    tree.tag_configure("show", background="#2E2E2E" if dark_mode[0] else "#f5f5f5", foreground="white" if dark_mode[0] else "black")

# Clear table
def clear_table():
    for row in tree.get_children():
        tree.delete(row)
    status_label.config(text="Table cleared.")
    log("Entity table cleared.")

# === GUI ===
style = ttk.Style()
style.theme_use("clam")

# Top buttons
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

btns = [
    ("Upload PDF", upload_pdf, "#4682B4"),
    ("Preview PDF", preview_pdf_pages, "#6A5ACD"),
    ("Open Redacted PDF", open_redacted_pdf, "#2E8B57"),
    ("Clear Table", clear_table, "#D2691E"),
    ("Toggle Dark Mode", toggle_dark_mode, "#444444"),
    ("Reset Filter", clear_highlights, "#808080"),
]

for i, (text, cmd, color) in enumerate(btns):
    tk.Button(top_frame, text=text, command=cmd, bg=color, fg="white").grid(row=0, column=i, padx=5)

# Checkboxes
check_frame = tk.Frame(root)
check_frame.pack(pady=5)

var_person = tk.BooleanVar(value=True)
var_gpe = tk.BooleanVar(value=True)
var_email = tk.BooleanVar(value=True)
var_phone = tk.BooleanVar(value=True)
var_aadhaar = tk.BooleanVar(value=True)
var_pan = tk.BooleanVar(value=True)

check_vars = [
    ("PERSON", var_person),
    ("GPE", var_gpe),
    ("EMAIL", var_email),
    ("PHONE", var_phone),
    ("AADHAAR", var_aadhaar),
    ("PAN", var_pan),
]

for i, (text, var) in enumerate(check_vars):
    tk.Checkbutton(check_frame, text=text, variable=var).grid(row=0, column=i, padx=5)

# Search
search_var = tk.StringVar()
search_box = tk.Entry(root, textvariable=search_var, width=50)
search_box.pack(pady=5)
search_box.bind("<KeyRelease>", filter_entities)
search_box.insert(0, "Search entity or type...")

# Table
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=5, fill="both", expand=True)

tree = ttk.Treeview(table_frame, columns=("Entity", "Type"), show="headings")
tree.heading("Entity", text="Extracted Entity")
tree.heading("Type", text="Type")
tree.column("Entity", width=600)
tree.column("Type", width=100)
tree.pack(fill="both", expand=True)

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")

# Log box
log_box = tk.Text(root, height=6, bg="#1e1e1e" if dark_mode[0] else "#f0f0f0", fg="white" if dark_mode[0] else "black")
log_box.pack(fill="both", expand=True, padx=10, pady=5)

# Status label
status_label = tk.Label(root, text="Ready", fg="green", bg="#2E2E2E" if dark_mode[0] else "#f5f5f5")
status_label.pack(pady=5)

apply_theme()

root.mainloop()
