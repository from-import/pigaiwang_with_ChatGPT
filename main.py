import openai
import json
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import multiprocessing

# Clash 配置
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 配置OpenAI API凭证
openai.api_key = ""

def chatgpt(message):
    # 发送请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s"% openai.api_key
    }

    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [{"role": "user", "content": "%s" % message}],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json().get("choices")[0].get("message").get("content")


def write_pg(account,password,number):

    result=""
    o = Options()
    o.add_argument('--disable-infobars')

    username = account
    password = password
    num = number

    driver = webdriver.Firefox()
    driver.get("http://www.pigai.org/")
    sleep(0.3)
    driver.find_element("xpath", '//*[@id="username"]').send_keys(username)
    driver.find_element("xpath", '//*[@id="password"]').send_keys(password)
    butt_login = driver.find_element("xpath", '//*[@id="ulogin"]/img')
    driver.execute_script("arguments[0].click();", butt_login)
    sleep(1)
    driver.find_element("xpath", '/html/body/div[4]/div[3]/form/div[2]/input[1]').click()
    sleep(0.3)


    driver.find_element("xpath", '/html/body/div[4]/div[3]/form/div[2]/input[1]').send_keys(num)
    driver.find_element("xpath", '/html/body/div[4]/div[3]/form/div[3]/button').click()
    sleep(1)

    topic = driver.find_element("xpath", '//*[@id="request_y"]').get_attribute('innerHTML')
    soup = BeautifulSoup(topic, "html.parser")
    text_without_html = soup.get_text()
    print("catch the title")
    os_open()
    topic=text_without_html
    print("printing")
    result = chatgpt("Please summarize the topic of %s and answer me in one sentence, just answer what the topic is, for example: 'How to Plant A Tree'. Don't return 'The topic is', just return the topic"%topic)
    result = chatgpt("Write an essay of %s, with less than 300 words"%(result))
    os_close()
    driver.find_element("xpath", '//*[@id="contents"]').send_keys(result)
    driver.find_element("xpath",'//*[@id="dafen"]').click()
    sleep(3)
    point="/html/body/div[4]/div[3]/div[5]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div/div/span[1]"
    point=driver.find_element("xpath",point)
    print(point.text)
    return point.text




#account:账号
#password:密码
#number:作文号

write_pg(account,password,number)
