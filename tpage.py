import random as r

def getHTMLcode(prog):
    htmlCode = ""
    for key,value in prog.items():
        value = value.replace("\\n","<br>")
        if key == "title":
            htmlCode += "<h1>"
            htmlCode += value
            htmlCode += "</h1>"
            continue
        if key.endswith("Image"):
            htmlCode += f"<img src='{value}' width=300>"
            continue
        if key.endswith("Text"):
            htmlCode += "<p>"
            htmlCode += value
            htmlCode += "</p>"
            continue
        if key.endswith("RandC"):
            values = value.split(",")
            htmlCode += "<p>"
            if key+"Name" in prog:
                htmlCode += prog[key+"Name"]
            htmlCode += r.choice(values)
            htmlCode += "</p>"
            continue
        if key.endswith("RandRange"):
            values = value.split(",")
            htmlCode += "<p>"
            if key+"Name" in prog:
                htmlCode += prog[key+"Name"]
            htmlCode += str(r.randint(int(values[0]),int(values[1])))
            htmlCode += "</p>"
            continue
    return htmlCode

def parse(string):
    parsed = {}
    spl = string.split(";")
    for line in spl:
        if line == "":
            continue
        pLine = line.split("=")
        parsed[pLine[0]] = pLine[1]
    return parsed