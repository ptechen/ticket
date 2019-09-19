#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying
import redis
import json



CHAOJIYING_USERNAME = '15736755067'
CHAOJIYING_PASSWORD = 'TC15736755067'
CHAOJIYING_SOFT_ID = 899053
CHAOJIYING_KIND = 1902
CHAOJIYING_KIND1 = 1005
chrome_options = webdriver.ChromeOptions()
#无头模式
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920,1080')
chrome_options.add_argument('--disable-gpu')
#实例化Chrome driver823
# driver=webdriver.Chrome(chrome_options=chrome_options)


class RedisConn(object):

    def write(self, params):
        red = redis.Redis(host='47.56.66.23', password='123456', port=6379, db=0)
        params_str = json.dumps(params)
        red.sadd("key", params_str)

    def get_redis(self):
        flage = True
        while flage:
            red = redis.Redis(host='47.56.66.23', password='123456', port=6379, db=0)
            value = red.spop("key")
            if value == None:
                time.sleep(10)
                continue
            value_d = json.loads(value)
            return value_d


class CrackTouClick(object):

    def __init__(self, params):

        self.url = 'http://www.baidu.com'
        self.KeyUrl = 'https://ticket.urbtix.hk/internet/zh_TW/eventDetail/38663'
        self.browser = webdriver.Chrome(options=chrome_options)
        # self.browser = webdriver.Chrome()
        self.browser_headless = True
        self.wait = WebDriverWait(self.browser, 20)
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        # self.pool = redis.ConnectionPool(host='47.56.66.23', password='123456', port=6379, db=0, max_connections=2)
        # self.red = redis.Redis(connection_pool=self.pool)
        self.params = params

    def __del__(self):
            self.browser.close()

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_element(self, kind):
        """
        获取验证图片对象
        :return: 图片对象
        """
        element = ""
        if kind == 1:
            self.wait.until(EC.presence_of_element_located((By.ID, 'captchaImage')))
            element = self.browser.find_element_by_xpath('//*[@id="captchaImage"]')
            # element = self.wait.until(EC.presence_of_element_located((By.ID, 'captchaImage')))
        elif kind == 2:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#captcha-image-input-key-container > table > tbody > tr')))
            element = self.browser.find_element_by_xpath('//*[@id="captcha-image-input-key-container"]/table/tbody/tr[1]')
        elif kind == 3:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#captcha-image-input-key-container > table > tbody')))
            element = self.browser.find_element_by_xpath('//*[@id="captcha-image-input-key-container"]/table/tbody/tr[2]')
        return element

    def get_position(self, kind):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_touclick_element(kind)
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        time.sleep(5)
        # 424,474,703,823
        # 533 583 622 872
        # 583 633 622 872
        return top, bottom, left, right

    def get_touclick_image(self, kind=1):
        """
        获取验证码图片
        :return: 图片对象
        """
        name = "captcha{}.png".format(kind)
        top, bottom, left, right = self.get_position(kind)
        print(top, bottom, left, right)
        im = self.get_screenshot()
        self.browser.save_screenshot('full_snap.png')
        # if kind == 1 and self.browser_headless:
        self.browser.save_screenshot('full_snap.png')
        image = Image.open('full_snap.png')
        resized_image = image.resize((1920, 1080), Image.ANTIALIAS)
        resized_image.save('full_snap.png')

        im = Image.open('full_snap.png')
        # im = Image.open(name)
        captcha = im.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_picture_result(self, kind):
        image = self.get_touclick_image(kind)
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # # # 识别验证码
        if kind == 1:
            CHAOJIYING_CODE = CHAOJIYING_KIND
        else:
            CHAOJIYING_CODE = CHAOJIYING_KIND1
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_CODE)
        print(result)
        return result['pic_str']

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        # self.params = self.get_redis()
        self.browser.get(self.url)
        search = self.wait.until(EC.presence_of_element_located((By.ID, 'kw')))
        search.send_keys("城市售票网")
        baidu_click = self.wait.until(EC.presence_of_element_located((By.ID, 'su')))
        baidu_click.click()
        spw = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1"]/h3/a[1]')))
        spw.click()
        self.browser.switch_to.window(self.browser.window_handles[1])
        print(self.browser.current_url)
        if self.browser.current_url == "https://busy.urbtix.hk/redirect.html" or \
                self.browser.current_url == "http://busy.urbtix.hk/redirect.html":
            time.sleep(1)
            try:
                self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td/a').click()
            except Exception as E:
                print(E)

    def check_current_page_url(self):
        key = 0
        while True:
            print("key: ", key)
            try:
                if key == 0:
                    self.browser.find_element_by_xpath('//*[@id="to-hot-event-btn"]').click()
                    key = 1
            except Exception as E:
                print(E)
            if self.browser.current_url == "https://ticket.urbtix.hk/internet/zh_TW/eventDetail/39311":
                html = self.browser.page_source
                kk =PyQuery(html)
                aa = kk.find("#evt-ava-perf-content").find("tr").find("img")
                num = 0
                for a in aa:
                    aaa = PyQuery(a).attr("title")
                    print(aaa)
                    if aaa == "查看門票詳情":
                        num += 1
                    if aaa == "購買門票":
                        break
                self.browser.find_element_by_xpath('//*[@id="evt-perf-items-tbl"]/tbody/tr[{}]/td[6]/div/img'.format(num)).click()
                break
            if self.browser.current_url == "https://busy.urbtix.hk/redirect.html" or \
                    self.browser.current_url == "http://busy.urbtix.hk/redirect.html":
                time.sleep(1)
                try:
                    self.browser.find_element_by_xpath(
                        '/html/body/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td/a').click()
                except Exception as E:
                    print(E)
            time.sleep(0.1)
            
    def refresh(self):
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/table/tbody/tr[3]/td[2]/table/tbody/tr[16]/td/img[2]').click()
        time.sleep(2)

    def click_code(self, key_index):
        for index in key_index:
            if index < 5:
                self.browser.find_element_by_xpath('//*[@id="captcha-image-input-key-container"]/table/tbody/tr[1]/td[{}]/img'.format(index + 1)).click()
            else:
                index = index - 5
                self.browser.find_element_by_xpath(
                    '//*[@id="captcha-image-input-key-container"]/table/tbody/tr[2]/td[{}]/img'.format(
                        index + 1)).click()
            time.sleep(0.2)

    def login_click(self):
        """
        登录
        :return: None
        """
        self.browser.find_element_by_xpath('//*[@id="login-submit"]/div/div').click()
        time.sleep(2)
        print('login success')

    def fei_vip(self):
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/table/tbody/tr[3]/td[2]/table/tbody/tr[8]/td/fieldset/input').click()
        key_index = []
        while True:
            index = []
            result_str = list()
            result = self.get_picture_result(1)
            for i in result:
                if i.isdigit():
                    result_str.append(i)
                elif i not in result_str:
                    result_str.append(i.lower())
            if len(result_str) != 4:
                self.refresh()
                continue
            str_list = list()
            result = self.get_picture_result(2)
            for i in result:
                if i.isdigit():
                    str_list.append(i)
                elif i.lower() in str_list and i.lower() not in result_str:
                    str_list.append(i.lower())
                else:
                    str_list.append(i.lower())
            if len(str_list) != 5:
                self.refresh()
                continue
            result = self.get_picture_result(3)
            for i in result:
                if i.isdigit():
                    str_list.append(i)
                elif i.lower() in str_list and i.lower() not in result_str:
                    str_list.append(i.lower())
                else:
                    str_list.append(i.lower())
            if len(str_list) != 10:
                self.refresh()
                continue
            result_list = list(result_str)
            for i in result_list:
                if not i.isdigit():
                    for k, v in enumerate(str_list):
                        if i == v:
                            index.append(k)
                else:
                    if int(i) != 0:
                        for k, v in enumerate(str_list):
                            if i == v:
                                index.append(k)
                    else:
                        for k, v in enumerate(str_list):
                            if i == v or i == 'o':
                                index.append(k)
            if len(index) != 4:
                self.refresh()
                continue
            key_index = index
            break

        self.click_code(key_index)
        self.login_click()

    def choose_ticker_num(self):
        # print("start choose_ticker_num")
        self.wait.until(EC.presence_of_element_located((By.ID, 'ticket-quota-223-sel')))
        html = self.browser.page_source.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
        options = PyQuery(html).find('#ticket-quota-223-sel > option')
        num = PyQuery(options[-1]).val()
        self.browser.find_element_by_xpath('//*[@id="ticket-quota-223-sel"]').send_keys(4)
        # self.browser.find_element_by_xpath('//*[@id="ticket-quota-223-sel"]').send_keys(int(num))
        self.browser.find_element_by_xpath('//*[@id="adjacent-seats-chk"]').click()
        try:
            self.browser.find_element_by_xpath('//*[@id="express-purchase-btn"]/div/span').click()
        except:
            self.browser.find_element_by_xpath('//*[@id="free-seat-purchase-btn"]/div/div/span').click()
        try:
            self.browser.find_element_by_xpath('/html/body/div[9]/div[3]/div/button[1]').click()
        except Exception as E:
        #     self.browser.find_element_by_xpath('//*[@id="reviewTicketForm"]/div[8]/div/div').click()
            print(E)
        print("end choose_ticket_num")

    def insert_shopping(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="checkbox-not-adjacent"]').click()
        except Exception as E:
            print(E)
            pass
        try:
            self.browser.find_element_by_xpath('//*[@id="reviewTicketForm"]/div[9]/div/div').click()
        except Exception as E:
            print(E)
            try:
                self.browser.find_element_by_xpath('//*[@id="reviewTicketForm"]/div[8]/div/div').click()
            except Exception as E:
                print(E)
        print("end insert shopping")
        # self.browser.save_screenshot("insert_shopping.png")

    def payment_area(self):
        print("start payment_area")
        time.sleep(1)
        try:
            self.browser.find_element_by_xpath('//*[@id="checkout-btn"]/div/div').click()
        except Exception as E:
            print(E)
            try:
                self.browser.find_element_by_xpath('//*[@id="checkbox-not-adjacent"]').click()
            except Exception as E:
                print(E)

        print("end payment_area")

    def personal_data(self):
        self.wait.until(EC.presence_of_element_located((By.ID, 'delivery-method-select')))
        self.browser.find_element_by_xpath('//*[@id="input-surname"]').clear()
        self.browser.find_element_by_xpath('//*[@id="input-surname"]').send_keys("cao")
        self.browser.find_element_by_xpath('//*[@id="input-first-name"]').clear()
        self.browser.find_element_by_xpath('//*[@id="input-first-name"]').send_keys('cao')
        self.browser.find_element_by_xpath('//*[@id="input-email"]').clear()
        self.browser.find_element_by_xpath('//*[@id="input-email"]').send_keys(self.params.get('email'))
        self.browser.find_element_by_xpath('//*[@id="delivery-method-select"]').click()
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="delivery_method_group_TDM"]').click()

    def choose_pay_mei(self):
        print("start choose_pay")

        self.browser.find_element_by_xpath('//*[@id="payment-type-select_title"]').click()
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="payment-type-select_child"]/ul/li[4]/img').click()
        time.sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="input-card-number"]').send_keys(
            self.params.get('input_card_number'))
        time.sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="input-security-code"]').send_keys(
            self.params.get('input_security_code'))
        time.sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="payment-expiry-month-select"]').send_keys(
            self.params.get('payment_expiry_month_select'))
        time.sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="payment-expiry-year-select"]').send_keys(
            self.params.get('payment_expiry_year_select'))
        time.sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="button-confirm"]/div/div/span').click()
        print("end choose_pay")
        self.browser.save_screenshot("choose_pay.png")

    def confirm_mei(self):
        print("start_confirm_mei")
        self.browser.find_element_by_xpath('//*[@id="checkbox-tnc"]').click()
        self.browser.find_element_by_xpath('//*[@id="button-confirm"]/div/div/span').click()
        print("end confirm_mei")

    def run(self):
        self.open()
        self.check_current_page_url()
        self.fei_vip()
        time.sleep(1)
        self.choose_ticker_num()
        self.insert_shopping()
        self.payment_area()
        self.personal_data()
        self.choose_pay_mei()
        self.confirm_mei()
        time.sleep(60)


if __name__ == '__main__':
    while True:
        redisConn = RedisConn()
        params = redisConn.get_redis()
        while time.time() < params.get('start_time', 0):
            print("wait")
            time.sleep(1)
        print("start")
        crack = CrackTouClick(params)
        crack.run()
