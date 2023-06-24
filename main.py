from utils.scrapper import Scraper
import time
import re
from selenium.webdriver.common.by import By
from datetime import datetime
from utils.text_formatting import text_formatting
from dotenv import load_dotenv
import os

import logging
load_dotenv(override=False)

PASSWORD = os.getenv('MICRO_PASS')

email = 'cb012185@students.apiit.lk'

course_pattern = r"^https:\/\/lms\.apiit\.lk\/course\/view"
assignment_pattern = r"^https:\/\/lms\.apiit\.lk\/mod\/assign\/view"
turnitin_pattern = r"^https:\/\/lms\.apiit\.lk\/mod\/turnitintooltwo\/view"

logging.info('Started')
scraper = Scraper('https://lms.apiit.lk/')
scraper.element_click_by_xpath('//a[@href="https://lms.apiit.lk/auth/oidc/"]')
# Add login functionality to the scraper

logging.info('Logging In')
scraper.driver.find_element(By.NAME, 'loginfmt').send_keys(email)
scraper.element_click_by_xpath("//input[@type='submit']")

scraper.driver.find_element(By.NAME, 'passwd').send_keys(PASSWORD)
scraper.element_click_by_xpath("//input[@type='submit']")

scraper.element_click_by_xpath("//input[@type='submit']")

scraper.go_to_page('https://lms.apiit.lk/')
logging.info('Logged In')
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
        'Due Date': due_date,
        'Time Remaining': time_remaining,
        'Title': title
    }

    if datetime.now() > datetime.strptime(due_date, '%A, %d %B %Y, %I:%M %p'):
        assignments_details.append(details)


turnitin_details = []
for turnit in turnitin:
    scraper.driver.get(turnit)
    table = scraper.find_element_by_class('mod_turnitintooltwo_part_details')
    rows = table.find_elements(By.TAG_NAME, "tr")
    turnitin_row = rows[1].find_elements(By.TAG_NAME, "td")
    details = {
        'Due Date': turnitin_row[2].text,
        'Time Remaining': str(datetime.now() - datetime.strptime(turnitin_row[2].text, "%d %b %Y - %H:%M")),
        'Title': turnitin_row[0].text
    }
    if datetime.now() > datetime.strptime(turnitin_row[2].text, "%d %b %Y - %H:%M"):
        turnitin_details.append(details)


text_message = text_formatting(turnitin_details, assignments_details)
print(text_message)
logging.info(text_message)
# pywhatkit.sendwhatmsg_to_group_instantly("DrUM5ch91Va93xUdj1sfgz", text_message)
# pywhatkit.sendwhatmsg_instantly("+", text_message)
