def redact_pii_in_pdf(doc, pii_list):
    for page in doc:
        for text, _ in pii_list:
            instances = page.search_for(text)
            for inst in instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()
    
    output_path = "docs/redacted_output.pdf"
    doc.save(output_path)
    return output_path
