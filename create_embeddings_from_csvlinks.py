import argparse
import pickle
import requests
import xmltodict
from dotenv import load_dotenv

load_dotenv()

from bs4 import BeautifulSoup
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
#from langchain.document_loaders.pdf import PDFPlumberLoader
#from langchain.document_loaders import PyPDFLoader
import PyPDF2


def extract_text_from(url_in, source_type):

    if source_type == 'url':
        html = requests.get(url_in).text
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)
    elif source_type == 'pdf':        
            response = requests.get(url)
            temp_pdf = '/tmp/temp.pdf'           
            with open(temp_pdf, 'wb') as f:
                f.write(response.content)
            text = ""
            with open(temp_pdf, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for pdf_page in pdf_reader.pages:#page_num in range(len(pdf_reader.pages)):
                    #pdf_page = pdf_reader.pages[page_num]
                    text += pdf_page.extract_text()
    
            return text.strip()
    #        with open(temp_pdf, 'wb') as f:
     #           f.write(response.content)
     #       loader = PyPDFLoader(temp_pdf)
     #       #pages = loader.load_and_split()
     #       documents = loader.load_and_split()


import csv

url_set = set()
no_of_duplicates = 0
pages = []
with open('links_nodups.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #print(f"no of urls found {len(list(reader))}")
    for row in reader:
        url = row[0].strip()     
        if 'pdf' in url:
            pages.append({'text': extract_text_from(url, source_type='pdf'), 'source': url})
        else:
            pages.append({'text': extract_text_from(url, source_type='url'), 'source': url})
    
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")

docs, metadatas = [], []
for page in pages:
    #if 'pdf' in page['source']:
    #    pdf_splits = text_splitter.split_documents(page['text'])
    #    docs.extend(pdf_splits)
    #    metadatas.extend([{"source": page['source']}] * len(pdf_splits))
    #    store = FAISS.from_documents(docs, OpenAIEmbeddings(), metadatas=metadatas)
    if 1:
        splits = text_splitter.split_text(page['text'])
        docs.extend(splits)
        metadatas.extend([{"source": page['source']}] * len(splits))
        print(f"Split {page['source']} into {len(splits)} chunks")

        store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
with open("faiss_store.pkl", "wb") as f:
    pickle.dump(store, f)
