from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import pandas as pd

path = # add path of chrome driver
website = 'https://www.bseindia.com/corporates/ann.html'

# <---------- Default Operations ----------->

op = Options()
op.add_argument("--incognito")
op.add_argument("--headless")
op.add_argument("--maximize_window")
driver = webdriver.Chrome(options=op, executable_path=path)
driver.maximize_window()
driver.delete_all_cookies()
driver.get(website)
time.sleep(10)

# <------ current date --------->

now = date.today().strftime("%d/%m/%Y")
print(now)

# <------ total number of announcements --------->

num_of_announcements = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div[1]/div[1]/div[2]')
print(num_of_announcements.text)


# <----------- segment, category, from date, to date bars ------------->

segment_bar = driver.find_element_by_id('ddlAnnType')
segment_bar.send_keys('Equity')
# category_bar = driver.find_element_by_id('ddlPeriod')
# category_bar.send_keys('Result')
# from_date_bar = driver.find_element_by_id('txtFromDt')
# from_date_bar.clear()
# dates = driver.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table//a')
# from_date_bar.send_keys("31122022")
# to_bar = driver.find_element_by_id('txtToDt')
# to_bar.clear()
# to_bar.send_keys("31122022")

# <-------- click submit button ----------->

submitbtn = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[1]/div[3]/div[5]/input[1]')
driver.execute_script("arguments[0].click();", submitbtn)

# <--------- check if announcements are available ---------->

try:
    data = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div/div[2]').text
    if data == "No Records Found":
        print("No Records Found")
except:
    pass


# <------- Displaying Data ---------->

pd.set_option('display.max_colwidth', None)
col_names = ["Symbol", "Subject", "Date", "More Info", "PDF Link", "Category"]
df = pd.DataFrame(columns=col_names)

# <------- Getting data from all announcement pages --------->

while True:
    rows = len(driver.find_elements_by_xpath('/html/body/div[1]/div[5]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table'))
    print("rows : ", rows)

    for r in range(1, rows+1):
        column_info = []
        my_links = driver.find_elements_by_xpath('/html/body/div[1]/div[5]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[1]/a'.format(str(r)))

        for link in my_links:
            driver.execute_script("arguments[0].click();", link)
            symbol = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[2]').get_attribute("textContent")
            subject = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td').get_attribute("textContent")
            date = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[3]/td/b[1]').get_attribute("textContent")
            time.sleep(1)

            try:
                more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[5]/td').get_attribute("textContent")
            except:
                more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[6]/td').get_attribute("textContent")
                pass

            try:
                pdf = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[5]/a').get_attribute('href')
            except Exception as e:
                # print(e)
                pdf = 'NO PDF'
                pass

            column_info.extend([symbol, subject, date, more_info, pdf])

            # <------ close button -------->

            try:
                driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/button').click()
            except:
                pass
            time.sleep(0.1)

        try:
            category = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[2]'.format(str(r))).get_attribute("textContent")

        except:
            pass

        column_info.append(category)
        print(column_info)
        df.loc[len(df)] = column_info

    try:
        nextbtn = driver.find_element_by_id('idnext')
        driver.execute_script("arguments[0].click();", nextbtn)
        time.sleep(10)
        chwd = driver.window_handles
        driver.switch_to.window(chwd[-1])
        print("Next Page")

    except:
        print("page not changed")
        break


print("Processing BSE DATA")
print(df)
df.to_csv(r'# add file path', index=False)





