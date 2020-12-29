import sys
import os

sys.path.insert(0, os.path.abspath('../../'))

project = 'bib2html'
copyright = '2020, Fabio Steffen'
author = 'Fabio Steffen'
release = '1.0.0'

extensions = [
]
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
html_show_sourcelink = False

html_theme_options = {
    'font_family': 'Open Sans',
    'logo':'logo.png',
    }

html_sidebars = {
    '**': [
        'about.html',
    ]
}

extensions = [    
    'sphinx.ext.githubpages',
]
