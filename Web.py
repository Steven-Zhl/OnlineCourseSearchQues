from bs4 import BeautifulSoup as BS
from urllib.parse import quote  # 将中文转换为url编码
from urllib.error import HTTPError  # Http错误类
from urllib.request import urlopen  # 读取网页HTML内容
from urllib.request import Request  # 发送请求
import re


def getPageHtml(url, decode='utf-8', requestClose=False):
    """
    请求网页Html内容
    :param decode: 网页编码方式，默认utf-8
    :param requestClose: 是否关闭每次请求以应对反爬虫
    :param url: 网页url
    :return: 网页内容
    """
    try:
        request = Request(url, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36 '
        })  # 添加浏览器信息，以应对部分反爬虫机制
        response = urlopen(request)
        content = response.read().decode(decode)
        if requestClose:
            response.close()  # 关闭连接(为了应对反爬虫)
        return content
    except HTTPError as e:
        print(e)
        return False


class Web:
    def __init__(self, url):
        self.url = url  # 主页url，最后不带/
        self.title = ''  # 网页标题
        self.decode = 'utf-8'  # 默认编码
        self.html_searchPage = ''  # 搜索页的html内容
        self.url_searchResult = None  # 搜索结果的url（可能为list）
        self.html_searchResult = None  # 搜索结果的html内容（可能为list）
        self.questionList = []  # 可能的题目列表

    def searchPageUrl(self, searchContent):
        """
        返回搜索页的url
        :param searchContent:搜索内容
        :return:
        """
        pass

    def searchResultUrl(self, searchPageHtmlContent):
        """
        返回搜索结果的Url
        :param searchPageHtmlContent:
        :return: 搜索搜索结果的Url，可能是str或list
        """
        pass

    def parseSearchResultUrl(self):
        """
        解析搜索页html内容，得到搜索结果的url
        :return:
        """
        pass

    def parseQuesUrl(self):
        """
        解析单个题目的html内容，生成题目
        :return:
        """


class Jinghuaba(Web):
    def __init__(self):
        super().__init__('https://www.jhq8.cn')
        self.title = '精华吧'
        self.decode = 'GB2312'

    def searchPageUrl(self, searchContent):
        return 'https://www.jhq8.cn/s/' + quote(searchContent) + '/'

    def parseSearchResultUrl(self):
        """
        通过BeautifulSoup解析网页内容，提取所需的信息
        :return: 所需的内容
        """
        html = BS(self.html_searchPage, 'html.parser')
        url_searchResult = html.find_all('div', {'class': 'lift_remen-list'})  # 找到所有匹配项

        if len(url_searchResult) == 1:  # 只有1个匹配项，直接等于str
            self.url_searchResult = self.url + url_searchResult[0].find('a')['href']
        else:
            self.url_searchResult = list()  # 有多个匹配项，则搜索结果为list
            for url in url_searchResult:
                self.url_searchResult.append(self.url + url.find('a')['href'])

    def parseQuesUrl(self):
        if isinstance(self.html_searchResult, str):
            html = BS(self.html_searchResult, 'html.parser')
            content = html.find('div', {'style': 'font-size: 15px;'}).contents  # 读取内容
            content = str.join('', [str(i) for i in content])  # 将其连接成字符串
            content = [i for i in re.split('[(<p>)(</p>)(\n)]', content) if i != '']  # 格式整理
            self.questionList.append(content)
        elif isinstance(self.html_searchResult, list):
            for htmlContent in self.html_searchResult:
                html = BS(htmlContent, 'html.parser')
                content = html.find('div', {'style': 'font-size: 15px;'}).contents  # 读取内容
                content = str.join('', [str(i) for i in content])  # 将其连接成字符串
                content = [i for i in re.split('[(<p>)(</p>)(\n)]', content) if i != '']  # 格式整理
                self.questionList.append(content)
