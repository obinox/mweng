from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, re, json, datetime


debugging = False
delay = 0.05

def debug(*args):
    if debugging:
        print(*args)

class ImageDownloader:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.cheeses = []
        self.channals = {}

    def login(self):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        input()
        time.sleep(1) 

    def wait_for_page_load(self, url):
        self.driver.get(url)
        time.sleep(2) 

    def getcheese(self):
        self.wait_for_page_load(self.url)
        welcome = self.driver.find_element(By.CSS_SELECTOR, "[class*='welcomePopup_button_close']") 
        if welcome:
            welcome.click()
            time.sleep(delay)

        dropdown = self.driver.find_elements(By.CSS_SELECTOR, "[class*='selectbox_button']")
        
        syear = 2023
        cyear = datetime.datetime.now().year
        cmonth = datetime.datetime.now().month

        for i in range(syear, cyear + 1):
            dropdown[0].click()
            debug("dropdown0", dropdown[0])
            time.sleep(delay)

            years = self.driver.find_elements(By.CSS_SELECTOR, "[class*='selectbox_option']")
            years[len(years) - 1 - (i - syear) ].click()
            debug("year", i, years[-1 - i + syear])
            time.sleep(delay)

            for j in range(cmonth if cyear == i else 12):
                dropdown[1].click() 
                debug("dropdown1", dropdown[1])
                time.sleep(delay)

                months = self.driver.find_elements(By.CSS_SELECTOR, "[class*='selectbox_option']")

                months[j].click()
                debug("month", j, months[j])
                time.sleep(delay)
                
                k = True
                while (nextpage := self.driver.find_elements(By.CSS_SELECTOR, "[class*='pagination_button_next']")) or k:
                    k = bool(nextpage)
                    pages = self.driver.find_elements(By.CSS_SELECTOR, "[class*='pagination_page']")
                    for page in pages:
                        page.click()
                        debug("page", page)
                        time.sleep(delay)

                        table = self.driver.find_element(By.CSS_SELECTOR, "[class*='table_wrapper']")
                        tableempty = self.driver.find_elements(By.CSS_SELECTOR, "[class*='table_empty']")
                        if len(tableempty) > 0:
                            continue

                        tbody = table.find_element(By.TAG_NAME, "tbody")
                        rows = tbody.find_elements(By.CSS_SELECTOR, "tr")
                        for row in rows:
                            cells = row.find_elements(By.CSS_SELECTOR, "td")
                            debug(cells[0].text)

                            date_str, time_str = cells[0].text.split('\n')
                            datetime_str = f"{date_str} {time_str}"
                            timestamp = datetime.datetime.strptime(datetime_str, "%Y.%m.%d %H:%M:%S").timestamp()               
                            cheese = ''.join(re.findall(r'\d', cells[1].text))
                            category = cells[2].text
                            channel = cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")

                            self.cheeses.append({"timestamp": timestamp, "cheese": cheese, "category": category, "channel": channel})
                            self.channals[channel] = None

                            if len(cells) >= 2:
                                debug(cells[1].text)

                    if len(nextpage) > 0:
                        nextpage[0].click()
                        debug("nextpage", nextpage[0])
                        time.sleep(delay)

        with open("cheeses.json", "w", encoding="utf-8") as f:
            json.dump(self.cheeses, f, ensure_ascii=False, indent=4)
            
        time.sleep(1)

    def channelfind(self):
        for channel in self.channals.keys():
            self.driver.get(channel)
            time.sleep(delay)
            name = self.driver.find_element(By.CSS_SELECTOR, "[class*='name_text']")
            self.channals[channel] = name.text
        with open("channals.json", "w", encoding="utf-8") as f:
            json.dump(self.channals, f, ensure_ascii=False, indent=4)
        time.sleep(1)


    def close(self):
        
        self.driver.quit()


# 사용 예시
url = "https://game.naver.com/profile#cash"

# 이미지 다운로드 시작
downloader = ImageDownloader(url)
downloader.login()  # 로그인
downloader.getcheese()
downloader.channelfind()
downloader.close()
