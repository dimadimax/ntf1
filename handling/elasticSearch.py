#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date,Integer, Keyword
from elasticsearch import Elasticsearch
import socket
#from . import models

connections.create_connection()

class mapping(DocType):
    author=Text()
    name = Text()
    job_title = Text()
    company = Text()
    location=Text()
    education=Text()
    ral=Integer()
    email=Text()
    url=Keyword()
    mobile=Text()
    status=Keyword()
    date = Date()
    note=Text()
    importedFrom=Keyword()
    raw_text=Text()
    experiences=Text()
    related_to=Text()
    
    class Meta:
        index = 'index5'


def delete(docId):
    
    es=Elasticsearch()
    return es.delete('index5','_doc',docId)

def portOpen(host='127.0.0.1',port=9200): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,port))
    if result==0:
        return True
    else:
        return False
    sock.close()
    
    
