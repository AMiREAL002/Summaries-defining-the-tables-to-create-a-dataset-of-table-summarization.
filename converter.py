import os
import multiprocessing
from downloader import getPath
import fitz
fitz.TOOLS.mupdf_display_errors(False)      # Ignores random messages from the PyMuPDF Module

pdf_dir = "./Project/NAACL Conference Papers/pdf/"     # Path to the downloaded pdf files
txt_dir = "./Project/NAACL Conference Papers/to_txt/"  # Path to store the converted pdf files into txt format
xml_dir = "./Project/NAACL Conference Papers/to_xml/"  # Path to store the converted pdf files into xml format

def converter(root_pdf) -> None:                                           # Converts pdf into txt and xml files respictively
    suffix = root_pdf[root_pdf.index("doc") + 3:root_pdf.index(".pdf")]
    filepath = os.path.join(pdf_dir, f"doc{suffix}.pdf")                   # Generates Filepath of the pdf files located in pdf_dir 
    
    if os.path.isfile(filepath):
        
        with fitz.Document(filepath) as pdf_file:
            
            with open(os.path.join(txt_dir, f"doc{suffix}.txt"), "w", encoding="utf-8") as txt_file:     # Saves extracted data from pdf as a txt file
                text = ""
                for page in pdf_file:
                    text += page.get_text("text")  # Extracts text from binary format
                txt_file.write(text)
        
            with open(os.path.join(xml_dir, f"doc{suffix}.xml"), "w", encoding="utf-8") as xml_file:     # Saves extracted data from pdf as a xml file
                xml = ""
                for page in pdf_file:
                    xml += page.get_text("text")    # Extracts text from binary format
                xml_file.write(xml)

def processor():                                          # Lists all the files in the pdf folder
    files_to_convert: list[str] = os.listdir(pdf_dir)
    with multiprocessing.Pool(processes=50) as pool:      # Accelerates process with multiprocessing 
                pool.map(converter, files_to_convert)

    
def getTask():
    getPath([txt_dir, xml_dir])                           # Sends the directory path of the txt and xml folders
    print("Converting the downloaded Reseach Papers.... please be patient....\n") 
    processor()
    print(f"Research Papers have been converted successfully.... \nYou may now proceed for final output.txt generation")


if __name__ == "__main__" :
        getTask()
