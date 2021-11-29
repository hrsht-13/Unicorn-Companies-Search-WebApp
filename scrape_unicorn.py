
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import pandas as pd
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time as t

def scrape():
    path="geckodriver.exe"
    browser=webdriver.Firefox(executable_path=path)

    template="https://www.cbinsights.com/research-unicorn-companies"
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
