#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:21:46 2019

@author: enrico
"""

#from pdfminer.pdfparser import PDFParser, PDFDocument
#from pdfminer.pdfparser import PDFParser
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfpage import PDFPage
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#import textract
import PyPDF2
import os 
import zipfile
import re
import subprocess
import textract


def getFormat(instanceDocument): 
    
    if re.search('.pdf$',str(instanceDocument))!=None:
        return 'pdf'
    if re.search('.doc$|docx$',str(instanceDocument))!=None:
        return 'doc'
    else:
        return "---> ERROR <---\nDocument "+str(instanceDocument)+" is not supported!"


def parsePdf(instanceDocument):
    path=os.getcwd()+'/media/'+str(instanceDocument)
    text = textract.process(path)
    text=text.decode("utf-8", "strict")
    text=text.lower()
    return text



    
def parsePdf0(instanceDocument):
    
    extracted_text=''
    path=os.getcwd()+'/media/'+str(instanceDocument)
    pdfFileObj = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for i in range(pdfReader.numPages):
        pageObj=pdfReader.getPage(i)
        extracted_text+='\n'+pageObj.extractText()
    extracted_text=extracted_text.lower()
    pdfFileObj.close()
    return extracted_text
        

def parsePdf2(instanceDocument):
    filepath=os.getcwd()+'/media/'+str(instanceDocument)
    print('Getting text content for {}...'.format(filepath))
    process = subprocess.Popen(['pdf2txt.py', filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    if process.returncode != 0 or stderr:
        raise OSError('Executing the command for {} caused an error:\nCode: {}\nOutput: {}\nError: {}'.format(filepath, process.returncode, stdout, stderr))
    extracted_text=stdout.decode('utf-8').lower()
    return extracted_text
    
    
    
    
def parsePdf1(instanceDocument):
    print("parseeeeeeeeeeeeeeee PDF")
    print(os.getcwd()+'/media/'+str(instanceDocument))
   # path=os.getcwd()+'/media/'+str(instanceDocument)
    path='/home/enrico/Desktop/Backup Ubuntu Mate/djangoProjects/last_development/proj3/media/documents/Anna_Nasti.pdf'
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    extracted_text=extracted_text.lower()
    fp.close()
    """
    f=open('write','w')
    f.write(extracted_text)
    f.close()
    """
    return  extracted_text


def parseDoc(instanceDocument):
    path=os.getcwd()+'/media'+'/'+str(instanceDocument)
    doc=zipfile.ZipFile(path)
    content = doc.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|\n)*?>',' ',content)
    extracted_text=re.sub(r'\s{2,100}',' ',cleaned)
    extracted_text=extracted_text.lower()
    return extracted_text













































                
