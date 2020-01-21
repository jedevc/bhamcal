import enum

from pprint import pprint

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

TIMETABLE = "https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"

class NativeFrame:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }

    def fetch(self, username, password):
        # get initial state
        session = requests.session()
        resp = session.get(TIMETABLE, headers=NativeFrame.HEADERS)

        # login
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form')
        filled = self._extract_form(form)
        filled['tUserName'] = username
        filled['tPassword'] = password

        resp = session.post(urljoin(resp.url, form['action']), data=filled, headers=NativeFrame.HEADERS)
        if 'Incorrect username or password' in resp.text:
            raise FrameFetchError()

        # navigate to web timetables form
        soup = BeautifulSoup(resp.text, 'html.parser')
        formdata = {
           '__VIEWSTATE': soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
           '__EVENTVALIDATION': soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'],
           '__EVENTTARGET': 'LinkBtn_modulesstudentset'
        }
        resp = session.post(TIMETABLE, data=formdata, headers=NativeFrame.HEADERS)
        with open('modules.html', 'w') as dump:
            dump.write(resp.text)






        # # Submit view timetable form
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form')
        select_modules = soup.find('select', attrs={'name': 'dlObject'})
        options = []
        for option in select_modules.findChildren():
            options.append(option['value'])
        print(options)
        # formdata = {
        #    '__EVENTTARGET': '',
        #    '__EVENTARGUMENT': '',
        #    '__LASTFOCUS': '',
        #    '__VIEWSTATE': soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
        #    '__VIEWSTATEGENERATOR': soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'],
        #    '__EVENTVALIDATION': soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'],
        #    "tLinkType": "modulesstudentset",
        #    "dlObject": "29289",
        #    "lbWeeks": "t",
        #    "lbDays": "1-5",
        #    "dlPeriod": "3-22",
        # #    "dlType": "individual;swsurl;1SWSCUST Object Individual",
        #    "dlType": "individual;swsurl;SWSCUST Object Individual MDS",
        #    "bGetTimetable": "View Timetable"
        # }

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://onlinetimetables.bham.ac.uk", "DNT": "1", "Connection": "close", "Referer": "https://onlinetimetables.bham.ac.uk/timetable/current_academic_year_2/default.aspx", "Upgrade-Insecure-Requests": "1"}
        formdata = {
                        "__EVENTTARGET": '',
                        "__EVENTARGUMENT": '',
                        "__LASTFOCUS": '',
                        "__VIEWSTATE": soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
                        "__VIEWSTATEGENERATOR": soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'],
                        # "__EVENTVALIDATION": "/wEWXwL2ire1CwLGjZyxBAKh2NLqCAKA+NWlAwKB1N7ACAL4jJt9Ao+T5AYC38Ga7A0CkoaswgYC1q6+0gYC6pbeegL0lt56ApKGjJYEAsGPxY4EAs+PxY4EAt2PxY4EAumX7goC94bKtgMCgI+9jQQC6ICgmgcCk5fk1wMC7P2LxAMCjY+JjQQCjY+NjQQCjY+xjQQCjY+1jQQCjY+5jQQCjY+9jQQCjY+hjQQCjY/ljgQCjY/pjgQCl87m2gMCuPfIrw0C3eCqhAcC5omNmQECi7Pv7wwCrNzxxAYCscXTWQLa7rWuCgLPhPXwAgLQrdfFDAKXzuraAwK498yvDQLd4K6EBwLmibGZAQKLs5PuDAKs3PXEBgKxxddZAtruua4KAs+E+fACAtCt28UMApfO7toDArj38K8NAt3g0oQHAuaJtZkBAouzl+4MAqzc+cQGArHF21kC2u69rgoCz4T98AIC0K3fxQwCl86S2QMCuPf0rw0C3eDWhAcC5om5mQECi7Ob7gwCrNz9xAYCscXfWQLa7qGuCgLPhOHwAgLQrcPFDAKXzpbZAwK49/ivDQLd4NqEBwLX2ZOaDgKB69f3AgKG69f3AgLoitfXDALpitfXDALqitfXDALritfXDALsitfXDALtitfXDALuitfXDALV0Lm1AQKI0JTOAwKRx46pCwKy0JTOAwLQu87MDAKK0My/CwLwoL2vAwKb9sRaAtvhxdUNAujWjewBAv3x+rAHyaxjgLxGzH0I3U23aQnIly6xGWA=",
                        "__EVENTVALIDATION": soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'],
                        "tLinkType": "modulesstudentset",
                        "dlObject": options,
                        "lbWeeks": "t",
                        "lbDays": "1-5",
                        "dlPeriod": "3-22",
                        # "dlType": "individual;swsurl;1SWSCUST Object Individual MDS",
                        "dlType": "TextSpreadsheet;swsurl;SWSCUST Object TextSpreadsheet MDS",
                        "bGetTimetable": "View Timetable"
                    }
        resp = session.post(TIMETABLE, headers=headers, data=formdata)
        # print(resp.history[0].request.path_url)


        # resp = session.post(TIMETABLE, data=formdata)

        with open('timetable.html', 'w') as dump:
            dump.write(resp.text)
        soup = BeautifulSoup(resp.text, 'html.parser')
        print('-------')
        for name in soup.find_all('span', attrs={'class': 'header-0-0-0'}):
            print(name.text)
        print('-------')
        return resp.text

    def _extract_form(self, form):
        extract = {}
        for tag in form.find_all('input'):
            name = tag.get('name')
            value = tag.get('value')
            if name:
                extract[name] = value
        return extract

class WebFrame:
    def __init__(self, driver):
        self.driver = driver

    def fetch(self, username, password):
        try:
            return self._download(username, password)
        except NoSuchElementException:
            raise FrameFetchError

    def _download(self, username, password):
        self.driver.get(TIMETABLE)

        # log in
        self.driver.find_element_by_name("tUserName").send_keys(username)
        self.driver.find_element_by_name("tPassword").send_keys(password)
        self.driver.find_element_by_name("bLogin").click()

        # go to web timetables
        self.driver.find_element_by_id("LinkBtn_mystudentset").click()

        # select options from drop downs
        select = Select(self.driver.find_element_by_id("lbWeeks"))
        select.deselect_all()
        select.select_by_visible_text('*All Term Time')

        select = Select(self.driver.find_element_by_id("lbDays"))
        select.deselect_all()
        select.select_by_visible_text('All Week')

        select = Select(self.driver.find_element_by_id("dlPeriod"))
        select.select_by_visible_text('All Day (08:00 - 22:00)')

        select = Select(self.driver.find_element_by_id("dlType"))
        select.select_by_visible_text('List Timetable (with calendar dates)')

        # actually get the calendar
        self.driver.find_element_by_id("bGetTimetable").click()

        # gets page source
        source = self.driver.page_source
        self.driver.quit()

        return source

class FrameFetchError(RuntimeError):
    pass

def CHROME(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def FIREFOX(headless=True):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver

if __name__ == "__main__":
    frame = NativeFrame()
    frame.fetch("cxd738","LEFTIES#dacquoise#RACIALIZED")