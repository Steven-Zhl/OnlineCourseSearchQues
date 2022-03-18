from bs4 import BeautifulSoup as BS
from urllib.parse import quote  # 将中文转换为url编码
from urllib.error import HTTPError  # Http错误类
from urllib.request import urlopen  # 读取网页HTML内容
from urllib.request import Request  # 发送请求
from re import sub, split  # 正则表达式


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
        try:
            content = response.read().decode(decode)
        except:
            content = response.read().decode('GB2312')
        if requestClose:
            response.close()  # 关闭连接(为了应对反爬虫)
        return content
    except HTTPError as e:
        print(e)
        return False


class MOOC:
    def __init__(self, path=None, mode='exam'):
        self.path = path
        self.quesElemName = [['div', 'class', 'm-choiceQuestion u-questionItem ' + mode + 'Mode first'],
                             ['div', 'class', 'm-choiceQuestion u-questionItem ' + mode + 'Mode'],
                             ['div', 'class', 'm-choiceQuestion u-questionItem ' + mode + 'Mode last']]  # 题目元素名称
        self.quesDesc = [['span', 'style',
                          'font-family: 宋体; line-height: 150%; font-size: 16px; color: rgb(102, 102, 102);'],
                         ['span', 'style', 'font-family: 宋体; font-size: 16px; text-align: justify; text-indent: 32px;'],
                         ['span', 'style', 'font-size: 16px; text-align: justify; text-indent: 32px; font-family: 宋体;'],
                         ['span', 'style', 'font-family:宋体;line-height:150%;font-size:14px;'],
                         ['span', 'style', 'font-family:宋体;line-height:150%;font-size:16px;'],
                         ['span', 'style', 'font-family:宋体;']]  # 问题描述元素名称
        self.quesList = []  # 问题列表
        self.ques_ansList = []  # 问题答案列表

    def _getQuesDesc(self, quesHtml):
        """
        获取题目描述
        :param quesHtml:
        :return: 题目描述
        """
        description = ''
        # 因为源网页中元素命名太不规范了，暂且只想到这种办法
        for i in range(len(self.quesDesc)):
            if len(quesHtml.find_all(self.quesDesc[i][0])) != 0 and description == '':
                description = ''.join([text.get_text() for text in quesHtml.find_all(self.quesDesc[i][0])][1:])
        description = description.encode('gbk', 'ignore').decode('gbk')  # 转换为gbk，使之能够兼容命令行，Mac请将gbk改成utf-8
        description = sub('[\n ]', '', description)  # 去除换行符和空格
        description = split('[，。？！]', description)[0]
        return description

    def getQuesList(self):
        """
        获取题目（描述）列表
        :return:
        """
        html = BS(open(self.path, 'r', encoding='utf-8').read(), 'html.parser')
        ques = list()  # 暂存各个题目的html内容
        # 第一题
        ques.append(html.find(self.quesElemName[0][0], {self.quesElemName[0][1]: self.quesElemName[0][2]}))
        # 中间题目
        ques.extend(html.find_all(self.quesElemName[1][0], {self.quesElemName[1][1]: self.quesElemName[1][2]}))
        # 最后一题
        ques.append(html.find(self.quesElemName[2][0], {self.quesElemName[2][1]: self.quesElemName[2][2]}))
        # 对每个题目进行处理
        ques = [item for item in ques if item is not None]
        if len(ques) != 0:
            for index in range(len(ques)):
                quesDesc = self._getQuesDesc(ques[index])
                self.quesList.append(quesDesc)
            return True  # 能获取到题目
        else:
            return False  # 无法获取到题目

    def showQuesList(self):
        for index in range(len(self.quesList)):
            print('第' + str(index + 1) + '题：' + self.quesList[index])

    def searchQues(self, searchKeyword=None, show=False):
        web = Jinghuaba()  # 选择搜题源
        if searchKeyword:  # 只搜1个
            searchResHtml = getPageHtml(web.searchPageUrl(searchKeyword), decode=web.decode)  # 读取搜索页面内容
            searchResUrl = web.parseSearchResultUrl(searchResHtml)  # 获取了搜索结果的url
            if searchResUrl != '':
                searchResContent = getPageHtml(searchResUrl, decode=web.decode)  # 读取搜索结果内容
            else:
                searchResContent = ''
            res = web.parseQuesUrl(searchResContent)
            if show:
                print(' '.join(res[0:-1]))
                print('\t', res[-1])
            return res

        else:  # 批量搜题
            ques_ans = [self.searchQues(searchKeyword=ques) for ques in self.quesList]
            if show:
                index = 1
                for item in ques_ans:
                    print(index, ' '.join(item[0:-1]))
                    print('\t', item[-1])
                    index += 1


class SearchPlatform:
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


class Jinghuaba:
    def __init__(self):
        self.url = 'https://www.jhq8.cn'
        self.title = '精华吧'
        self.decode = 'GB2312'
        self.searchContent = ''

    def searchPageUrl(self, searchContent):
        self.searchContent = searchContent
        return 'https://www.jhq8.cn/s/' + quote(searchContent) + '/'

    def parseSearchResultUrl(self, html_searchPage):
        """
        从搜索结果页中解析出匹配结果的url
        :return: 所需的内容
        """
        html = BS(html_searchPage, 'html.parser')
        url_searchResult = html.find_all('div', {'class': 'lift_remen-list'})  # 找到所有匹配项
        try:
            url_searchResult = self.url + url_searchResult[0].find('a')['href']  # 选最匹配的
        except:
            url_searchResult = ''
        return url_searchResult

    def parseQuesUrl(self, html_searchResult):
        """
        从题目详解页面中解析出题目及答案
        :param html_searchResult:
        :return:
        """
        if isinstance(html_searchResult, str) and html_searchResult != '':
            html = BS(html_searchResult, 'html.parser')
            content = html.find('div', {'style': 'font-size: 15px;'}).contents  # 读取内容
            content = str.join('', [str(i) for i in content])  # 将其连接成字符串
            content = [i.encode('gbk', 'ignore').decode('gbk') for i in split('[(<p>)(</p>)(\n)]', content) if
                       i != '']  # 格式整理
            ques_ans = content
        elif isinstance(html_searchResult, list):
            ques_ans = []
            for htmlContent in html_searchResult:
                html = BS(htmlContent, 'html.parser')
                content = html.find('div', {'style': 'font-size: 15px;'}).contents  # 读取内容
                content = str.join('', [str(i) for i in content])  # 将其连接成字符串
                content = [i.encode('gbk', 'ignore').decode('gbk') for i in split('[(<p>)(</p>)(\n)]', content) if
                           i != '']  # 格式整理
                ques_ans.append(content)
        else:
            ques_ans = [self.searchContent, "没有找到该题"]
        return ques_ans
