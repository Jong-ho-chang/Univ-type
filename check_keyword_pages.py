import fitz

pdf_path = "data/input.pdf"
keywords = ['고려대', '연세대', '성균관대']
doc = fitz.open(pdf_path)

found = {kw: False for kw in keywords}
for i, page in enumerate(doc):
    text = page.get_text()
    for kw in keywords:
        if kw in text:
            print(f"🔍 '{kw}' appears on page {i+1}")
            print(f"✅ '{kw}' found on page {i+1}")
            found[kw] = True

for kw, was_found in found.items():
    if not was_found:
        print(f"⚠️ '{kw}' not found in any page.")