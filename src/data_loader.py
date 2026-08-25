from pathlib import Path
from typing import List,Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader,CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load all documents from the specified directory and convert to LangChain Document objects.
    Supported: PDF,TXT,CSV,Excel,Work,JSON
    """

    #Use project root data folder
    data_path= Path(data_dir).resolve()
    print(f"[DEGUB] Data path: {data_path}")
    documents =[]

    #pdf files
    pdf_files= list(data_path.glob("**/*.pdf"))
    print(f"[DEGUB] PDF files: {len(pdf_files)} PDF files: { [ str(f) for f in pdf_files ]}")
    for pdf_file in pdf_files:
        print(f"[DEGUB] Loading PDF: {pdf_file}")
        try:
            loader= PyPDFLoader(str(pdf_file))
            loader= loader.load()
            print(f"[DEGUB] Loaded {len(loader)} PDF docs from {pdf_file}")
            documents.extend(loader)
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}")



    #Docx files
    docx_files= list(data_path.glob("**/*.docx"))
    print(f"[DEGUB] DOCX files: {len(docx_files)} DOCX files:  { [str(d) for d in docx_files] } ")
    for docx_file in docx_files:
        print(f"[DEGUB] Loading Doc: {docx_file}")
        try:
            loader=Docx2txtLoader(docx_file)
            loader= loader.load()
            print(f"[DEGUB] Loaded {len(loader)} DOCX from {docx_file}")
            documents.extend(loader)
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {docx_file}")

    return documents

    
    #CSV files

    #SQL fiels