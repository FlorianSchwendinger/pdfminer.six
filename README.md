# pdfminer.six - branch

This branch of **pdfminer.six** adds highlevel functions to retrive the data 
as a pandas **DataFrame**. Currently the additional functions in this
branch are only a subset of the functionality provided in [`pdfmole`](https://github.com/FlorianSchwendinger/pdfmole).

```python
from pdfminer import pdf
```
## Read the PDF-document
```python
doc = pdf.read_all("../samples/cars.pdf")
doc
#py> A pdf document with 10 pages.
```

## Get elements
```python
doc.list_elements()
#py> ['metainfo', 'text', 'line', 'rect', 'curve', 'figure', 'textline', 'textbox', 'textgroup', 'image']
```
By default all elments are returned as **DataFrame**.
```python
doc.get_metainfo()
#py>    pid  rotate  x0  y0   x1   y1
#py> 0    1       0   0   0  595  842
#py> 1    2       0   0   0  595  842

doc.get_text().head()
#py>    pid  block text          font  ...     x0       y0     x1       y1
#py> 0    1    1.0    s  Courier-Bold  ...   77.2  751.272   84.4  763.272
#py> 1    1    1.0    p  Courier-Bold  ...   84.4  751.272   91.6  763.272
#py> 2    1    1.0    e  Courier-Bold  ...   91.6  751.272   98.8  763.272
#py> 3    1    1.0    e  Courier-Bold  ...   98.8  751.272  106.0  763.272
#py> 4    1    1.0    d  Courier-Bold  ...  106.0  751.272  113.2  763.272
#py> 
#py> [5 rows x 11 columns]

doc.get_line()
#py> Empty DataFrame
#py> Columns: [pid, linewidth, x0, y0, x1, y1]
#py> Index: []

doc.get_rect()
#py> Empty DataFrame
#py> Columns: [pid, linewidth, x0, y0, x1, y1]
#py> Index: []

doc.get_curve()
#py> Empty DataFrame
#py> Columns: [pid, linewidth, pts, x0, y0, x1, y1]
#py> Index: []

doc.get_figure()
#py> Empty DataFrame
#py> Columns: [pid, name, x0, y0, x1, y1]
#py> Index: []

doc.get_textline().head()
#py>    pid     x0       y0      x1       y1
#py> 0    1   77.2  751.272  153.20  763.272
#py> 1    1  288.2  772.590  307.09  782.590
#py> 2    1   67.9  736.272   75.10  748.272
#py> 3    1   67.9  721.272   75.10  733.272
#py> 4    1   67.9  706.272   75.10  718.272

doc.get_textbox().head()
#py>    pid  id       wmode     x0       y0      x1       y1
#py> 0    1   0  horizontal   77.2  751.272  153.20  763.272
#py> 1    1   1  horizontal  288.2  772.590  307.09  782.590
#py> 2    1   2  horizontal   60.7   91.472   75.10  748.272
#py> 3    1   3  horizontal  108.0   91.472  122.40  748.272
#py> 4    1   4  horizontal  147.6   91.472  162.00  748.272

doc.get_textgroup().head()
#py>    pid     x0       y0      x1       y1
#py> 0    1   60.7   58.290  313.46  782.590
#py> 1    1   60.7   91.472  307.09  782.590
#py> 2    1   77.2  751.272  307.09  782.590
#py> 3    1   60.7   91.472  162.00  748.272
#py> 4    1  108.0   91.472  162.00  748.272

doc.get_image()
#py> Empty DataFrame
#py> Columns: [pid, src, width, height]
#py> Index: []
```

But it is also possible the get the elemens as a list of dictionaries.
```python
doc.get_metainfo("list")
#py> [{'pid': 1, 'rotate': 0, 'x0': 0, 'y0': 0, 'x1': 595, 'y1': 842},
#py>  {'pid': 2, 'rotate': 0, 'x0': 0, 'y0': 0, 'x1': 595, 'y1': 842}]
```

Group the characters based on the blocks detected by **pdfminer.six**.
```python
x = doc.get_text()
pdf.group_blocks(x).head()
#py>    pid   text                   font  size  ...     x0       y0      x1       y1
#py> 0    1  speed           Courier-Bold  12.0  ...   77.2  751.272  113.20  763.272
#py> 1    1   dist           Courier-Bold  12.0  ...  124.4  751.272  153.20  763.272
#py> 2    1   cars  BAAAAA+LiberationSans  10.0  ...  288.2  772.590  307.09  782.590
#py> 3    1      1                Courier  12.0  ...   67.9  736.272   75.10  748.272
#py> 4    1      2                Courier  12.0  ...   67.9  721.272   75.10  733.272
#py> 
#py> [5 rows x 10 columns]
```	

# pdfminer.six

[![Build Status](https://travis-ci.org/pdfminer/pdfminer.six.svg?branch=master)](https://travis-ci.org/pdfminer/pdfminer.six)
[![PyPI version](https://img.shields.io/pypi/v/pdfminer.six.svg)](https://pypi.python.org/pypi/pdfminer.six/)
[![gitter](https://badges.gitter.im/pdfminer-six/Lobby.svg)](https://gitter.im/pdfminer-six/Lobby?utm_source=badge&utm_medium)

Pdfminer.six is a community maintained fork of the original PDFMiner. It is a
tool for extracting information from PDF documents. It focuses on getting
and analyzing text data. Pdfminer.six extracts the text from a page directly
from the sourcecode of the PDF. It can also be used to get the exact location, 
font or color of the text. 

It is build in a modular way such that each component of pdfminer.six can be
replaced easily. You can implement your own interpreter or rendering device
to use the power of pdfminer.six for other purposes that text analysis. 

Check out the full documentation on
[Read the Docs](https://pdfminersix.readthedocs.io).


## Features

 * Written entirely in Python.
 * Parse, analyze, and convert PDF documents.
 * PDF-1.7 specification support. (well, almost).
 * CJK languages and vertical writing scripts support.
 * Various font types (Type1, TrueType, Type3, and CID) support.
 * Support for extracting images (JPG, JBIG2 and Bitmaps).
 * Support for RC4 and AES encryption.
 * Table of contents extraction.
 * Tagged contents extraction.
 * Automatic layout analysis.


## How to use

 * Install Python 3.4 or newer
 * Install

    `pip install pdfminer.six`

 * Use command-line interface to extract text from pdf:

    `python pdf2txt.py samples/simple1.pdf`


## Contributing

Be sure to read the [contribution guidelines](https://github.com/pdfminer/pdfminer.six/blob/master/CONTRIBUTING.md). 
