"""
this file contains chunker which can split the documents into smaller documents 

    written by- Sai Mukhund 
"""
import os 
import json 
import argparse

from langchain.docstore.document import Document 
from langchain.text_splitter import (
    CharacterTextSplitter,
    Language,
    RecursiveCharacterTextSplitter,
)
from transformers import Autotokenizer 

from read_data import read_documents 

def separators(chunker_type,separators_type,separators):
    if chunker_type=="character":
        if separators is None:
            separators=" "
        else :
            separators=separators           #TODO check if list 
    elif chunker_type=="recursive":
        if separators is not None:
            separators=separators
        elif separators_type is None:
            separators=["\n\n","\n"," ",""]
        elif separators_type.lower()=="markdown":
            separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language.MARKDOWN)
        elif separators_type.lower()=="html":
            separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language.HTML)
        elif separators_type.lower()=="python":
            separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language.PYTHON)
        elif separators_type.lower()=="cpp":
            separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language.CPP)
        elif separators_type.lower()=="java":
            separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language.JAVA)
        else:
            raise Excpetion(f"cant support such functionality")
        return separators

def chunker(
    documents,
    chunking_type="recursive",
    chunk_size=500,
    chunk_overlap=20,
    separators_type=None,
    separators=None,
    tokenizer_name_or_path=None):

    final_documents=read_documents(documents)
    final_separators=get_separators(chunker_type,separators_type,separators)

    if chunker_type=="character":
        splitter=CharacterTextSplitter(
            separators=final_separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    elif chunker_type=="recursive":
        if tokenizer_name_or_path is None:
            splitter=RecursiveCharacterTextSplitter(
                separators=separators,
                chunk_size=chunk_size,
                chunk_overalap=chunk_overlap
            )
        else:
            tokenizer=Autotokenizer.from_pretrained(tokenizer_name_or_path)
            splitter=RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
                tokenizer,
                separators=separators,
                chunk_size=chunk_size,
                chunk_overalap=chunk_overlap
            )
    splitted_documents=splitter.split_documents(final_documents)
    return splitted_documents
