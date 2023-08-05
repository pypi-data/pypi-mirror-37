# coding=utf-8
import webbrowser
import pinyin

urls = {
        'baidu':'http://www.baidu.com',
        'yuanfudao':'http://yuanfudao.com',
        'xiaoyuan':'http://www.yuanfudao.com/info/emojis',
        'sougou':'http://www.sogou.com',
        'sanliuling':'http://www.so.com',
        'shipin':'http://v.qq.com',
        'youxi':'http://www.4399.com',
        'yinyue':'http://music.163.com',
        'donghua':'http://child.iqiyi.com',
        'dianying':'http://www.iqiyi.com/dianying/',
        'biancheng':'https://python.yuanfudao.com/',
        'shuai':'https://www.yuanfudao.com/tutor-ybc-course-api/fshow/king1.jpg',
        'bilibili':'https://www.bilibili.com/',
        'duichenhuihua':'http://weavesilk.com/',
        'diantai':'http://www.qingting.fm/',
        'zhongguose':'http://zhongguose.com',
        'jike':'http://geektyper.com/',
        'tupiantexiao':'https://photomosh.com/',
        'wenzitexiao':'http://tholman.com/texter/',
        'yishusheji':'http://huaban.com/',
        'sumiaoshangse':'http://paintschainer.preferred.tech/index_zh.html',
        'shubiaogangqin':'http://touchpianist.com/',
    }

def open_browser(text):
    if not text:
        return -1

    res = pinyin.get(text, format = 'strip')

    url = "http://www.baidu.com"
    for key in urls.keys():
        if res in key or key in res:
            url = urls[key]
            break
    return webbrowser.open_new_tab(url)

def open_local_page(file_name):
    file_path = os.path.abspath(file_name)
    local_url = 'file://' + file_path
    webbrowser.open_new_tab(local_url)
