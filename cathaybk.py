import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class main:
    def __init__(self):
        self.item_name = '產品介紹'
        self.product_name = '信用卡'
        self.mobile_emulation = {
            "deviceMetrics": {"width": 428, "height": 926, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"
        }

    def chrome_driver_manager(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", self.mobile_emulation)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def item(self, items):
        for item in items:
            # 產品介紹
            if item.text == self.item_name:
                item.click()
                return item

    def product(self, products):
        for product in products:
            if product.text == self.product_name:
                product.click()
                time.sleep(30)
                return product

    def main(self):
        driver = self.chrome_driver_manager()
        # 01 首頁
        driver.get("https://www.cathaybk.com.tw/cathaybk/")
        time.sleep(5)
        # 02 菜單
        driver.find_element(By.CSS_SELECTOR, ".cubre-a-burger__img.-close").click()
        # time.sleep(5)
        # 03 個人金融
        # driver.find_element(By.CSS_SELECTOR, ".cubre-a-menuLink.-channel.is-active").click()
        # print('03')
        time.sleep(5)
        # 03 產品介紹
        # productDescriptionJS = "$('.cubre-a-menuSortBtn.-l1').each((k,v)=>{if($(v).text().trim() === '%s' ) {$(v).click()})})" % '產品介紹'
        # driver.execute_script(productDescriptionJS)
        products = self.item(driver.find_elements(By.CSS_SELECTOR, ".cubre-a-menuSortBtn.-l1"))
        # 信用卡
        # driver = self.product(products)
        #
        #driver = driver.find_element(By.CSS_SELECTOR, ".cubre-a-burger__img.-close")
        # time.sleep(30)
        driver.quit()


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main.main()
# $('.cubre-a-menuSortBtn.-l1').each((k,v)=>{if($(v).text().trim() ==='產品介紹')console.log($(v).text())})
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
