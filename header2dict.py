def header2dict(header):
    items = header.split('\n')
    dict_ = {}
    index = 0
    new_lst = []

    for item in items:
        str = ''
        temp = item.split(':')
        new_lst = temp[1:]
        k = temp[0].strip()
        for i in new_lst:
            str += i

        dict_[k]=str.strip()

    return dict_

if __name__ == '__main__':
    header = '''Host: kexues.icu
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Accept-Encoding: gzip, deflate, br
    X-Requested-With: XMLHttpRequest
    Origin: https://kexue.ga
    Connection: keep-alive
    Referer: https://kexue.ga/user
    Cookie: _ga=GA1.2.711495693.1580472729; _gid=GA1.2.615565355.1582277312; uid=1340; email=1657802074%40qq.com; key=7d5c895664ee210ade1837f973b78dd246832a8d6de0b; ip=cc6600ab77608f3c585450cab8d0fd5f; expire_in=1582882112; _gat=1
    Content-Length: 0
    TE: Trailers'''
    text = header2dict(header)
    print(text)