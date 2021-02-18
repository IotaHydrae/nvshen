#coding:utf-8
import os
import sys
import threading
import requests
import time
from bs4 import BeautifulSoup
from header2dict import header2dict

global ORIGIN_UR,ROOT_URL,PERSON_ID,PIC_BASE




headers = """Host: www.nvshens.org
Connection: keep-alive
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: records=%5B%7B%22id%22%3A%2216232%22%2C%22name%22%3A%22%u674E%u598D%u66E6%22%7D%5D; UM_distinctid=177ab1010f63db-0b00abb79b0a27-13e3563-384000-177ab1010f7c58; CNZZDATA1279553903=1298368565-1613482688-https%253A%252F%252Fwww.nvshens.org%252F%7C1613482688; 3501_2470_112.9.212.227=1; Hm_lvt_0f1f5a5e4d9fc6dc0f52ab6f2ec45893=1613482699; gallery_32261=1; 3502_2499_112.9.212.227=1; gallery_30218=1; 3502_2325_112.9.212.227=1; richviews_3502=v9BNVM0UVmiulJdHIx3tIQ0lE4dIVibGExL67k9s3wT%252B7QqABpwWVFB58p2Pm%252BMSBFchr6XUIEnXKCJBZCDL6AjIRF62f7Dj4cqs2dXUAROoyeqDBqXXbKspxcg8mObTbxjwEs45G36ztxvcNllrZPeRMArdNKzplcaCjg%252B2Q5SP5wjlfUEzh95kT6ROHXJ36MrjGvVMXRtoqHChiKFHkisheIHPh%252BdK1fThdZijxcU1Nuc61JSrYGmXEwsr3XmuAY%252FFNO84reyXC%252Flz4C%252BrhhShvDB6xPSO9vi7QrNQ0MXM8i2z9uS7gOY4u3K2%252BEEiMQ2axMal4UcXhrH0RQZ3%252FA%253D%253D; 3502_2538_112.9.212.227=1; Hm_lpvt_0f1f5a5e4d9fc6dc0f52ab6f2ec45893=1613482718; gallery_32327=1; 3501_2320_112.9.212.227=1; beitouviews_3501=QmmNZGf9GWBULu%252FIEFOuVaPHJ5hhVxoWlXJz4lU9eulCU4m0jtmcVIKmI0W9Ib5mE9cxZXMpGaLGXHyoJzGmjrHozrQf83UUYDB%252BUZTG%252FBL9Ng4pDmdOd%252F4oBc0j2U0bQ40G2C8tPYCcGtBVZddf6H5fQ1HFF%252Fcca4uXbeje758%252BXQH9QzzrIrIwKk909B30DaSyZm63caDrMbFxc9viA%252Fb5V%252BxTOP5kPaL1XD4H1l4Ub9%252BGBGj5OHqmzX%252FmFDDfAhd%252FhX8w2MEweaDdNkmAw5BsVUdr7ADuWeW6m1WW5esKeFe0WyIslxNtdrAnyhbdW1PsXC5Qr52xkB0qM8PJUw%253D%253D; 3501_2517_112.9.212.227=1"""
headers = header2dict(headers)

headers2={
'Accept':'image/webp,image/*,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'t1.onvshen.com:85',
"If-None-Match":"ce118ca4a39cd31:0",
"Referer":"https://www.nvshens.org/g/34932/",
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400',
}
# print(headers2)

"""
程序框架
1. ROOT页面中获取图集总数，并保存下来
2. 进入图集分页浏览页，把每一页的图集链接保存下来
3. 
"""
GALLERY_INFO_LIST = ''

class myThread(threading.Thread):
    def __init__(self, tid, tname, t_ucount):
        threading.Thread.__init__(self)
        self.tid = tid
        self.tname = tname
        self.t_ucount = t_ucount

    def run(self):
        print(f"线程{self.tid}", self.tname, "开始执行")
        craw(self.t_ucount, self.tname)
        print(f"线程{self.tid}", self.tname, "执行完毕")


def overview_locator(target_url):
    """
    doc：寻找页面中的相册总数按钮，如果相册书小于6，则不显示总数按钮，需要直接查看ul获取相册数
    web_data: data of web
    :return: url of overview and count of gallery
    """
    web_data = requests.get(target_url, headers=headers)
    web_data = web_data.content.decode('utf-8')
    # print(web_data)

    soup = BeautifulSoup(web_data, 'lxml')
    overview_btn=''
    try:
        overview_btn = soup.select('a[class="title"]')[0]
    except:
        pass

    print(type(overview_btn))
    if overview_btn != '':
        gallery__num = overview_btn.text[1:-1]
        overview_url_end = overview_btn['href']
        return overview_url_end, gallery__num
    else:
        gallery__num = 0
        gallery__url_list = []
        photo_ul = soup.select('ul[class="photo_ul"]')[0]
        for li in photo_ul.children:
            gallery__num += 1
            gallery__url_list.append(ROOT_URL + li.a['href'])
            # print(li.a['href'])
        return gallery__url_list, gallery__num

