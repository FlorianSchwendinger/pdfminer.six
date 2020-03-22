#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:34:19 2020

@author: florian
"""

from pdfminer import pdf

# Read the document
doc = pdf.read_all("../samples/cars.pdf")
doc

# Get elements
doc.list_elements()
# By default all elments are returned as **DataFrame**.
doc.get_metainfo()
doc.get_text().head()
doc.get_line()
doc.get_rect()
doc.get_curve()
doc.get_figure()
doc.get_textline().head()
doc.get_textbox().head()
doc.get_textgroup()
doc.get_image()

# But it is also possible the get the elemens as list of dictionaries.
doc.get_metainfo("list")

x = doc.get_text()
pdf.group_blocks(x).head()


