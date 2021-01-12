from pdf2image import convert_from_path, convert_from_bytes
images = convert_from_path(input())
images.save("pdf.png")

##from pdf2image import convert_from_path, convert_from_bytes
##uploaded_image = "/Users/TanKeeMeng/Downloads/oxbridge project/CP1 Review Exercise 1.pdf"
##file_name = str(uploaded_image).replace('.pdf','')
##output_file = file_name+'.png'
##pages = convert_from_path(uploaded_image, 200)
##for page in pages:
##    page.save(output_file, 'PNG')
##    break
##os.chdir(project_dir)
##img = Image.open(output_file)
##img = img.resize(img_size, PIL.Image.ANTIALIAS)
##img.save(output_file)


