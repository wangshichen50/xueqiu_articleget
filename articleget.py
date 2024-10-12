import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime
import time

url = 'https://xueqiu.com/u/' #目标用户的主页网址
file = open(" ", "w", encoding='utf-8')#文件目标地址

driver = webdriver.Chrome()
time_str = "2024-10-14T14:09:19.056Z"
dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
expiry = int(dt.timestamp())
cookie = {
    'name' : 'xq_a_token',
    'value' : '',
    'path': '/',
    'domain': '.xueqiu.com',
    'secure': False,
    'httpOnly': True,
    'expiry': expiry
}#浏览器中保存的cookie

driver.get(url)
driver.add_cookie(cookie)
driver.refresh()

button = driver.find_element(By.LINK_TEXT, "原发布")
# driver.execute_script("arguments[0].click();", button)
button.click()
#等待元素加载完毕
time.sleep(2)

j = 0
while True:
    j+=1
    button2 = driver.find_element(By.CLASS_NAME, 'profiles__timeline__bd')
    articles = button2.find_elements(By.XPATH, "./*")
    lines = []
    i = 0
    for article in articles:
        try:
            i+=1
            longtext = article.find_element(By.CLASS_NAME,"timeline__item__content.timeline__item__content--longtext")
        except (NoSuchElementException, StaleElementReferenceException): #短文处理，包含是否展开的处理
            info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "date-and-source")))
            lines.append("# "+ info.text +"\n")
            lines.append("page"+str(j)+"item"+str(i)+"\n"+"\n")
            print("# "+ info.text +"\n"+"page"+str(j)+"item"+str(i)+"\n"+"\n")
            try:
                expand_button = article.find_element(By.CLASS_NAME, "timeline__expand__control")
            except (NoSuchElementException, StaleElementReferenceException):
                # main_text  = WebDriverWait(article, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content.content--description")))
                main_text = article.find_element(By.CLASS_NAME, "content.content--description")
                lines.append(main_text.text + "\n")
                print(main_text.text + "\n")
            else:
                expand_button.click()
                time.sleep(1)
                # main_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,
                #                                                                 'content.content--detail')))
                main_text = article.find_element(By.CLASS_NAME, "content.content--detail")
                lines.append(main_text.text + "\n"+"\n")
                print(main_text.text + "\n")

        else: #专栏文章处理
            aref = longtext.find_element(By.XPATH,'./*[1]')
            new_url = aref.get_attribute('href')
            # print(new_url)
            js_script = "window.open('" + new_url + "', 'tmp_window');"
            driver.execute_script(js_script)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            info = driver.find_element(By.CLASS_NAME,"time")
            article_area = driver.find_element(By.CLASS_NAME, 'article__bd')
            title = article_area.find_element(By.XPATH, './*[1]')


            # file.write("#"+title.text+"\n")
            lines.append("# " + title.text + " ")
            lines.append(info.text+"\n")
            lines.append("page"+str(j)+"item"+str(i)+"\n"+"\n")
            print("# " + title.text + " " +info.text+"\n"+"page"+str(j)+"item"+str(i)+"\n"+"\n")
            main_text = article_area.find_element(By.CLASS_NAME, "article__bd__detail").find_elements(By.XPATH, './*')
            for text in main_text:
                tmp_text = text.text.replace('\n', '')
                lines.append(tmp_text + '\n' + '\n')
                print(tmp_text + '\n' + '\n')

            driver.switch_to.window(driver.window_handles[0])

    file.writelines(lines)

    page_button = driver.find_element(By.LINK_TEXT, str(j + 2));
    button_nextPage = driver.find_element(By.CLASS_NAME, "pagination__next")

    try:
        button_nextPage.click()
    except Exception :
        break

    #等待换页后元素加载完毕
    time.sleep(3)


time.sleep(100)
driver.quit()