def overview_parser(overview_url, page_num):
    """
    doc:
    :param overview_url: target_url
    :return: the url list of all gallery
    """
    gallery_url_list = []

    # 根据传入的页面数访问对应总览页并采集重要数据
    for index in range(1, page_num + 1):
        my_overview_url = f'{overview_url}{index}.html'
        # print(index)
        web_data = requests.get(my_overview_url, headers=headers)

        # 获取到目标页面数据
        # print(web_data.content)
        soup = BeautifulSoup(web_data.content, 'lxml')
        photo_ul = soup.select('ul[class="photo_ul"]')[0]

        gallery_list = photo_ul.children
        for gallery in gallery_list:
            # print(gallery.a['href'])
            gallery_url_end = gallery.a['href']
            gallery_url_list.append(ROOT_URL + gallery_url_end)

    return gallery_url_list


def gallery_parser(target_url):
    """
    doc：
    :param target_url: 具体相册链接
    :return: 图片总数
    """
    print(target_url)
    web_data = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(web_data.content, 'lxml')

    try:
        album_info = soup.select('div[id="dinfo"] > span')[0]
        # print(album_info.text.split('张')[0])
        print('album_info',album_info)
        gallery_pieces = int(album_info.text.split('张')[0])

        return gallery_pieces
    except:
        return -1


def write_gallery_info_to_disk(gallery_url_list):
    """

    :param gallery_url_list:
    :return:
    """
    # 生成相册信息文件
    path_gallery_info_file = f'./{PERSON_ID}.info'
    if os.path.exists(path_gallery_info_file):
        with open(path_gallery_info_file, 'r') as f_info:
            file_lines = len(f_info.readlines())
            print(file_lines)
            print(len(gallery_url_list))
            if file_lines != len(gallery_url_list):
                os.remove(path_gallery_info_file)
            else:
                return path_gallery_info_file

    for gallery_url in gallery_url_list:
        photo_num = gallery_parser(gallery_url)  # 得到相册图片数
        if photo_num != -1:
            print(gallery_url)
            gid = gallery_url.split('/')[-2]
            print(gid, photo_num)
            with open(path_gallery_info_file, 'a') as f_info:
                f_info.write(f'{gid},{photo_num}\n')
        else:
            with open(path_gallery_info_file, 'a') as f_info:
                f_info.write(f'0,0\n')


    return path_gallery_info_file


def pic_to_disk(path_info_file):
    output_dir = f'./{PERSON_ID}'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # fd_info_file = open(path_info_file, 'r')
    # GALLERY_INFO_LIST = fd_info_file.readlines()
    # print(GALLERY_INFO_LIST)

def craw(t_ucont, tname):
    img_data_list = []
    current_html = 1
    downloader_session = requests.session()
    downloader_session.headers = headers2

    fd_info_file = open(f'./{PERSON_ID}.info', 'r')
    info_list = fd_info_file.readlines()

    my_info = info_list[t_ucont]
    tmp = my_info.split(',')
    my_gid = tmp[0]
    my_pnum = tmp[1]
    if my_gid == '0':
        return

    output_dir = f'./{PERSON_ID}/{my_gid}'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print("当前网页: ", f'https://www.nvshens.org/g/{my_gid}/{current_html}.html')
    downloader_session.get(f'https://www.nvshens.org/g/{my_gid}/{current_html}.html')
    current_pic = 0

    for pic_index in range(int(my_pnum)):
        if pic_index == 0:
            pass
        elif int(pic_index) < 10:
            pic_index = f'00{pic_index}'
        else:
            pic_index = f'0{pic_index}'
        img_url = f'{PIC_BASE}/{my_gid}/s/{pic_index}.jpg'
        local_pic_path = f'{output_dir}/{pic_index}.jpg'
        if not os.path.exists(local_pic_path):
            print(f'[ Downloading ]线程{tname}--正在下载{my_gid}--{pic_index}张照片 [ Url ] {img_url}')
            res = downloader_session.get(img_url, allow_redirects=False)
            current_pic += 1

            if res.status_code == 200:
                print(f'[ OK ]线程{tname}--已下载{my_gid}--{pic_index} [ Url ] {img_url}')
                img_data = res.content

                with open(f'{output_dir}/{pic_index}.jpg', 'wb') as pic:

                    pic.write(img_data)
                    pic.close()
                img_data_list.append(img_data)
            else:
                print(res.status_code, "[ Error ]无法访问到: ", img_url)

            if current_pic == 3:
                current_html += 1
                print("[ Current ]当前网页: ", f'https://www.nvshens.org/g/{my_gid}/{current_html}.html')
                downloader_session.get(f'https://www.nvshens.org/g/{my_gid}/{current_html}.html', headers=headers2)
                current_pic = 0

    # count = 0
    # try:
    #     print(f"---------------------线程{tname}正在写入到文件中--------------------")
    #     for img_data in img_data_list:
    #         with open(f'{output_dir}/{count}.jpg', 'wb') as pic:
    #
    #             pic.write(img_data)
    #             pic.close()
    #
    #         count += 1
    #     print(f"---------------------线程{tname}写入文件完成！----------------------")
    # except Exception as e:
    #     print(e)

