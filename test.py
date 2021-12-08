import difflib

html_diff = difflib.HtmlDiff()

with open("test.html", "r") as handler:
    file1 = handler.readlines()

with open("test2.html", "r") as handler:
    file2 = handler.readlines()

text = html_diff.make_file(fromlines=file1, tolines=file2, )
with open("final.html", "w") as handler:
    handler.write(text)

# differ = difflib.Differ()
# text = differ.compare(file1, file2)
# pprint(list(text))
