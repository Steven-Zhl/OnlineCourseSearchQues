import Process


def menu():
    print('网课搜题小工具   by Steven')
    print('1. 搜索单个题目')
    print('2. 整页搜题')
    choice = input('请选择：')
    if choice == '1':
        quesDesc = input('请输入或粘贴题目：')
        Process.MOOC.searchQues(self=Process.MOOC(), searchKeyword=quesDesc, show=True)  # 搜并且展示
    elif choice == '2':
        print('请输入页面文件的路径：')
        pagePath = input()
        print('请选择页面类型：')
        print('1. 考试页面：考试页面为考试过程中通过浏览器保存的页面')
        print('2. 分析页面：分析页面为考完后回顾题目的页面')
        mode = input('请选择：')
        if mode == '1':
            mooc = Process.MOOC(path=pagePath, mode='exam')
        elif mode == '2':
            mooc = Process.MOOC(path=pagePath, mode='analysis')
        else:
            print('输入错误，请稍后再试')
            return
        print('正在搜索中，请稍候...')
        mooc.getQuesList()
        mooc.searchQues(show=True)
    else:
        print('您的输入有误')


if __name__ == '__main__':
    menu()
