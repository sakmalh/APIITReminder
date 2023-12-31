from utils.scrapper import Scraper
import time
import re
from selenium.webdriver.common.by import By
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.text_formatting import text_formatting
from dotenv import load_dotenv
import os
import json
from whatsapp_api_client_python import API
import logging
import requests


load_dotenv(override=False)
PASSWORD = os.getenv('MICRO_PASS')
IDINSTANCE = os.getenv('IDINSTANCE')
TOKENID = os.getenv('TOKENID')
PANTRYTOKEN = os.getenv('PANTRYTOKEN')

greenAPI = API.GreenApi(
    IDINSTANCE, TOKENID
)
pantry = f"https://api.npoint.io/a2376d48fe134d4592dc"
email = 'cb012185@students.apiit.lk'

course_pattern = r"^https:\/\/lms\.apiit\.lk\/course\/view"
assignment_pattern = r"^https:\/\/lms\.apiit\.lk\/mod\/assign\/view"
turnitin_pattern = r"^https:\/\/lms\.apiit\.lk\/mod\/turnitintooltwo\/view"

scraper = Scraper('https://lms.apiit.lk/login/index.php')
scraper.element_click_by_xpath('//a[@href="https://lms.apiit.lk/auth/oidc/"]')

scraper.element_send_keys('loginfmt', email)
scraper.element_click_by_xpath("//input[@type='submit']")

scraper.element_send_keys('passwd', PASSWORD)
scraper.element_click_by_xpath("//input[@type='submit']")

scraper.element_click_by_xpath("//input[@type='submit']")

scraper.go_to_page('https://lms.apiit.lk/')
links = scraper.get_all_links()
courses = set([link for link in links if re.match(course_pattern, link)])
turnitin = []
assignments = []

for course in courses:
    scraper.driver.get(course)
    links = scraper.get_all_links()
    course_turnitin = set([link for link in links if re.match(turnitin_pattern, link)])
    course_assignment = set([link for link in links if re.match(assignment_pattern, link)])
    turnitin.extend(list(course_turnitin))
    assignments.extend(list(course_assignment))

assignments_details = []
for assignment in assignments:
    scraper.driver.get(assignment)
    due_date = scraper.driver.find_element('xpath', '//th[text()="Due date"]/following-sibling::td').text
    time_remaining = scraper.driver.find_element('xpath', '//th[text()="Time remaining"]/following-sibling::td').text
    title = scraper.driver.find_element('xpath', '//section[@id="region-main"]//h2[1]').text
    details = {
        'Link': assignment,
        'Type': 'Normal',
        'Due Date': due_date,
        'Time Remaining': datetime.strptime(due_date, '%A, %d %B %Y, %I:%M %p').replace(tzinfo=ZoneInfo('Asia/Kolkata')) - datetime.now(tz=ZoneInfo('Asia/Kolkata')),
        'Title': title
    }

    if datetime.now(tz=ZoneInfo('Asia/Kolkata')) < datetime.strptime(due_date, '%A, %d %B %Y, %I:%M %p').replace(tzinfo=ZoneInfo('Asia/Kolkata')) :
        assignments_details.append(details)

turnitin_details = []
for turnit in turnitin:
    scraper.driver.get(turnit)
    table = scraper.find_element_by_class('mod_turnitintooltwo_part_details')
    rows = table.find_elements(By.TAG_NAME, "tr")
    turnitin_row = rows[1].find_elements(By.TAG_NAME, "td")
    details = {
        'Link': turnit,
        'Type': 'Turnitin',
        'Due Date': turnitin_row[2].text,
        'Time Remaining': datetime.strptime(turnitin_row[2].text, "%d %b %Y - %H:%M").replace(tzinfo=ZoneInfo('Asia/Kolkata')) - datetime.now(tz=ZoneInfo('Asia/Kolkata')),
        'Title': turnitin_row[0].text
    }
    if datetime.now(tz=ZoneInfo('Asia/Kolkata')) < datetime.strptime(turnitin_row[2].text, "%d %b %Y - %H:%M").replace(tzinfo=ZoneInfo('Asia/Kolkata')) :
        turnitin_details.append(details)

data = json.loads(requests.get(pantry).text)

ten_day = data['10Day']
three_day = data['3Day']
initialized = data['New']

total_assignments = turnitin_details + assignments_details

ten_day_new = []
three_day_new = []
initialized_new = []
one_day = []

for total_assignment in total_assignments:
    if total_assignment['Time Remaining'].days == 10:
        ten_day_new.append(total_assignment)

    if total_assignment['Time Remaining'].days == 3:
        three_day_new.append(total_assignment)

    if total_assignment['Time Remaining'].days == 0:
        one_day.append(total_assignment)

    if total_assignment['Link'] not in initialized:
        initialized_new.append(total_assignment)

ten_day.extend([x['Link'] for x in ten_day_new])
three_day.extend([x['Link'] for x in three_day_new])
initialized.extend([x['Link'] for x in initialized_new])

data['10Day'] = ten_day
data['3Day'] = three_day
data['New'] = initialized

if len(ten_day_new) != 0 or len(three_day_new) != 0 or len(initialized_new) != 0 or len(one_day) != 0:
    response = requests.post(pantry, json=data)
    text_message = text_formatting(ten_day_new, three_day_new, initialized_new, one_day)
    logging.info(text_message)
    greenAPI.sending.sendMessage("120363120724407545@g.us", text_message)
    greenAPI.sending.sendMessage("94751285876@c.us", text_message)
    greenAPI.sending.sendMessage("120363074446222578@g.us", text_message)

greenAPI.sending.sendMessage("94751285876@c.us", 'Run Successful')

