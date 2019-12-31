"""
* This file contains source code for reading and extracting data from pdfs
* @author: Mubashar Hussain
"""
import fitz
from storage import enumrateFilenames

def readAllPdf():
    """
    * @def: Read all the pdf files from the stotage and return the text from all in a list and the file name
    * @return: List of tuple, pdf name and text data from all the pdfs
    """
    pages = []
    for pdf in enumrateFilenames():
        with fitz.open(pdf) as infile:
            for page in infile:
                pages.append((pdf, page.getText()))
    return pages

def readPdf(pdfname):
    """
    * @def: Read a pdf file from the stotage and return the text from all in a list and the file name
    * @param -> pdfname: path to the pdf
    * @return: List of tuple, pdf name and text data from the pdf
    """
    pages = []
    with fitz.open(pdfname) as infile:
        for page in infile:
            pages.append((pdfname, page.getText()))
    return pages
