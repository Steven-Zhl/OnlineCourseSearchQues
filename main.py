import Web


def main(searchContent):
    # print('请选择搜索源：')
    # print('1.精华吧')
    # choice = eval(input())
    # web = None
    #
    # if choice == 1:
    web = Web.Jinghuaba()
    web.html_searchPage = Web.getPageHtml(web.searchPageUrl(searchContent), decode=web.decode)  # 读取搜索页面内容
    web.parseSearchResultUrl()  # 获取了搜索结果的url
    # 读取每个搜索结果的内容
    if isinstance(web.url_searchResult, str):
        web.html_searchResult = Web.getPageHtml(web.url_searchResult, decode=web.decode)  # 读取搜索结果内容
    elif isinstance(web.url_searchResult, list):
        web.html_searchResult = list()
        for url_res in web.url_searchResult:
            web.html_searchResult.append(Web.getPageHtml(url_res, decode=web.decode))
    web.parseQuesUrl()  # 获取题目信息
    print(web.questionList)


if __name__ == '__main__':
    print('请输入搜题内容：')
    main(input())
