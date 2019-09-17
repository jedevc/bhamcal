from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

TIMETABLE = "https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"

class Frame:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def CHROME(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

    @property
    def FIREFOX(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        return driver

    def extract(self, driver):
        driver.get(TIMETABLE)

        # log in
        driver.find_element_by_name("tUserName").send_keys(self.username)
        driver.find_element_by_name("tPassword").send_keys(self.password)
        driver.find_element_by_name("bLogin").click()

        # go to web timetables
        driver.find_element_by_id("LinkBtn_mystudentset").click()

        # select options from drop downs
        select = Select(driver.find_element_by_id("lbWeeks"))
        select.deselect_all()
        select.select_by_visible_text('*All Term Time')

        select = Select(driver.find_element_by_id("lbDays"))
        select.deselect_all()
        select.select_by_visible_text('All Week')

        select = Select(driver.find_element_by_id("dlPeriod"))
        select.select_by_visible_text('All Day (08:00 - 22:00)')

        select = Select(driver.find_element_by_id("dlType"))
        select.select_by_visible_text('List Timetable (with calendar dates)')

        # actually get the calendar
        driver.find_element_by_id("bGetTimetable").click()

        #gets page source
        source = driver.page_source
        driver.quit()

        return source