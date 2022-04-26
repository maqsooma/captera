from encodings import utf_8
from multiprocessing.connection import wait
from time import time
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
from selenium import webdriver
import soupsieve
import sqlalchemy
from sqlalchemy import create_engine,true
from sqlalchemy.orm import sessionmaker,scoped_session
from selenium.webdriver.firefox.options import Options
import time
import random as rd


def make_soup(content):
    soup = BeautifulSoup(content,"html.parser")
    return soup


engine = create_engine('mysql://root:@localhost/eclinic' )

con = engine.connect()

con.execute('SET GLOBAL max_allowed_packet=67108864')


# import pdb;pdb.set_trace()
links = []
data = con.execute("SELECT link from capterra_data")
for link in data:
    links.append((tuple(link))[0])
options = Options()
options.headless = False



if __name__ =="__main__":
    counter =  1
    for link in links:
        driver = webdriver.Firefox(options=options)
        driver.get(link)

        content = driver.page_source
        soup = make_soup(content)
        
        try:
            about = (soup. find("div", {"id": "LoadableProductSummary"})).encode()
        except:
            about = "None"
        try:
            price =  soup. find("div", {"id": "LoadableProductPricingSection"}).encode()
        except:
            price ="None"
        con.execute("INSERT INTO capterra_scraped(link,about,pricing) values(%s,%s,%s)",(link,about,price),encoding='utf-8')
        # except:
        #     con.execute("INSERT INTO capterra_scraped(link,about,pricing) values(%s,%s,%s)",(link,'none','none'),encoding='utf-8')
        print(counter)
        counter = counter + 1
        driver.close()
        time.sleep(rd.randint(0,4))
