import time
from selenium import webdriver
import pandas as pd
import json
from pandas.io.json import json_normalize
import urllib
from pandas import DataFrame
import requests
import re
from datetime import datetime

today = datetime.today()
datelist = pd.date_range(datetime(2010, 1, 1),datetime(today.year, today.month+1, 1),freq='1M')-pd.offsets.MonthBegin(1)
vacancydatelist = pd.date_range(datetime(2005, 1, 1),datetime(today.year, today.month, 1),freq='1M')-pd.offsets.MonthBegin(1)
yearlist = list(range(1991, 2017, 5))

#https://stackoverflow.com/questions/39864796/how-to-scrape-charts-from-a-website-with-python

listingsURL = 'https://sqmresearch.com.au/total-property-listings.php?postcode={}&t=1'
listingsURL2 = 'https://sqmresearch.com.au/total-property-listings.php?postcode={}&t=1&hu=1'
housesURL = 'https://sqmresearch.com.au/graph.php?postcode={}&mode=8&t=1'
semisURL = 'https://sqmresearch.com.au/graph.php?postcode={}&mode=9&t=1'
unitsURL = 'https://sqmresearch.com.au/graph.php?postcode={}&mode=10&t=1'
vacanciesURL = 'https://sqmresearch.com.au/graph_vacancy.php?postcode={}&t=1'

#https://sqmresearch.com.au/total-property-listings.php?postcode=2089&t=1
#https://sqmresearch.com.au/graph.php?postcode=3146&mode=8&t=1

driver = webdriver.Chrome()
y = 0

try:
    #code = codelist[x]
    code = '2000'
    #print(x, codelist[x], len(codelist))
    #Time Spend on Market
    fullURL = listingsURL.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp1 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    temp2 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[1].options.data')
    temp3 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[2].options.data')
    temp4 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[3].options.data')
    temp5 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[4].options.data')
    data1 = [item[1] for item in temp1]
    data2 = [item[1] for item in temp2]
    data3 = [item[1] for item in temp3]
    data4 = [item[1] for item in temp4]
    data5 = [item[1] for item in temp5]

    #Number of Properties on Market
    fullURL = listingsURL2.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp6 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    temp7 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[1].options.data')
    data6 = [item[1] for item in temp6]
    data7 = [item[1] for item in temp7]

    #Number of Houses
    fullURL = housesURL.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp8 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    data8 = [item[1] for item in temp8]

    #Number of Semis
    fullURL = semisURL.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp9 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    data9 = [item[1] for item in temp9]

    #Number of Units
    fullURL = unitsURL.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp10 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    data10 = [item[1] for item in temp10]

    #vacancies
    fullURL = vacanciesURL.format(code)
    driver.get(fullURL)
    time.sleep(10)
    temp11 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[0].options.data')
    temp12 = driver.execute_script('return window.Highcharts.charts[0]'
                                '.series[1].options.data')
    data11 = [item[1] for item in temp11]
    data12 = [item[1] for item in temp12]
    vacanciestable = pd.DataFrame({'Vacancy Count': data11, 'Vacancy Rate': data12})
    vacanciestable['Vacancy Rate'] = vacanciestable['Vacancy Rate']/100
    vacanciestable.insert(loc=0, column='Postcode', value=code) #creates postcode column at start
    modifieddatelist = vacancydatelist[-len(vacanciestable):]
    vacanciestable['Date'] = modifieddatelist
    if y == 0:
        vacanciestable.to_csv('SQMResearch Vacancies.csv', index=False)
    else:
        vacanciestable.to_csv('SQMResearch Vacancies.csv', mode='a', header=False, index=False)
    #print(vacanciestable)

    #property types table
    listingstypetable = pd.DataFrame({'Houses': data6, 'Units': data7})
    listingstypetable.insert(loc=0, column='Postcode', value=code) #creates postcode column at start
    modifieddatelist = datelist[-len(listingstypetable):]
    listingstypetable['Date'] = modifieddatelist
    if y == 0:
        listingstypetable.to_csv('SQMResearch Listing Types.csv', index=False)
    else:
        listingstypetable.to_csv('SQMResearch Listing Types.csv', mode='a', header=False, index=False)
    #print(listingstypetable)

    #existing properties table
    propertiestypetable = pd.DataFrame({'Houses': data8, 'Semis': data9, 'Units': data10})
    propertiestypetable.insert(loc=0, column='Postcode', value=code) #creates postcode column at start
    modifiedyearlist = yearlist[-len(propertiestypetable):]
    propertiestypetable['Date'] = modifiedyearlist
    if y == 0:
        propertiestypetable.to_csv('SQMResearch Property Types.csv', index=False)
    else:
        propertiestypetable.to_csv('SQMResearch Property Types.csv', mode='a', header=False, index=False)
    #print(propertiestypetable)

    listingsdatetable = pd.DataFrame({'Under 30 Days': data1, '30-60 Days': data2, '60-90 Days': data2, '90-180 Days': data4, 'Over 180 Days': data5})
    listingsdatetable.insert(loc=0, column='Postcode', value=code) #creates postcode column at start
    modifieddatelist = datelist[-len(listingsdatetable):]
    listingsdatetable['Date'] = modifieddatelist
    print(listingsdatetable)
except Exception as e:
    print(e)

driver.close()
exit()
