#! /usr/bin/env/python
# (C) Fabio D. Steffen

import numpy as np
import re
import os
import sys
if sys.version_info.major < 3:
    import Tkinter, tkFileDialog, tkMessageBox
else:
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
    import tkinter as Tkinter

class Author:
    """
    creates an author instance with attributes: firstname, lastname and firstname_initials
    """
    def __init__(self, name):
        self.name = name.split(", ")
        self.lastname = self.name[0]
        self.firstname = self.name[1]
        self.firstname_initials = " ".join(item[0].upper()+"." for item in self.firstname.split())


def openDialog():
    """
    opens a dialog to choose a BibTeX file from the local drive
    """

    FILEOPENOPTIONS = dict(defaultextension='.bib',filetypes=[('bibtex file','*.bib'), ('All files','*.*')])
    bib_file_path = tkFileDialog.askopenfilename(title="Open .bib file", **FILEOPENOPTIONS)
    path_splitted = os.path.split(os.path.abspath(bib_file_path))
    bib_path = path_splitted[0]
    bib_filename = path_splitted[1]

    return bib_file_path, bib_path, bib_filename


def saveDialog(bib_path, bib_filename):
    """
    opens a dialog to choose a directory and filename to save the .html file on the local drive
    """

    FILEOPENOPTIONS = dict(defaultextension='.html',filetypes=[('html file','*.html'), ('All files','*.*')])
    save_file_path = tkFileDialog.asksaveasfilename(initialdir=bib_path, initialfile=bib_filename.replace('bib','html'), title="Save file as", **FILEOPENOPTIONS)

    return save_file_path

def openBib(bib_file_path):
    """
    reads the .bib file
    """
    with open(bib_file_path) as file:
        data = file.read()
    return data


def parseBibtex(data):
    """
    parses the individual citations from the BibTeX field codes and puts the keys into a dictionary
    """
    citations = data.split("@")
    citehead = []
    for c in citations:
        try:
            citehead.append(re.search("\{([\w*\.[1-9]*)", c).group(1))
        except:
            citehead.append(None)

    citations = [citations[i] for i in range(1,len(citehead)) if citehead != None]
    citehead.remove(None)


    # get bibtex keys
    keywords = ["abstract", "author", "year", "title", "pages", "volume", "doi", "journal", "doi", "magnolia", "badge"]
    citeDict = {}
    for i in range(len(citehead)):
        citeDict[citehead[i]] = {}
        for s in keywords:
            pattern = "(%s = )\"\{(.*?)\}\"" % s

            # if the entries in magnolia or badge are missing do not break
            if s == 'magnolia' or s == 'badge':
                try:
                    citeDict[citehead[i]][s] = re.search(pattern, citations[i]).group(2)
                except:
                    citeDict[citehead[i]][s] = ''
            else:
                try:
                    citeDict[citehead[i]][s] = re.search(pattern, citations[i]).group(2)
                except AttributeError:
                    bibTexKey_errormessage = "bibtex-key '%s' not found in citation '%s', no HTML file is written..." % (s, citehead[i])
                    details = '{}\nmatching pattern: {}'.format(citations[i], pattern)
                    tkMessageBox.showwarning("BibTex-key missing", bibTexKey_errormessage, detail=details)
                    print(bibTexKey_errormessage)
                    return citehead, None 
    return citehead, citeDict


def formatAuthor(citehead, citeDict):
    """
    extracts all authors from the citation and formats them according to the style: <lastname_author1>, <firstname_author1>; <lastname_author2>, <firstname_author2>
    """
    firstauthor = {}
    authorblock = {}
    for c in citehead:

        # generate author instances
        authorList = citeDict[c]["author"].split(" and ")
        authors = []
        for authorname in authorList:
            authorname = authorname.replace("{","").replace("}","") # {} surround multiple last names in bibtex file
            authors.append(Author(authorname))

        # format author block
        author_formatted = []
        firstauthor[c] = authors[0].lastname
        for author in authors:
            #author_formatted.append("%s %s" % (author.firstname_initials, author.lastname))
            author_formatted.append("%s, %s" % (author.lastname, author.firstname))

        authorblock[c] = "; ".join(author_formatted)
    return authorblock, firstauthor