def thread_start(c1, c2, c3, c4):
    info_file = open(f"./{PERSON_ID}.info")
    file_content = info_file.readlines()
    _len = len(file_content)
    print("条目数:",_len)

    threads = []
    thread1 = myThread(1, "T1", c1)
    thread2 = myThread(2, "T2", c2)
    thread3 = myThread(3, "T3", c3)
    thread4 = myThread(4, "T4", c4)


    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)

    if _len < 4:
        for i in range(_len):
            ret = threads.pop()
            print(ret)

    for td in threads:
        td.join()

def threads_controller(gallery_count):
    print("相册总数: ",gallery_count)
    c1=0
    c2=1
    c3=2
    c4=3

    while True:
        thread_start(c1, c2, c3, c4)
        c1 += 4
        c2 += 4
        c3 += 4
        c4 += 4

        if c4 >= gallery_count+4:
            break


def main():

    target_rul = ORIGIN_URL
    # get the overview url and count of gallery
    result_overview_locator = overview_locator(target_rul)
    gallery_count = 0

    # 处理上一步得到的结果
    # 情况1 相册数大于6，需要进一步获取其他相册链接
    if type(result_overview_locator[0]) != type([]):
        # link two parts of url
        overview_url = ROOT_URL + result_overview_locator[0]
        print(overview_url)

        # calc page num
        mid_val = int(result_overview_locator[1]) / 30
        page_num = int(mid_val) + 1

        gallery_url_list = overview_parser(overview_url, page_num)
        gallery_count = len(gallery_url_list)

        path_info_file = write_gallery_info_to_disk(gallery_url_list)
        print(path_info_file)
        pic_to_disk(path_info_file)

    else:   # 情况2 相册数小于六，在页面中直接获取到了所有相册链接
        gallery_url_list = result_overview_locator[0]
        gallery_count = len(gallery_url_list)
        path_info_file = write_gallery_info_to_disk(gallery_url_list)
        print(path_info_file)
        pic_to_disk(path_info_file)

    # 启动线程控制器
    threads_controller(gallery_count)

def help():
    print(
        """
        Normally, The outermost URL is you must input.\n
        Any value of other may cause program run error.\n
        Also you can input the name of output dir, its not a necessary value,\n
        if you dont input it, the name of output dir will be set to girl id.
        """
    )
    pass

def raise_usege():
    if len(sys.argv) < 2:
        print("Usage: python main.py <URL> [name of output dir]")
        print('Please try "python main.py help" to get more info')
        exit(-1)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'help':
            help()
            exit()

def debug():
    URL = 'https://www.nvshens.org/girl/26089/'
    res = overview_locator(URL)
    print(res)

if __name__ == '__main__':
    now = time.time()

    raise_usege()
    # ORIGIN_URL = 'https://www.nvshens.org/girl/27912/'
    ORIGIN_URL = sys.argv[1]
    ROOT_URL = "https://www.nvshens.org"
    PERSON_ID = ORIGIN_URL.split('/')[-2]
    PIC_BASE = f"https://t1.onvshen.com:85/gallery/{PERSON_ID}"

    if main() == -1:
        print("program run error")

    if len(sys.argv) == 3:
        if not os.path.exists(sys.argv[2]):
            os.rename(f"./{PERSON_ID}", sys.argv[2])
        else:
            os.rename(f"./{PERSON_ID}", f"./{sys.argv[2]}{now}")
