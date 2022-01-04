from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from browserstack.local import Local
import os


username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
browserstack_local = os.getenv("BROWSERSTACK_LOCAL")
browserstack_local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")

BROWSERSTACK_URL = 'https://genegrady_zGMDwK:XY6JqwRAggsPCGXnAkxs@hub-cloud.browserstack.com/wd/hub'

caps = [{
      'os_version': '10',
      'os': 'Windows',
      'browser': 'Firefox',
      'browser_version': 'latest',
      'name': 'Parallel Test1', # test name
      'build': build_name, # CI/CD job name using BROWSERSTACK_BUILD_NAME env variable
      'browserstack.local': browserstack_local,
      'browserstack.localIdentifier': browserstack_local_identifier,
      'browserstack.user': username,
      'browserstack.key': access_key, # Your tests will be organized within this build
      'browserstack.networkLogs': 'true',
      "browserstack.debug" : "true",
      "browserstack.geoLocation" : "FR",
      "browserstack.console" : "info",
      "browserstack.maskCommands" : "setValues"
      },
      {
      'os_version': '10',
      'os': 'Windows',
      'browser': 'Edge',
      'browser_version': 'latest',
      'name': 'Parallel Test2', # test name
      'build': build_name, # CI/CD job name using BROWSERSTACK_BUILD_NAME env variable
      'browserstack.local': browserstack_local,
      'browserstack.localIdentifier': browserstack_local_identifier,
      'browserstack.user': username,
      'browserstack.key': access_key, # Your tests will be organized within this build
      'browserstack.networkLogs': 'true',
      "browserstack.debug": "true",
      "browserstack.geoLocation" : "FR",
      "browserstack.console" : "info",
      "browserstack.maskCommands" : "setValues"
      },
      {
      'os_version': 'Monterey',
      'os': 'OS X',
      'browser': 'Chrome',
      'browser_version': 'latest',
      'name': 'Parallel Test3', # test name
      'build': build_name, # CI/CD job name using BROWSERSTACK_BUILD_NAME env variable
      'browserstack.local': browserstack_local,
      'browserstack.localIdentifier': browserstack_local_identifier,
      'browserstack.user': username,
      'browserstack.key': access_key, # Your tests will be organized within this build
      'browserstack.networkLogs': 'true',
      "browserstack.debug": 'true',
      "browserstack.geoLocation" : "FR",
      "browserstack.console" : "info",
      "browserstack.maskCommands" : "setValues"  
      }, 
      {
      'device': 'iPhone 12 Pro',
      'os_browser': '14',
      'real_mobile': 'true',
      'name': 'Parallel Tests4',
      'build': build_name, # CI/CD job name using BROWSERSTACK_BUILD_NAME env variable
      'browserstack.local': browserstack_local,
      'browserstack.localIdentifier': browserstack_local_identifier,
      'browserstack.user': username,
      'browserstack.key': access_key, # Your tests will be organized within this build
      'browserstack.networkLogs' : 'true',
      "browserstack.debug" : "true",
      "browserstack.geoLocation" : "FR",
      "browserstack.console" : "info",
      "browserstack.maskCommands" : "setValues",
      "browserstack.networkProfile" : "4g-lte-advanced-good"
    }]

    # driver initialization
def run_session(desired_cap):
    driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
    # launch URL
    driver.get("https://www.amazon.com")
    #locate search location by class name
    search = driver.find_element(By.ID, "twotabsearchtextbox")
    # send_keys() to simulate key strokes
    search.send_keys('Iphone X')
    # locate submit button by id
    submit = driver.find_element(By.ID, "nav-search-submit-button")
    submit.click()

    ios_filter = driver.find_element(By.ID, "p_n_feature_twenty_browse-bin\/17881878011" )
    ios_filter.click()

    sort_by= driver.find_element(By.CLASS_NAME, "a-button-text")
    sort_by.click()

    price_sort= driver.find_element(By.ID, "s-result-sort-select_2")
    price_sort.click()

    #Create arrays for each element we want to list
    a = []
    b = []
    c = []

    all_urls = driver.find_elements(By.CLASS_NAME, "a-link-normal")
    for elem in all_urls:
        a.append("Url:"  + " " + elem.get_attribute("href"))
    all_names = driver.find_elements(By.CSS_SELECTOR, "span.a-size-medium.a-color-base.a-text-normal") 
    for elem in all_names:
        b.append("Name:" + " " + elem.get_attribute("innerHTML"))
    all_prices =driver.find_elements(By.CLASS_NAME, 'a-offscreen')
    for elem in all_prices:
        c.append("Price:" + " " + elem.get_attribute("innerHTML"))
    #Combine arrays and arrange them in order
    x = [list(e) for e in zip(a,b,c)]
    print(x)
    print(driver.title)
    if (driver.title=="Amazon"):
	        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Title matched!"}}')
    else:
	        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Title not matched"}}')
    
    driver.quit()   
   

with ThreadPoolExecutor(max_workers=2) as executor:
	executor.map(run_session, caps)

