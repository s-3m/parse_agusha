import time
from pprint import pprint

from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.ozon.ru/"

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Прокрутка вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Пауза, пока загрузится страница.
        time.sleep(2)
        # Вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Прокрутка завершена")
            break
        last_height = new_height
        print("Появился новый контент, прокручиваем дальше")

    # driver.execute_script('''
    #     const scrollStep = 200;
    #     const scrollInterval = 100;
    #     const scrollHeight = document.documentElement.scrollHeight;
    #     let currenePosition = 0;
    #     const interval = setInterval(() => {
    #         window.scrollBy(0, scrollStep);
    #         currenePosition += scrollStep;
    #
    #         if (currenePosition >= scrollHeight) {
    #             clearInterval(interval);
    #         }
    #     }, scrollInterval);
    # ''')


def get_items(item_name = "конфитюр"):
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    all_elem_on_page = []
    driver.get(BASE_URL)
    time.sleep(2)

    find_input = driver.find_element(By.NAME, "text")
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)
    scroll_page(driver)
    time.sleep(10)

    page_text = driver.page_source

    soup = BeautifulSoup(page_text, "lxml")

    containers = soup.find_all("div", class_="widget-search-result-container")
    for container in containers:
        all_items = container.find_all("div", attrs={"data-index": True})
        all_elem_on_page.extend(all_items)

    driver.close()
    driver.quit()

    result_dict = []

    for item_elem in all_elem_on_page:
        link = BASE_URL + item_elem.find("a")["href"]
        price = item_elem.find('a').find_next_sibling("div").find("div").find('span').text.strip()
        price = price.replace(u'\u2009', '')
        result_dict.append({"link": link,
                            "price": price})

    pprint(result_dict)

def main():
    get_items()


if __name__ == '__main__':
    main()
