
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import pandas as pd
from datetime import date, datetime, timedelta
import time as t

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scrape():

    template="https://www.cbinsights.com/research-unicorn-companies"
    XPATH = "//*[@class='ui-mainview-block eventpath-wrapper']"
    TIMEOUT = 20

    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    browser = webdriver.Firefox(
        options=firefoxOptions,
        executable_path="/home/appuser/.conda/bin/geckodriver",
    )
    browser.get(template)
    t.sleep(2)
    num_rows=browser.execute_script("return document.getElementsByTagName('tr').length")


    company=[]
    val=[]
    dt=[]
    country=[]
    city=[]
    industry=[]
    investors=[]

    for i in range(1,num_rows):
        try:
          company.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[0].innerText"))
          val.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[1].innerText"))
          dt.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[2].innerText"))
          country.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[3].innerText"))
          city.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[4].innerText"))
          industry.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[5].innerText"))
          investors.append(browser.execute_script("return document.getElementsByTagName('tr')["+str(i)+"].children[6].innerText"))

        except:
            pass
        
    browser.quit()
    dict={"Company name": company, "Valuation (in $B)":val, "Date Joined":dt,"Country of origin":country,"City":city,"Industry":industry,"Investors":investors}
    table1=pd.DataFrame(dict)

    table1["Date Joined"]=pd.to_datetime(table1["Date Joined"],infer_datetime_format=True)
    table1["Date Joined"]=table1["Date Joined"].dt.strftime("%d-%m-%Y")
    table1["Valuation (in $B)"] = table1["Valuation (in $B)"].apply(lambda x : x.replace("$","")) 
    table1["Valuation (in $B)"] = table1["Valuation (in $B)"].astype("float")
    table1.to_csv("tb1.csv",index=False)

    print("Done")
