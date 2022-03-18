import Process


def menu():
    print('网课搜题小工具(/≧▽≦)/   by Steven\n')
    print('该项目已开源，开源地址如下：')
    print('Github：https://github.com/Steven-Zhl/OnlineCourseSearchQues')
    print('Gitee：https://gitee.com/steven-zhl/online-course-search-ques')
    print('详细使用说明也可以在该链接查看')
    print('由于技术不强，整页搜题时间较长（通常半分钟，具体取决于网络情况），请耐心等待\(￣︶￣*\))')
    print('总之，祝你使用愉快  :-)\n')
    print('请选择搜题模式')
    print('1. 搜索单个题目')
    print('2. 整页搜题')
    choice = input('请选择：')
    if choice == '1':
        quesDesc = input('请输入或粘贴题目(*/ω＼*)：')
        Process.MOOC.searchQues(self=Process.MOOC(), searchKeyword=quesDesc, show=True)  # 搜并且展示
    elif choice == '2':
        pagePath = input('请输入或粘贴页面文件的路径(*/ω＼*)：')
        print('请选择页面类型（这个很重要，如果选择错误会导致获取不到题目）：')
        print('1. 考试页面：考试页面为考试过程中通过浏览器保存的页面 :D')
        print('2. 分析页面：分析页面为考完后回顾题目的页面 :D')
        mode = input('请选择：')
        if mode == '1':
            mooc = Process.MOOC(path=pagePath, mode='exam')
        elif mode == '2':
            mooc = Process.MOOC(path=pagePath, mode='analysis')
        else:
            print('输入错误，请稍后再试（＞人＜；）')
            input('按任意键退出...')
            return
        print('正在搜索中，请稍候O(∩_∩)O...')
        state = mooc.getQuesList()  # 能否获取到题目列表
        if state:
            mooc.searchQues(show=True)
        else:
            print('获取题目列表失败，看来不适合这门课程呢（＞人＜；）')
            input('按任意键退出...')
            return
    else:
        print('您的输入有误，请稍后再试（＞人＜；）')
        input('按任意键退出...')
        return
    input('搜索完成,按任意键退出(～￣▽￣)～')


if __name__ == '__main__':
    menu()
