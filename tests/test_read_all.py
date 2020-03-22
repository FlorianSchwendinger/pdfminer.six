#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:34:19 2020

@author: florian
"""

import os
from pdfminer import pdf
import pandas as pd
import numpy as np

f = "../samples/cars.pdf"
os.path.exists(f)


doc = pdf.read_all(f)
doc

doc.list_elements()
doc.get_metainfo()
doc.get_text().head()
doc.get_rect()
doc.get_textbox().head()


x = doc.get_text()
pdf.group_blocks(x)
