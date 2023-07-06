import pandas as pd                     
from pandas import DataFrame           
import numpy as np                      

from itertools import chain

from collections import Counter         
from datetime import datetime           
import re                              
from time import sleep                  
import random                           
import math                            
import time                             
import itertools                       
import sys
import openpyxl
import psycopg2

from flask import Flask, render_template
from flask_restful import Resource, Api
import psycopg2

import requests                        
from bs4 import BeautifulSoup           
from selenium import webdriver         
import json                            


def get_soup_elements(typ_obchodu = "prodej", typ_stavby = "byty", pages = 1):  
    
    browser = webdriver.Chrome()
    
    
    url_x = r"https://www.sreality.cz/hledani"             
    url = url_x + "/" +  typ_obchodu + "/" +  typ_stavby

    browser.get(url)    # (url).text ??
    sleep(random.uniform(1.0, 1.5))
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML,'lxml') # "parser" ??
    
    elements = []    
    
    for link in soup.findAll('a', attrs={'href': re.compile("^/detail/")}):      
        link = link.get('href')   
        elements.append(link)     
    elements = elements[0::2]   

    records = soup.find_all(class_ ='numero ng-binding')[1].text
    records = re.split(r'\D', str(records))                         
    records = ",".join(records).replace(",", "")
    records = int(records)
    max_page = math.ceil(records / 20)   
    print("----------------")
    print("Scrapuji: " + str(typ_obchodu) + " " + str(typ_stavby))
    print("Celkem inzerátů: " + str(records))
    print("Celkem stránek: " + str(max_page))
    
    if pages == 999:
        print("Scrapuji (pouze) " + str(pages) + " stran.")
        print("----------------")
  
    
    for i in range(pages-1):   
        i = i+2
        
        sys.stdout.write('\r'+ "Strana " + str(i-1) + " = " + str(round(100*(i-1)/(pages), 2)) + "% progress. Zbývá cca: " + str(round(random.uniform(3.4, 3.8)*(pages-(i-1)), 2 )) + " sekund.")    # Asi upravím čas, na rychlejším kabelu v obýváku je to občas i tak 3 sec :O

        url2 = url + "?strana=" + str(i)
        browser.get(url2)

        sleep(random.uniform(1.0, 1.5))

        innerHTML = browser.execute_script("return document.body.innerHTML")
        soup2 = BeautifulSoup(innerHTML,'lxml') 
        
        elements2 = []
        
        for link in soup2.findAll('a', attrs={'href': re.compile("^/detail/prodej/")}):  
            link = link.get('href') 
            elements2.append(link)  
   
        elements2 = elements2[0::2]  
        
        elements = elements + elements2     

    
    browser.quit()   
    
    return elements


def elements_and_ids(x):
    
    elements = pd.DataFrame({"url":x})

    def get_id(x):
        x = x.split("/")[-1]
        return x
    
    len1 = len(elements)
    elements = elements.drop_duplicates(subset = [ "url"], keep = "first", inplace = False)   
    len2 = len(elements)                                                                             
                                                                                                      
    print("-- Vymazáno " + str(len1-len2) + " záznamů kvůli duplikaci.")
    return elements

def scrap_all(typ_obchodu = "prodej", typ_stavby = "byty", pages = 1):
    
    data = get_soup_elements(typ_obchodu = typ_obchodu, typ_stavby = typ_stavby, pages = pages)
    print( "1/8 Data scrapnuta, získávám URLs.")
    
    data = elements_and_ids(data)
    data.to_excel(r"a1_URLs_prodej_byty.xlsx")
    print( "2/8 Získány URL, nyní získávám Souřadnice, Ceny a Popis - několik minut...")
    

    return data

data = scrap_all(pages=25)

data[['null','detail', 'prodej','byt','velikost','lokace','id']] = data.url.str.split("/", expand = True)
data = data.drop(['url','null', 'detail','prodej','byt','id'], axis=1)
data.to_csv('sreality.csv')

data.to_csv('sreality.csv')

conn = psycopg2.connect(host='localhost',
port = '5432',
user = 'postgres',
password = '159357lol',
dbname = 'postgres')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS sreality')

create_script= "CREATE TABLE IF NOT EXISTS sreality (ID INT,Velikost VARCHAR(255), Lokace VARCHAR(255))"
cur.execute(create_script)

with open('sreality.csv', 'r') as f:
    next(f) 
    cur.copy_from(f, 'sreality', sep=',')

conn.commit()
conn.close()
cur.close()
