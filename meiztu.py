import os
import requests
from bs4 import BeautifulSoup


class mztu():
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}  ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

    def myRequest(self, url):
        content = requests.get(url, headers=self.headers)
        return content

    def mkDir(self, title):
        path = str(title).strip()
        if path.find(':') != -1:
            print("11111111111111111111111")
            path = path.replace(':', '-')
        elif path.find('?') != -1:
            print("2222222222222222222")
            path = path.replace('?', '-')
        elif path.find('*') != -1:
            print("2222222222222222222")
            # path = path.replace('*', '-')
        else:
            print(path)
        if not os.path.exists(os.path.join("D:\mzitu", path)):
            os.makedirs(os.path.join("D:\mzitu", path))
            os.chdir("D:\mzitu\\" + path)
            return True
        else:
            print(path + "文件夹已经存在")
            return False

    def save(self, image_url):
        name = image_url[-9:-4]
        headers = {"Referer": self.href,
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
        img = requests.get(image_url, headers=headers)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def all_url(self, url):
        start_html = self.myRequest(url)
        # print(start_html.text)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        a_list = Soup.find('div', class_='all').find_all('a')

        for a in a_list:
            title = a.get_text()
            print(title)
            next = self.mkDir(title)
            if (next):
                href = a['href']
                self.href = href
                page_html = self.myRequest(href)
                page_soup = BeautifulSoup(page_html.text, 'lxml')
                page_span = page_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
                # print(page_span)
                for page_num in range(1, int(page_span) + 1):
                    href_image = href + '/' + str(page_num)
                    # print(href_image)
                    image_page = self.myRequest(href_image)
                    image_soup = BeautifulSoup(image_page.text, 'lxml')
                    image_url = image_soup.find('div', class_='main-image').find('img')['src']
                    self.save(image_url)


mzitu = None
while (True):
    if mzitu == None:
        mzitu = mztu()
        mzitu.all_url('http://www.mzitu.com/all/')
