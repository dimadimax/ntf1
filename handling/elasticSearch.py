#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date,Integer, Keyword
from elasticsearch import Elasticsearch
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
        index = 'index4'


def delete(docId):
    
    es=Elasticsearch()
    return es.delete('index4','_doc',docId)
