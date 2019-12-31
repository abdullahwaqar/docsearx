"""
* This file contains spurce code for reading and extracting data from pdfs
* @author: Mubashar Hussain
"""
import fitz
from storage import enumrateFilenames

def readPdf():
    with fitz.open(enumrateFilenames()[1]) as infile:
        print(infile.pageCount)
        # print(infile.metadata)
        print(infile.getToC())
        # for page in infile:
        #     print(page.getText())

readPdf()