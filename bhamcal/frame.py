import enum

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

TIMETABLE = "https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"

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
