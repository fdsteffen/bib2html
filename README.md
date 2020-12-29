# ![](docs/source/_static/logo.png)

## Quickstart

*Bib2HTML* is a Python script to convert bibtex files to an HTML-formatted reference list ordered by year and first author. See an example [here](https://fdsteffen.github.io/bib2html)

[](docs/source/_static/Watson.png)

The bibtex entries should be formatted as follows:
```
@article{Watson.1953,
 author = "{Watson, J. D. and Crick, F. H. C.}",
 year = "{1953}",
 title = "{Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid}",
 journal = "{Nature}",
 volume = "{171}",
 pages = "{737--738}",
 abstract = "{We wish to suggest a structure of the salt of deoxyribose nucleic acid (D.N.A.). This structure has novel features which are of considerable biological interest.}",
 doi = "{10.1038/171737a0}"
}
```

If you wish to include a graphical abstract then the following key should be specified in addition:
```
 magnolia = "{uniqueImageIdentifier}",
```
The `uniqueImageIdentifier` should point to the location of the image on a file server or on the local disk.

Convert the bibtex file into a HTML file using *Bib2HTML*
```
python bib2html.py
```


## Dependencies
- Python 2.7, 3 or higher
- numpy
- tkinter

## Export bibtex files from Citavi

> Note: In Citavi, make sure that all citations have a **periodical entry** that includes the full name of the journal (name) and an abbreviation with dots (abbreviation 1)

- upload a graphical abstract (in .jpg or .png format) to the Content Managment system (CMS) and copy the unique Magnolia Assets Identifier into the *Custom field 1* entry of Citavi
- export the bibtex file as follows:

  * select all citations that should be exported
  * go to ``File`` → ``Export`` → ``Export...`` choose *the selected reference* → BibTeX
  * untick both *Place capital letters in braces* and *Use LaTeX notation*
  * click on *Edit BibTeX export definition* : no changes need to be made on ``Map reference types``
  * on ``Map fields`` choose *Journal article*, write *magnolia* into *Custom field 1* and move the *journal* entry from *Periodical: Name* to *Periodical: Abbreviation1*
  * on ``Options`` make sure that *Use LaTeX notation* and *Place capital letters in braces* are unticked; choose *Quotation marks and parentheses* as field delimiter
  * give a name to the export format e.g. "BibTeX_journal_abbreviated"
  * choose a name for the exported bibtex file
  * if you wish, give a name to the export definition for future use
