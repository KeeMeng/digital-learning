import fitz

pages = int(input("Pages: "))
count = 1
doc2 = fitz.open("template.pdf")
while count < pages:
    doc = fitz.open("template.pdf")
    doc.insertPDF(doc2)
    doc.save("template2.pdf")
    doc2 = fitz.open("template2.pdf")
    count += 1
