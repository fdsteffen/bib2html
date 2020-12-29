## Changelog

### [1.0.0] 2020-12-29
#### Added
- Initial release of Bib2HTML
- Github page with demo citations

#### Fixed 
- Remove forward slash from the magnolia identifier again to allow Github pages to find the image 


### [0.9.0] 2020-03-04
#### Added
- Add error details to messagebox if bibkey is not found
- Add python 3 support, 
- Add save dialog
- Convert cursor to pointer when hovering over citation
- Wrap the code into modules
- Add <pages> to the citationID to distinguish entries in the same journal in the same year by the same first author

#### Fixed 
- Add forward slash to the magnolia identifier; 
- Add error exception if graphical abstract or badge is missing
- Changed the field code delimiter from {} to "{}"