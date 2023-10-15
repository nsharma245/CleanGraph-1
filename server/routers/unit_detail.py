from bs4 import BeautifulSoup,NavigableString
import requests
import validators

from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, Query, Body, HTTPException

from models import unit_detail as unit_detail_model



def crawl_until_end(element):
    elements = []

    if isinstance(element, NavigableString):
        # If the element is a NavigableString (text), return it
        return [str(element)]
    else:
        # If the element is a Tag, check its children
        for child in element.contents:
            child_elements = crawl_until_end(child)
            if child_elements:
                elements.extend(child_elements)

    return elements


def is_valid_url(text):
    return validators.url(text)

router = APIRouter(prefix="/crawler", tags=["Crawler"])


@router.post("/" )         
async def extract_unit_detail(crawler : unit_detail_model.CreateUnitDetail):
    if is_valid_url(url):
        #print(f"{url} is a valid URL")
        try:
            
            # we can modify this hardcode url with the input url
            source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            source.raise_for_status()
            
            soup = BeautifulSoup(source.content, 'html5lib')
            
            title = soup.find('h2', attrs = {'id':'pagetitle'}) 
            
            list = soup.find('dl', attrs = {'class':'ruled'}) 
            
            info = ''
            info = title.text
            info += '\n'
            
            dt_element = list.find_all('dt')  # Get all <dt> elements within the <dl>
        
            dd_element = list.find_all('dd')  # Get all <dd> elements within the <dl>
        
            
            for dt_e, dd_e in zip(dt_element, dd_element):
                    
                info += dt_e.get_text()
                info += ":"
                
                #reccursive function to get the end element
                all_element = crawl_until_end(dd_e)
                for el in all_element:
                    stripped_item = el.strip()
                    if stripped_item:
                        info += el 
            
                info += "\n"
                
            print("Text crawled for unit details")
            
            #file where the text will be crawled
            unit_code = url.split('=')[-1]
            name = f"{unit_code}.txt"
            filename = "./crawler/" + name
            #write title in file
            with open(filename, 'w',encoding='utf-8') as f:
                f.write(info)
                    
            return info

        except Exception as e:
            print(e)
        
    else:
        print(f"{url} is not a valid URL")
        return None

    return None



    
