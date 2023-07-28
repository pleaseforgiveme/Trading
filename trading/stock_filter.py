import requests
import os
from bs4 import BeautifulSoup
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

'''
1. Find stocks with earnings post market today and pre market tomorrow (probably from https://ca.investing.com/earnings-calendar/)
    1.1 Fetch data from https://ca.investing.com/earnings-calendar/
    1.2 Filter stocks to leave only US stocks. Generate a list of the results  
2.  (From tradingView) fetch the past 3 price fluctuations post earnings, and record all of them.
    2.1 Also snapshot RSI
3. From Etrade or https://www.optionsprofitcalculator.com/calculator/strangle.html, fetch the option prices
4. Compare the results of 2 and 3, sort it by fluctuations/option prices. Choose to buy if this is at least 100%.
5. Generate reports, send emails or alerts to notice if action is needed.
'''

def get_data_by_chrome():
    # Set up ChromeDriver path
    chrome_driver_path = '/usr/local/bin/chromedriver'  # which chromedriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run ChromeDriver in headless mode (without opening a browser window)
    service = Service(chrome_driver_path)

    # Start the WebDriver session
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the earnings calendar page
    url = 'https://ca.investing.com/earnings-calendar/'
    driver.get(url)
    table = driver.find_element(By.ID, 'earningsCalendarData')

    # Find all the rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # print("~~~~~~")
    # print(rows)
    # print("~~~~~~")
    for row in rows[1:20]:  # Skip the header row.  
        # e.g.  <selenium.webdriver.remote.webelement.WebElement (session="53f26be816bdd8e7e2e67dbaed291f44", element="7135750921C791EE2D1DA05A16A62C95_element_70")>
        cells = row.find_elements(By.TAG_NAME, 'td')
        # print("sdfsdf: " + str(cells))
        if len(cells) >= 7:
            company_name = cells[1].text.strip()
            earnings_time_col = cells[7].find_elements(By.TAG_NAME, 'span')
            if len(earnings_time_col) > 0:
                earnings_time_description = earnings_time_col[0].get_attribute("data-tooltip")
                if earnings_time_description is not None:
                    earning_time = earnings_time_description.split(" ")
                    if len(earning_time) > 0:
                        before_or_after = earning_time[0]
                        print(company_name + ", " + before_or_after)

    # Quit the WebDriver session
    driver.quit()



# def get_earnings_data():
#     url = "https://ca.investing.com/earnings-calendar/"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
#     print("sss:**********" + str(response))
    # soup = BeautifulSoup(response.content, 'html.parser')
    # table = soup.find('table', {'id': 'earningsCalendarData'})
    # rows = table.find_all('tr')
    # earnings_data = []
    # for row in rows[1:]: # Skip the header row
    #     cols = row.find_all('td')
    #     if len(cols) > 0:
    #         time_col = cols[4].find('span')
    #         if time_col:
    #             time = time_col.get('class')[0]
    #             company = cols[0].text.strip()
    #             if time == 'js-event-img sun':
    #                 earnings_data.append({'company': company, 'time': 'pre'})
    #             elif time == 'js-event-img moon':
    #                 earnings_data.append({'company': company, 'time': 'post'})
    # return earnings_data

# def get_earnings_data():
#     filename = "earnings_calender.html"
#     if not os.path.isfile(filename):
#         print("Error: File not found.")
#         return

#     with open(filename, "r", encoding="utf-8") as f:
#         content = f.read()
#     soup = BeautifulSoup(content, "html.parser")
#     print(soup)
#     table = soup.find("table", {"id": "economicCalendarData"})
#     rows = table.find_all("tr")
#     for row in rows:
#         cols = row.find_all("td")
#         if len(cols) > 1:
#             symbol = cols[0].text.strip()
#             time = cols[4].text.strip()
#             if "pm" in time.lower():
#                 # post market today
#                 print(symbol, "post market today")
#             elif "am" in time.lower():
#                 # pre market tomorrow
#                 print(symbol, "pre market tomorrow")

def filter_stocks(earnings_data, symbols):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    post_market_today = [d['company'] for d in earnings_data if d['time'] == 'post']
    pre_market_tomorrow = [d['company'] for d in earnings_data if d['time'] == 'pre']
    filtered_stocks = []
    for symbol in symbols:
        if symbol in post_market_today and symbol in pre_market_tomorrow:
            earnings_history = get_earnings_history(symbol)
            if earnings_history is not None and len(earnings_history) >= 3:
                earnings_history = earnings_history[-3:]
                earnings_percent_change = [float(h['change_percent'].replace('%', '')) for h in earnings_history]
                if abs(sum(earnings_percent_change) / len(earnings_percent_change)) >= 10:
                    filtered_stocks.append(symbol)
    return filtered_stocks

def get_earnings_history(symbol):
    url = "https://www.alphavantage.co/query"
    function = "EARNINGS"
    apikey = "PNFGZJ7E5N87IO8W"
    params = {"function": function, "symbol": symbol, "apikey": apikey}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "quarterlyEarnings" in data:
            earnings = data["quarterlyEarnings"]
            if len(earnings) < 3:
                return None
            change_percents = []
            for i in range(-3, 0):
                quarter = earnings[i]
                change_percent = quarter["reportedEPS"] / quarter["estimatedEPS"] - 1
                change_percents.append(change_percent)
            avg_change_percent = sum(change_percents) / len(change_percents)
            if avg_change_percent >= 0.1:
                return avg_change_percent
    return None

get_data_by_chrome()
#earnings_data = get_earnings_data()
#print(earnings_data)
#filtered_stocks = filter_stocks(earnings_data, earnings_data)
#print(filtered_stocks)
