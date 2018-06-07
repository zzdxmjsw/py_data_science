import requests
import urllib.request
import json
import re
from lxml import etree
import pandas as pd


s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh - CN,zh;q = 0.8',
    'Cache-Control': 'max-age = 0',
    'Connection': 'keep-alive',
    'Host': 'piao.qunar.com',
    'Upgrade-Insecure-Requests': '1'}
s.headers = headers


def get_page(url):  # 获取链接中的网页内容

    try:
        r = s.get(url, timeout=5)  # url 为piao.qunar.com/
        page = r.content.decode('utf-8')
        return page
    except (urllib.request.URLError, Exception) as e:
        if hasattr(e, 'reason'):
            print('抓取失败，具体原因：', e.reason)
            r = s.get(url, timeout=5)
            page = r.content.decode('utf-8')
            return page


def get_list():
    place_name = input('请输入想搜索的区域、类型(如北京、热门景点等)：')
    url = 'http://piao.qunar.com/ticket/list.htm?keyword=' + \
        str(place_name) + '&region=&from=mpl_search_suggest&page={}'
    i = 1
    sightlist = []
    while i < 300:  # 300页
        page = get_page(url.format(i))
        selector = etree.HTML(page)
        print('正在爬取第' + str(i) + '页景点信息')
        i += 1
        informations = selector.xpath('//div[@class="result_list"]/div')
        for inf in informations:  # 获取必要信息
            sight_name = inf.xpath('./div/div/h3/a/text()')[0]  # 景点名
            sight_level = inf.xpath('.//span[@class="level"]/text()')  # 星级
            if len(sight_level):  # 有的景点没有星级标签
                sight_level = sight_level[0].replace('景区', '')  # 5A景区-> 5A
            else:
                sight_level = 0  # 否则无星
            sight_area = inf.xpath(
                './/span[@class="area"]/a/text()')[0]  # 行政区划地址
            sight_hot = inf.xpath(
                './/span[@class="product_star_level"]//span/text()')[0].replace('热度 ', '')  # 热度
            sight_add = inf.xpath(
                './/p[@class="address color999"]/span/text()')[0]  # 具体地址
            sight_add = re.sub(
                '地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$',
                '',
                str(sight_add))  # 地址改写
            sight_slogen = inf.xpath(
                './/div[@class="intro color999"]/text()')[0]  # 标语
            sight_price = inf.xpath(
                './/span[@class="sight_item_price"]/em/text()')  # 门票价格
            if len(sight_price):
                sight_price = sight_price[0]
            else:  # 没有价格就结束
                i = 0
                break
            sight_soldnum = inf.xpath(
                './/span[@class="hot_num"]/text()')[0]  # 月销量
            sight_url = inf.xpath('.//h3/a[@class="name"]/@href')[0]  # 链接
            sightlist.append([sight_name,
                              sight_level,
                              sight_area,
                              float(sight_price),
                              int(sight_soldnum),
                              float(sight_hot),
                              sight_add.replace('地址：', ''),
                              sight_slogen,
                              sight_url])
        # time.sleep(3)
    return sightlist, place  # 返回某市所有景点信息和该地地名


def list2excel(a_list, name):
    df = pd.DataFrame(
        a_list,
        columns=[
            '景点名称',
            '级别',
            '所在区域',
            '起步价',
            '销售量',
            '热度',
            '地址',
            '标语',
            '详情网址'])
    df.to_excel(name + '景点信息.xlsx')
    df.to_csv(name+'景点信息.csv')


def get_baidu_geo(sightlist):
    ak = 'h21bgTXT4S4aOql7yGjpIjsSqKVyQWtV'
    bjsonlist = []
    ejsonlist1 = []
    ejsonlist2 = []
    num = 1
    for site in sightlist:
        try:
            try:
                try:
                    address = site[6]  # 准确地址
                    url = 'http://api.map.baidu.com/geocoder/v2/?address=' + \
                        address + '&output=json&ak=' + ak
                    json_data = requests.get(url=url).json()
                    json_geo = json_data['result']['location']
                except KeyError:  # 退而求其次
                    address = site[0]  # 景点名称
                    url = 'http://api.map.baidu.com/geocoder/v2/?address=' + \
                        address + '&output=json&ak=' + ak
                    json_data = requests.get(url=url).json()
                    json_geo = json_data['result']['location']
            except KeyError:
                address = site[2]  # 所在地市
                url = 'http://api.map.baidu.com/geocoder/v2/?address=' + \
                    address + '&output=json&ak=' + ak
                json_data = requests.get(url=url).json()
                json_geo = json_data['result']['location']
        except KeyError:
            continue  # 直接跳过
        json_geo['count'] = site[4] / 100  # 销售量除以100
        bjsonlist.append(json_geo)  # 大列表中加入景点信息
        ejson1 = {site[0]: [json_geo['lng'], json_geo['lat']]}  # 控制地理信息
        ejsonlist1 = dict(ejsonlist1, **ejson1)
        ejson2 = {'name': site[0], 'value': site[4] / 100}  # 控制热力深浅
        ejsonlist2.append(ejson2)
        print('正在生成第' + str(num) + '个景点的经纬度')
        num += 1
    bjsonlist = json.dumps(bjsonlist)
    ejsonlist1 = json.dumps(ejsonlist1, ensure_ascii=False)
    ejsonlist2 = json.dumps(ejsonlist2, ensure_ascii=False)
    with open('./points.json', "w") as f:
        f.write(bjsonlist)
    with open('./geoCoordMap.json', "w") as f:
        f.write(ejsonlist1)
    with open('./data.json', "w") as f:
        f.write(ejsonlist2)


sight_list, place = get_list()
list2excel(sight_list, place)
get_baidu_geo(sight_list)
