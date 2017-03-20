This script takes a PDF file (as an argument) and renames that file in place with information from its metadata.
The script depends on [PDFMiner.six](hhttps://github.com/pdfminer/pdfminer.six "PDFMiner.six").

Options:

* `--verbose` print a message saying what was done
* `--truncate` subtitles will be abbreviated
* `--surname` if the author field has multiple words the last will be used
* `--date` the creation date of the PDF will be included in ISO format
* `--getdate` a file must be provided; if it has a YAML block with a date field that will be used as the date (in ISO format)
* `--prepend` text to add before the new name
* `--append` text to add after the new name
