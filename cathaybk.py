import os
import time
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class WebDriverContextManager:
    def __init__(self, browser_type="chrome"):
        self.browser_type = browser_type
        self.driver = None

    def __enter__(self):
        self.driver = WebDriverFactory.create_driver(self.browser_type)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class WebDriverFactory:
    mobile_emulation = {
        "deviceMetrics": {"width": 428, "height": 926, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"
    }

    @staticmethod
    def create_driver(browser_type="chrome"):
        if browser_type == "chrome":
            return WebDriverFactory._create_chrome_driver()
        elif browser_type == "firefox":
            return WebDriverFactory._create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

    @staticmethod
    def _create_chrome_driver():
        options = ChromeOptions()
        options.add_experimental_option("mobileEmulation", WebDriverFactory.mobile_emulation)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(WebDriverFactory.mobile_emulation["deviceMetrics"]["width"],
                               WebDriverFactory.mobile_emulation["deviceMetrics"]["height"])
        return driver

    @staticmethod
    def _create_firefox_driver():
        options = FirefoxOptions()
        # 在此处配置 Firefox 选项
        # ...


class Command:
    def __init__(self, driver):
        self.driver = driver
    def execute(self):
        raise NotImplementedError

class OpenPageCommand(Command):
    def __init__(self, driver, url):
        super().__init__(driver)
        self.url = url

    def execute(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


class CssClickCommand(Command):
    def __init__(self, driver, css_selector):
        self.driver = driver
        self.css_selector = css_selector
    def execute(self):
        self.driver.find_element(By.CSS_SELECTOR, self.css_selector).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


class JsClickCommand(Command):
    def __init__(self, driver, DOM, name, type=None):
        self.driver = driver
        self.DOM = DOM
        self.name = name
        self.type = type

    def execute(self):
        js = """
            var selector = arguments[0];
            var name = arguments[1];
            var targetIndex = -1;
            $(selector).each(function(index) {
                if ($(this).text().trim() === name) {
                    targetIndex = index;
                    return false;
                }
            });
            return targetIndex;
        """
        DOM_index = self.driver.execute_script(js, self.DOM, self.name)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        if self.type is None:
            self.driver.find_elements(By.CSS_SELECTOR, self.DOM)[DOM_index].click()
        elif type == 'js_click':
            js_click = """
                var selector = arguments[0];
                var name = arguments[1];
                $(selector).filter(function() {
                    return $(this).text().trim() === name;
                }).click();
            """
            self.driver.execute_script(js_click, self.DOM, self.name)
        else:
            return int(DOM_index)

class MultipleWebPagesCommand(Command):
    def __init__(self):
        pass

    def execute(self, url):
        sub_driver = WebDriverFactory().create_driver()
        sub_driver.get(url)
        WebDriverWait(sub_driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        TakeScreenshotCommand(sub_driver, CathayBK().info_path).execute()
        sub_driver.quit()


class CardsCommand(Command):
    def __init__(self, driver, path):
        self.driver = driver
        self.path = path

    def execute(self):
        now_index = JsClickCommand(self.driver, '.cubre-a-iconTitle__text', CathayBK().card_name, 'count').execute()
        card_count_js = "return $('.cubre-a-iconTitle__text').eq(%d).parents('div.cubre-o-block__wrap').find('.swiper-pagination-bullet').length" % int(
            now_index)
        card_count = int(self.driver.execute_script(card_count_js))
        card_index_js = "return $('.swiper-pagination-bullet').index($('.cubre-a-iconTitle__text').eq(%d).parents('div.cubre-o-block__wrap').find('.swiper-pagination-bullet:first'))" % int(
            now_index)
        card_index = int(self.driver.execute_script(card_index_js))
        cards = self.driver.find_elements(By.CSS_SELECTOR, '.swiper-pagination-bullet')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        for i in range(int(card_index), int(card_index) + int(card_count)):
            cards[i].click()
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            title_index = i - int(card_index)
            title_js = "return $('.swiper-pagination-bullet').eq(%d).parents('div.cubre-o-block__wrap').find('.cubre-m-compareCard__title').eq(%d).text()" % (
                i, title_index)
            title_name = self.driver.execute_script(title_js)
            time.sleep(5)
            TakeScreenshotCommand(self.driver, self.path, title_name).execute()

class TakeScreenshotCommand(Command):
    def __init__(self, driver, path, title_name=None):
        self.driver = driver
        self.path = path
        self.title_name = title_name

    def execute(self):
        if self.title_name is None:
            self.title_name = self.driver.title
        photo_path = os.path.join(self.path, '%s.png' % self.title_name)
        self.driver.save_screenshot(photo_path)


# 主类
class CathayBK:

    def __init__(self):
        base_directory = os.getcwd()
        parent_folder = 'photo'
        folder_path = self.setup_directories(base_directory, parent_folder)
        self.index_path = self.setup_directories(folder_path, 'index')
        self.info_path = self.setup_directories(folder_path, 'info')
        self.card_path = self.setup_directories(folder_path, 'card_path')
        self.driver = WebDriverFactory.create_driver()
        self.item_name = '產品介紹'
        self.product_name = '信用卡'
        self.card_info_name = '卡片介紹'
        self.card_name = '停發卡'

    # 创建必要的文件夹
    def setup_directories(self, base_directory, parent_folder):
        folder_path = os.path.join(base_directory, parent_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    # 执行导航和截图命令
    def process(self, url, path):
        # 網站
        OpenPageCommand(self.driver, url).execute()
        TakeScreenshotCommand(self.driver, path).execute()
        # 菜單
        CssClickCommand(self.driver, '.cubre-a-burger__img.-close').execute()
        # 產品介紹
        JsClickCommand(self.driver, '.cubre-a-menuSortBtn.-l1', self.item_name).execute()
        # 信用卡
        JsClickCommand(self.driver, '.cubre-a-menuSortBtn', self.product_name).execute()
        # 信用卡產品
        product_group = self.driver.find_elements(By.CSS_SELECTOR, '.cubre-o-menuLinkList__item.is-L2open a')
        urls = [product.get_attribute('href') for product in product_group]  # Ex
        with Pool(5) as pool:
            pool.map(MultipleWebPagesCommand().execute, urls)
        # 卡片介紹
        JsClickCommand(self.driver, '.cubre-a-menuLink', self.card_info_name).execute()
        # 卡片
        JsClickCommand(self.driver, '.cubre-m-anchor__btn.swiper-slide', self.card_name, 'js_click').execute()
        #  停發卡 invalid card
        CardsCommand(self.driver, self.card_path).execute()

    def main(self):
        url = "https://www.cathaybk.com.tw/cathaybk/"
        with WebDriverContextManager() as driver:
            self.driver = driver
            self.process(url, self.index_path)

if __name__ == '__main__':
    CathayBK().main()
