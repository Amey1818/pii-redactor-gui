import spacy
import re

nlp = spacy.load("en_core_web_sm")

def detect_pii(text):
    doc = nlp(text)
    pii_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ['PERSON', 'GPE', 'ORG']]
    emails = re.findall(r'\S+@\S+', text)
    phones = re.findall(r'\b\d{10}\b', text)

    pii = pii_entities + [(email, 'EMAIL') for email in emails] + [(phone, 'PHONE') for phone in phones]
    return pii
