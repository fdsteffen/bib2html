import unittest
import bib2html

import os 
test_path = os.path.dirname(os.path.realpath(__file__))

class BibtexTest(unittest.TestCase):
    def test_missingEntry(self):
        data = bib2html.openBib(test_path+'/bibtex_missingEntry.bib')
        citehead, citeDict = bib2html.parseBibtex(data)
        self.assertRaises(AttributeError)

    def test_missingQuotationMark(self):
        data = bib2html.openBib(test_path+'/bibtex_missingquotationmarks.bib')
        citehead, citeDict = bib2html.parseBibtex(data)
        self.assertRaises(AttributeError)

    def test_Watson(self):
        data = bib2html.openBib(test_path+'/bibtex_Watson.bib')
        citehead, citeDict = bib2html.parseBibtex(data)
        authorblock, firstauthor = bib2html.formatAuthor(citehead, citeDict)
        self.assertEqual(firstauthor[citehead[0]], 'Watson')

if __name__ == "__main__":
    unittest.main()
