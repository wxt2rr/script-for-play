# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import os


def detail(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}  # 添加request headers,伪装成浏览器登录，若不添加则会被浏览器认出来是爬虫，而有的浏览器会限制爬虫，比如下厨房。

    res = requests.get(url, headers=headers)  # 获取数据
    soup = BeautifulSoup(res.text, 'html.parser')  # 解析数据
    print('html content parser success')
    inf = soup.find('div', class_="steps")  # 找到步骤块
    stepsList = inf.ol.find_all('li')  # 所有的步骤
    index: int = 1
    content: str = ''
    for step in stepsList:
        method = step.find('p').text  # 做法
        imgUrl = step.find('img')['src']  # 详情图

        try:
            content = content + str(index) + '.' + method + '\n'
        except:
            pass

        pullImg(imgUrl, path + '/img', str(index) + '.jpg')
        index += 1
    print('img pull over')
    splicingText(content.encode(), path, 'content.txt')
    print('content write over')
    print('done!')


def pullImg(url, path, name):
    response = requests.get(url)
    writeFileToOs(path, name, response.content)


def splicingText(text, path, name):
    writeFileToOs(path, name, text)


def writeFileToOs(path, name, content):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + '/' + name, 'wb') as file_obj:
        file_obj.write(content)
        file_obj.close()


if __name__ == '__main__':
    url = input('input url:')
    path = input("input path:")
    detail(url, path)
