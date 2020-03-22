#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 08:46:25 2020

@author: florian

This is copied from pdfmole (<https://github.com/FlorianSchwendinger/pdfmole>)
from the file "pdfmole/inst/python/pdf2list.py".

  
"""

import os
import json

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFLayoutAnalyzer
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams, LTPage, LTText, LTLine, LTRect, LTCurve, LTFigure, LTImage, \
    LTChar, LTTextLine, LTTextBox, LTTextGroup, LTTextBoxVertical
from pdfminer.utils import enc
from pdfminer.pdfpage import PDFPage

import pandas as pd

class PDF2Converter(PDFLayoutAnalyzer):
    def __init__(self, rsrcmgr, codec='utf-8', pageno=1, laparams=None):
        PDFLayoutAnalyzer.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.codec = codec
        return
  

class XML2Converter(PDF2Converter):

    def __init__(self, rsrcmgr, codec='utf-8', pageno=1, laparams=None, imagewriter=None, 
                 stripcontrol=False):
        PDF2Converter.__init__(self, rsrcmgr, codec=codec, pageno=pageno, laparams=laparams)
        self.imagewriter = imagewriter
        self.stripcontrol = stripcontrol
        self.doc = list()
        self.page = None
        
        return

    def receive_layout(self, ltpage):
        def show_group(item):
            if isinstance(item, LTTextGroup):
                self.page['textgroup'].append({'x0': item.bbox[0], 'y0': item.bbox[1], 
                                               'x1': item.bbox[2], 'y1': item.bbox[3]})
                for child in item:
                    show_group(child)
            return

        def render(item):
            if isinstance(item, LTPage):
                metainfo = {'pid': item.pageid, 'rotate': item.rotate, 'x0': item.bbox[0], 
                            'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]}
                self.page = {'metainfo': metainfo, 'text': [], 'line': [], 'rect': [], 'curve': [], 
                             'figure': [], 'textline': [], 'textbox': [], 'textgroup': [], 
                             'image': []}

                for child in item:
                    render(child)
                
                if item.groups is not None:
                    for group in item.groups:
                        show_group(group)
                
                self.doc.append(self.page)
            elif isinstance(item, LTLine):
                self.page['line'].append({'linewidth': item.linewidth, 'x0': item.bbox[0], 
                                          'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]})
            elif isinstance(item, LTRect):
                self.page['rect'].append({'linewidth': item.linewidth, 'x0': item.bbox[0], 
                                          'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]})
            elif isinstance(item, LTCurve):
                curve = {'linewidth': item.linewidth, 'pts': item.get_pts(), 'x0': item.bbox[0], 
                         'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]}
                self.page['curve'].append(curve)
            elif isinstance(item, LTFigure):
                self.page['figure'].append({'name': item.name, 'x0': item.bbox[0], 
                                            'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]})
                for child in item:
                    render(child)
            elif isinstance(item, LTTextLine):
                self.page['textline'].append({'x0': item.bbox[0], 'y0': item.bbox[1], 
                                              'x1': item.bbox[2], 'y1': item.bbox[3]})
                for child in item:
                    render(child)
            elif isinstance(item, LTTextBox):
                wmode = 'vertical' if isinstance(item, LTTextBoxVertical) else 'horizontal'
                tb = {'id': item.index, 'wmode': wmode, 'x0': item.bbox[0], 'y0': item.bbox[1], 
                      'x1': item.bbox[2], 'y1': item.bbox[3]}
                self.page['textbox'].append(tb)
                for child in item:
                    render(child)
            elif isinstance(item, LTChar):
                # bbox (x0,y0,x1,y1)
                # x0: the distance from the left of the page to the left edge of the box.
                # y0: the distance from the bottom of the page to the lower edge of the box.
                # x1: the distance from the left of the page to the right edge of the box.
                # y1: the distance from the bottom of the page to the upper edge of the box.
                txt = {'text': item.get_text(), 'font': enc(item.fontname), 'size': item.size,
                       'colorspace': item.ncs.name, 'color': json.dumps(item.graphicstate.ncolor),
                       'x0': item.bbox[0], 'y0': item.bbox[1], 'x1': item.bbox[2], 'y1': item.bbox[3]}
                self.page['text'].append(txt)
            elif isinstance(item, LTText):
                # LTText is the interface for things that have text.
                # LTAnno inherits from LTText.
                self.page['text'].append({'text': item.get_text()})
            elif isinstance(item, LTImage):
                if self.imagewriter is not None:
                    name = self.imagewriter.export_image(item)
                    img = {'src': enc(name), 'width': item.width, 'height': item.height}
                    self.page['image'].append(img)
                else:
                    self.page['image'].append({'width': item.width, 'height': item.height})
            else:
                assert False, str(('Unhandled', item))
            return
        render(ltpage)
        return


COL_NAMES = {
    'metainfo': ['pid', 'rotate', 'x0', 'y0', 'x1', 'y1'],
    'text': ['pid', 'block', 'text', 'font', 'size', 'colorspace', 'color', 'x0', 'y0', 'x1', 'y1'],
    'line': ['pid', 'linewidth', 'x0', 'y0', 'x1', 'y1'],
    'rect': ['pid', 'linewidth', 'x0', 'y0', 'x1', 'y1'],
    'curve': ['pid', 'linewidth', 'pts', 'x0', 'y0', 'x1', 'y1'],
    'figure': ['pid', 'name', 'x0', 'y0', 'x1', 'y1'],
    'textline': ['pid', 'x0', 'y0', 'x1', 'y1'],
    'textbox': ['pid', 'id', 'wmode', 'x0', 'y0', 'x1', 'y1'],
    'textgroup': ['pid', 'x0', 'y0', 'x1', 'y1'],
    'image': ['pid', 'src', 'width', 'height']}


class PdfDoc:    
    def __init__(self, doc):        
        self.elements = ['metainfo', 'text', 'line', 'rect', 'curve', 'figure', 'textline', 
                         'textbox', 'textgroup', 'image']
        self.doc = {}
        for ele in self.elements:
            self.doc[ele] = list()
            for page in doc:
                if ele == 'metainfo':
                    self.doc[ele].append(page[ele])
                else:
                    pid = page['metainfo']['pid']
                    for item in page[ele]:
                        item['pid'] = pid
                        self.doc[ele].append(item)
        
    def __repr__(self):
        if len(self.doc) == 1:
            s = "A pdf document with 1 page."
        else:
            s = "A pdf document with %i pages." % (len(self.doc), )
        return s
    
    def __str__(self):
        return self.__repr__()
    
    def list_elements(self):
        return self.elements
    
    def check_dtype(self, dtype):
        if not dtype in ("list", "df"):
            raise ValueError("Unknown dtype, allowed values are 'list' and 'df'!")
            
    def __get_element(self, element, dtype="df"):
        self.check_dtype(dtype)
        if  dtype == "list":
            return self.doc[element]
        else:
            df = pd.DataFrame(self.doc[element], columns=COL_NAMES[element])
            return df
    
    def get_text(self, dtype="df"):
        self.check_dtype(dtype)
        if dtype == "list":
            return self.doc['text']
        else:
            d = list()
            pid = -1
            block = 0
            for item in self.doc['text']:
                if "x0" in item.keys():
                    if pid != item['pid']:
                        block += 1
                    item['block'] = block
                    d.append(item)
                    pid = item['pid']
                else:
                    block += 1
            df = pd.DataFrame(self.doc['text'], columns=COL_NAMES['text'])
            return df
        
    def get_element(self, element, dtype="df"):
        return self.get_text(dtype) if element == "text" else self.__get_element(element, dtype)
                    
    def get_metainfo(self, dtype="df"):
        return self.__get_element('metainfo', dtype)
    
    def get_line(self, dtype="df"):
        return self.__get_element('line', dtype)
    
    def get_rect(self, dtype="df"):
        return self.__get_element('rect', dtype)
    
    def get_curve(self, dtype="df"):
        return self.__get_element('curve', dtype)
    
    def get_figure(self, dtype="df"):
        return self.__get_element('figure', dtype)
    
    def get_textline(self, dtype="df"):
        return self.__get_element('textline', dtype)
    
    def get_textbox(self, dtype="df"):
        return self.__get_element('textbox', dtype)
    
    def get_textgroup(self, dtype="df"):
        return self.__get_element('textgroup', dtype)
    
    def get_image(self, dtype="df"):
        return self.__get_element('image', dtype)
    

def read_all(pdffile, page_numbers=[], codec='utf-8', strip_control=False,
             password="", caching=True, maxpages=0, rotation=0, image_dir=None):
    
    if not (os.path.splitext(pdffile)[1] == ".pdf"):
        raise IOError("PDF-file expected got '%s'!" % (os.path.splitext(pdffile)[1], ))
    
    if not os.path.exists(pdffile):
        raise IOError("Could not find PDF-file '%s'!" % (pdffile, ))
        
    if image_dir is None:
        imagewriter = None
    else:
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        imagewriter = ImageWriter(image_dir)

    rsrcmgr = PDFResourceManager(caching=caching)
    laparams = LAParams()
    
    device = XML2Converter(rsrcmgr, codec=codec, laparams=laparams, imagewriter=imagewriter,
                           stripcontrol=strip_control)
    
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    with open(pdffile, 'rb') as con:
        if (page_numbers is None) or (len(page_numbers) == 0):
            page_numbers = [i[0] for i in enumerate(PDFPage.get_pages(con))]
    
        for page in PDFPage.get_pages(con, page_numbers, maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate + rotation) % 360
            interpreter.process_page(page)
    
    return PdfDoc(device.doc)
    

def group_blocks(x):
    def group_block(d):
        if d.shape[0] == 0:
            return None
        
        r1 = d.iloc[0]
        di = {'pid': r1['pid'], 'text': ''.join(d['text']), 'font': r1['font'], 'size': r1['size'], 
              'colorspace': r1['colorspace'], 'color': r1['color'], 
              'x0': d['x0'].min(), 'y0': d['y0'].min(), 'x1': d['x1'].max(), 'y1': d['y1'].max()}
        return di

    x = x.dropna(subset=['block'])
    x = x.astype({'block': int})
    y = [group_block(df) for block_id, df in x.groupby('block', as_index=False)]
    return pd.DataFrame(y)

