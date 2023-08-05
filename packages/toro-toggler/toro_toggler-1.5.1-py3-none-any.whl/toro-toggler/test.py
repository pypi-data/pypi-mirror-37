import markdown

md = markdown.Markdown(extensions=["toro-toggler","codehilite","pymdownx.superfences","markdown.extensions.tables"])
print("\n")
with open('/Users/jerrick.pua/Desktop/togglerBug/togglermessy.txt', 'r') as content_file:
    content = content_file.read()
    print(md.convert(content))