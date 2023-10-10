import os
import requests
from bs4 import BeautifulSoup

from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, Query, Body, HTTPException

from models import crawler as crawler_model


router = APIRouter(prefix="/crawler", tags=["Crawler"])


@router.post("/" )
async def crawler(crawler : crawler_model.CreateCrawler): 

    try:
        url = crawler.name

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            course_name_tag = soup.find('h2', id='pagetitle') 
            course_code = url.split('=')[-1]
            if course_name_tag:
                course_name = course_name_tag.get_text(strip=True)
            else:
                course_name = f"Course Name Not Found [{course_code}]"

            # Find the "Course overview" section
            course_overview_tag = soup.find('h3', string='Course overview')
            if course_overview_tag:
                course_overview_dl = course_overview_tag.find_next('dl', class_='columns ruled')
                course_overview = {}
                for dt, dd in zip(course_overview_dl.find_all('dt'), course_overview_dl.find_all('dd')):
                    course_overview[dt.get_text(strip=True)] = dd.get_text(strip=True)
            else:
                course_overview = {"Course overview": "Not Found"}

            # Find the "Course details" section
            course_details_tag = soup.find('h3', string='Course details')
            if course_details_tag:
                course_details_dl = course_details_tag.find_next('dl', class_='columns ruled')
                course_details = {}
                for dt, dd in zip(course_details_dl.find_all('dt'), course_details_dl.find_all('dd')):
                    course_details[dt.get_text(strip=True)] = dd.get_text(strip=True)
            else:
                course_details = {"Course details": "Not Found"}

            # Extract tables within <div class="table-scroll">
            table_scroll_divs = soup.find_all('div', class_='table-scroll')
            course_structure = []
            for div in table_scroll_divs:
                table = div.find('table', class_='styled width-max')
                if table:
                    headers = [th.get_text(strip=True) for th in table.find_all('th')]
                    for row in table.find_all('tr')[1:]:
                        cols = row.find_all('td')
                        unit_info = {}
                        for header, col in zip(headers, cols):
                            unit_info[header] = col.get_text(strip=True)
                        course_structure.append(unit_info)
                else:
                    course_structure.append({"Course structure": "Table Not Found"})

            formatted_info = f"Course overview of {course_name}\n"
            for key, value in course_overview.items():
                formatted_info += f"{key.strip()}: {value.strip()}\n"

            for key, value in course_details.items():
                formatted_info += f"{key.strip()}: {value.strip()}\n"

            formatted_info += f"\nCourse Structure of {course_name}\n"
            for unit_info in course_structure:
                for key, value in unit_info.items():
                    formatted_info += f"{key.strip()}: {value.strip()}\n"
            return formatted_info

        else:
            print(f"Failed to fetch URL: {url}, Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred while processing URL: {url}, Error: {str(e)}")

    return None

