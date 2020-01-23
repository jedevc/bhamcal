import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TIMETABLE = "https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"

class NativeFrame:
    def fetch(self, username, password):
        # get initial state
        session = requests.session()
        resp = session.get(TIMETABLE)

        # login
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form')
        filled = self._extract_form(form)
        filled['tUserName'] = username
        filled['tPassword'] = password

        resp = session.post(urljoin(resp.url, form['action']), data=filled)
        if 'Incorrect username or password' in resp.text:
            raise FrameFetchError()

        # navigate to web timetables form
        soup = BeautifulSoup(resp.text, 'html.parser')
        formdata = {
           '__VIEWSTATE': soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
           '__EVENTVALIDATION': soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'],
           '__EVENTTARGET': 'LinkBtn_mystudentset'
           # '__EVENTTARGET': 'LinkBtn_modulesstudentset'  # download all modules
        }
        resp = session.post(TIMETABLE, data=formdata)

        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form')

        # find all available module codes (only for downloading all modules)
        # select_modules = soup.find('select', attrs={'name': 'dlObject'})
        # modules = [x['value'] for x in select_modules.findChildren()]

        formdata = {
            # used to call a postback
            "__EVENTTARGET": '',
            "__EVENTARGUMENT": '',

            # used by ASP.NET to store state
            "__LASTFOCUS": '',
            "__VIEWSTATE": soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
            "__VIEWSTATEGENERATOR": soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'],
            "__EVENTVALIDATION": soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'],

            # not sure... just seemed to be there
            # "tLinkType": "modulesstudentset",

            # select modules (only for downloading all modules)
            # "dlObject": modules,
            # select weeks
            "lbWeeks": soup.find('option', string='*All Term Time')['value'],
            # select days of the week
            "lbDays": soup.find('option', string='All Week')['value'],
            # select hours of the day to view
            "dlPeriod": soup.find('option', string='All Day (08:00 - 22:00)')['value'],
            # formate to output the timetable in
            "dlType": soup.find('option', string='List Timetable (with calendar dates)')['value'],
            # select button to submit form
            "bGetTimetable": "View Timetable"
        }
        resp = session.post(TIMETABLE, data=formdata)

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
        from selenium.common.exceptions import NoSuchElementException

        try:
            return self._download(username, password)
        except NoSuchElementException:
            raise FrameFetchError

    def _download(self, username, password):
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver.chrome.options import Options

        # load the start page
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
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def FIREFOX(headless=True):
    from selenium import webdriver

    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver
