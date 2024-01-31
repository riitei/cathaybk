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
    """
    管理Selenium WebDriver的生命周期。
    在進入上下文管理時初始化WebDriver，在退出時關閉。
    """

    def __init__(self, browser_type="chrome"):
        """
        構造函數。
        :param browser_type: 瀏覽器類型（默認為chrome）。
        """
        self.browser_type = browser_type
        self.driver = None

    def __enter__(self):
        """
        上下文管理器入口，建立WebDriver實例。
        :return: WebDriver實例。
        """
        self.driver = WebDriverFactory.create_driver(self.browser_type)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出，關閉WebDriver實例。
        """
        self.driver.quit()


# create webDriver and 裝置設定參數
class WebDriverFactory:
    """
    工廠類，用於創建WebDriver實例。
    提供了模擬移動設備的配置選項。
    """
    # 移動設備模擬配置
    mobile_emulation = {
        "deviceMetrics": {"width": 428, "height": 926, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"
    }

    @staticmethod
    def create_driver(browser_type="chrome"):
        """
        根據瀏覽器類型建立WebDriver。
        :param browser_type: 瀏覽器類型。
        :return: WebDriver實例。
        """
        if browser_type == "chrome":
            return WebDriverFactory._create_chrome_driver()
        elif browser_type == "firefox":
            return WebDriverFactory._create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

    @staticmethod
    def _create_chrome_driver():
        """
        建立Chrome WebDriver實例。
        :return: Chrome WebDriver實例。
        """
        options = ChromeOptions()
        options.add_experimental_option("mobileEmulation", WebDriverFactory.mobile_emulation)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(WebDriverFactory.mobile_emulation["deviceMetrics"]["width"],
                               WebDriverFactory.mobile_emulation["deviceMetrics"]["height"])
        return driver

    @staticmethod
    def _create_firefox_driver():
        """
        建立Firefox WebDriver實例。
        :return: Firefox WebDriver實例。
        """
        options = FirefoxOptions()
        # Firefox驅動的建立邏輯（略）


class Command:
    """
    命令類的基類。
    所有命令類都繼承自此類，並需要實現execute方法。
    """

    def __init__(self, driver):
        """
        構造函數。
        :param driver: WebDriver實例。
        """
        self.driver = driver

    def execute(self):
        """
        抽象方法，執行命令。
        需要在子類中實現。
        """
        raise NotImplementedError


# 開啟頁面命令
class OpenPageCommand(Command):
    """
    打開網頁的命令。
    繼承自Command類。
    """

    def __init__(self, driver, url):
        """
        構造函數。
        :param driver: WebDriver實例。
        :param url: 要打開的網址。
        """
        super().__init__(driver)
        self.url = url

    def execute(self):
        """
        執行打開網頁的操作。
        打開指定URL並等待頁面加載完成。
        """
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


# selenium run click 命令模式
class CssClickCommand(Command):
    """
    通過CSS選擇器點擊元素的命令。
    繼承自Command類。
    """

    def __init__(self, driver, css_selector):
        """
        構造函數。
        :param driver: WebDriver實例。
        :param css_selector: CSS選擇器。
        """
        self.driver = driver
        self.css_selector = css_selector

    def execute(self):
        """
        執行點擊操作。
        通過CSS選擇器找到元素並點擊，然後等待頁面加載。
        """
        self.driver.find_element(By.CSS_SELECTOR, self.css_selector).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


# 使用JS控制命令
class JsClickCommand(Command):
    """
    使用JavaScript執行點擊操作的命令。
    繼承自Command類。
    """

    def __init__(self, driver, DOM, name, type=None):
        """
        構造函數。
        :param driver: WebDriver實例。
        :param DOM: 操作的DOM元素。
        :param name: 元素的名稱。
        :param type: 點擊類型，默認為None。
        """
        self.driver = driver
        self.DOM = DOM
        self.name = name
        self.type = type

    def execute(self):
        """
        執行JavaScript點擊操作。
        根據提供的DOM和名稱執行相應的點擊操作。
        """
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
            # selenium run click
            self.driver.find_elements(By.CSS_SELECTOR, self.DOM)[DOM_index].click()
        elif type == 'js_click':
            # js run click
            js_click = """
                var selector = arguments[0];
                var name = arguments[1];
                $(selector).filter(function() {
                    return $(this).text().trim() === name;
                }).click();
            """
            self.driver.execute_script(js_click, self.DOM, self.name)
        else:
            # 回傳 DOM now index value
            return int(DOM_index)


# 同時間開啟網頁截圖
class MultipleWebPagesCommand(Command):
    """
    同時開啟多個網頁並執行截圖的命令。
    繼承自Command類。
    """

    def __init__(self):
        """構造函數。"""
        pass

    def execute(self, url):
        """
        執行開啟網頁和截圖的操作。
        :param url: 要開啟的網址。
        """
        sub_driver = WebDriverFactory().create_driver()
        sub_driver.get(url)
        WebDriverWait(sub_driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        TakeScreenshotCommand(sub_driver, CathayBK().info_path).execute()
        sub_driver.quit()


# 針對卡片處理流程
class CardsCommand(Command):
    """
    處理網頁中卡片元素的命令。
    繼承自Command類。
    """

    def __init__(self, driver, path):
        """
        構造函數。
        :param driver: WebDriver實例。
        :param path: 截圖保存的路徑。
        """
        self.driver = driver
        self.path = path

    def execute(self):
        """
        執行對卡片元素的操作。
        包括點擊卡片、等待加載、截圖等。
        """
        # 目前 class index
        now_index = JsClickCommand(self.driver, '.cubre-a-iconTitle__text', CathayBK().card_name, 'count').execute()
        card_count_js = "return $('.cubre-a-iconTitle__text').eq(%d).parents('div.cubre-o-block__wrap').find('.swiper-pagination-bullet').length" % int(
            now_index)
        # 全部 class 數量
        card_count = int(self.driver.execute_script(card_count_js))
        card_index_js = "return $('.swiper-pagination-bullet').index($('.cubre-a-iconTitle__text').eq(%d).parents('div.cubre-o-block__wrap').find('.swiper-pagination-bullet:first'))" % int(
            now_index)
        card_index = int(self.driver.execute_script(card_index_js))
        # 卡片元素
        cards = self.driver.find_elements(By.CSS_SELECTOR, '.swiper-pagination-bullet')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # 針對每張卡片點選
        for i in range(int(card_index), int(card_index) + int(card_count)):
            cards[i].click()
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            title_index = i - int(card_index)
            title_js = "return $('.swiper-pagination-bullet').eq(%d).parents('div.cubre-o-block__wrap').find('.cubre-m-compareCard__title').eq(%d).text()" % (
                i, title_index)
            title_name = self.driver.execute_script(title_js)
            time.sleep(5)
            TakeScreenshotCommand(self.driver, self.path, title_name).execute()


# 截圖
class TakeScreenshotCommand(Command):
    """
    截圖命令。
    繼承自Command類。
    """

    def __init__(self, driver, path, title_name=None):
        """
        構造函數。
        :param driver: WebDriver實例。
        :param path: 截圖保存的路徑。
        :param title_name: 截圖的標題名稱，默認為None。
        """
        self.driver = driver
        self.path = path
        self.title_name = title_name

    def execute(self):
        """
        執行截圖操作。
        截取當前瀏覽器視窗的畫面並保存。
        """
        if self.title_name is None:
            self.title_name = self.driver.title
        photo_path = os.path.join(self.path, '%s.png' % self.title_name)
        self.driver.save_screenshot(photo_path)


# 參數設定和程式進入點
class CathayBK:
    """
    參數設定和程式進入點。
    用於定義和執行整個網頁爬蟲過程。
    """

    def __init__(self):
        """
        構造函數。
        初始化各種路徑和配置。
        """
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

    # 建立文件
    def setup_directories(self, base_directory, parent_folder):
        """
        建立文件夾。
        在指定的基本目錄下建立所需的文件夾結構。
        :param base_directory: 基本目錄的路徑。
        :param parent_folder: 要建立的父文件夾名稱。
        :return: 建立的文件夾路徑。
        """
        folder_path = os.path.join(base_directory, parent_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    # 測試主流程
    def process(self, url, path):
        """
        測試主流程。
        定義了自動化測試的主要步驟。
        :param url: 要訪問的網站URL。
        :param path: 截圖保存的路徑。
        """
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
        """
        程序的入口點。
        初始化WebDriver並執行自動化流程。
        """
        url = "https://www.cathaybk.com.tw/cathaybk/"
        with WebDriverContextManager() as driver:
            self.driver = driver
            self.process(url, self.index_path)


if __name__ == '__main__':
    CathayBK().main()