def compileCitation(citehead, citeDict, authorblock, firstauthor, magnolia_prefix='/dam/jcr:'):
    """
    compiles the citation (sorted by year in alphabetic order) using html formatting
    """
    years = [int(citeDict[key]["year"]) for key in citehead]
    citehead = [c for _,c in sorted(zip(years,citehead))]

    # split the citations into years (newest first)
    yearSet = sorted(set(years), reverse=True)
    citeheadYear = {year: [citehead[i] for i, x in enumerate(sorted(years)) if x == year] for year in yearSet}

    # compile the individual citations sorted by year (newest first)
    citationHTML = []
    yearTOC = []
    for year in yearSet:
        citationYear = []
        citationsperyear = len(citeheadYear[year])
        count = 1
        for c in citeheadYear[year]:

            # create a unique ID for each citation
            citationID = "%s_%s_%s_%s" % (firstauthor[c], citeDict[c]["journal"], citeDict[c]["year"], citeDict[c]["pages"])
            citationID = citationID.replace(" ", "").replace(".", "")

            # format article citation with HTML code
            citation = "<div><button class='noBG pointer' onclick='showAbstract(\"%s\")'><p class='citation title'>%s</p>\n<p class='citation'>%s, <i>%s</i> %s, <i>%s</i>, %s.</p></div><div><p class='doi'>DOI: <a href=\"http://dx.doi.org/%s\" target=\"_blank\">%s</a><p><img src='%s%s' onerror=\"this.style.display='none'\"/ alt=''></button></div>\n<div id='%s' style='display:none;'><img src='%s%s' onerror=\"this.style.display='none'\"/ alt=''>\n<p class='abstract'>%s</p></div>\n" % (citationID, citeDict[c]["title"], authorblock[c], citeDict[c]["journal"], citeDict[c]["year"], citeDict[c]["volume"], citeDict[c]["pages"].replace("--","-"), citeDict[c]["doi"], citeDict[c]["doi"], magnolia_prefix, citeDict[c]["badge"], citationID, magnolia_prefix, citeDict[c]["magnolia"], citeDict[c]["abstract"])

            # include a dotted line between publications of the same year
            if count != citationsperyear:
                citation = "%s\n<p class='dottedLine'></p>" % citation

            citationYear.append(citation)
            count += 1

        # combine the citations by year
        citationYear = "\n".join(citationYear)
        citationHTML.append("<div><h2 id='%s'>%s</h2></div>\n%s" % (year, year, citationYear))

        yearTOC.append("<a href='#%s'>%s</a>" % (year, year))


    # combine all citations
    citationHTML = "\n".join(citationHTML)
    yearTOC = "\n".join(yearTOC)
    return citationHTML, yearTOC


def createHTML(bib_path, bib_filename, yearTOC, citationHTML):
    """
    writes the html file to the directory where the BibTeX file is located
    """

    # javascript function for abstract unfolding
    scriptHTML = "<script>\nfunction showAbstract(citationID){\nvar x = document.getElementById(citationID);\nif (x.style.display === 'none'){\nx.style.display = 'block';\n} else {\nx.style.display = 'none';}}\n</script>\n"

    # write html file
    html_file_path = saveDialog(bib_path, bib_filename)
    if html_file_path != '':
        out = open(html_file_path,"w")
        out.write("<!DOCTYPE html>\n<meta charset='UTF-8'>\n<html>\n")
        out.write("<head>\n<style>\np {font-family: Arial, Helvetica, FreeSans, sans-serif; font-size: 12px;}\nh2 {font-family: Arial, Helvetica, FreeSans, sans-serif; margin-top: 1.5em !important; margin-bottom: 0.5em !important;}\n.citation{margin-top: 0em !important; margin-bottom: 0em !important;}\n.doi{margin-top: 0em !important; margin-bottom: 0.5em !important;}\n.abstract{margin-top: 0.5em !important; margin-bottom: 1.8em !important;}\n.title{font-weight: bold;}\n.noBG{background-color: transparent; border: 0; padding: 0; text-align: left;font-size: 12px;}\n.dottedLine{border-bottom: 1px dotted; margin-top: 0em; margin-bottom: 1em;}\n.pointer{cursor: pointer;}\n</style>\n</head>\n<body>\n")
        out.write(yearTOC+"\n")
        out.write(citationHTML)
        out.write(scriptHTML)
        out.write("</body>\n</html>")


if __name__ == "__main__":
    # file selection dialog
    root = Tkinter.Tk()
    root.withdraw()

    bib_file_path, bib_path, bib_filename = openDialog()
    if bib_file_path != '':
        data = openBib(bib_file_path)
        citehead, citeDict = parseBibtex(data)
        if citeDict is not None:
            authorblock, firstauthor = formatAuthor(citehead, citeDict)
            citationHTML, yearTOC = compileCitation(citehead, citeDict, authorblock, firstauthor)
            createHTML(bib_path, bib_filename, yearTOC, citationHTML)
