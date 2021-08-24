import json
import requests
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
}


def login(username, password):
    timestamp = str(int(time.time()))  # 获取今日时间，先转化为整形再转化为字符串
    url = 'https://api-service.chanmama.com/v1/access/token'
    data = {"appId": '10000', "timeStamp": timestamp, "username": username, "password": password}  # 登录

    response = requests.session().post(url, headers=headers, data=data).json()
    return response


def get_the_page(url, params, response):
    cookies={}
    cookies['LOGIN-TOKEN-FORSNS'] = response['data']['token']  # 获取cookies
    response = requests.get(url, headers=headers, cookies=cookies, params=params).text
    return response

# 不同的榜单有不同的数据需求，以不同的函数获取数据
def yesterday_sale_rank(text):
    data = []
    text = json.loads(text)  # 加载数据
    text = text['data']
    for text in text:
        # 将字典中的数据分别抠出来，这个message需要随着循坏不断更新地址，否则爬出来的数据都会指向最后一个数据的地址
        message = {}
        message['rank'] = text['rank']  # 排名
        message['name'] = text['title']  # 商品名
        message['price'] = text['coupon_price']  # 商品价格
        message['rate'] = '{:.2%}'.format(text['rate']/100)  # 佣金比例
        message['yesterday_sales'] = text['day_order_count']  # 昨日销量
        message['sales'] = text['amount']  # 销售额
        message['month_sales'] = text['order_count']  # 月销量
        message['conversion_rate'] = '{:.2%}'.format(text['month_conversion_rate']/100)  # 30天转化率
        message['platform'] = text['platform']  # 销售平台
        message['image'] = text['image']  # 图片链接
        data.append(message)

    return data


def yesterday_hot_rank(text):
    data = []
    text = json.loads(text)
    text = text['data']
    for text in text:
        message = {}
        message['rank'] = text['rank']  # 排名
        message['name'] = text['title']  # 商品名
        message['price'] = text['coupon_price']  # 价格
        message['rate'] = '{:.2%}'.format(text['rate']/100)  # 佣金比例
        message['author'] = text['author_number']  # 昨日带货达人数
        message['month_sales'] = text['order_count']  # 月销量
        message['conversion_rate'] = '{:.2%}'.format(text['month_conversion_rate']/100)  # 30天转化率
        message['platform'] = text['platform']  # 销售平台
        message['image'] = text['image']  # 图片链接
        data.append(message)
    return data


def live_rank(text):
    data = []
    text = json.loads(text)
    text = text['data']
    for text in text:
        message = {}
        message['rank'] = text['rank']  # 排名
        message['name'] = text['title']  # 商品名
        message['price'] = text['coupon_price']  # 价格
        message['rate'] = '{:.2%}'.format(text['rate']/100)  # 佣金比例
        message['hour_sales'] = text['sale_incr']  # 近两小时销量
        message['month_sales'] = text['sales']  # 月销量
        message['platform'] = text['platform']  # 销售平台
        message['image'] = text['image']  # 图片链接
        data.append(message)
    return data


def all_day_rank(text):
    return live_rank(text)


def speciality_today(text):
    data = []
    text = json.loads(text)
    text = text['data']
    for text in text:
        message = {}
        message['rank'] = text['rank']  # 排名
        message['name'] = text['shop_title']  # 抖音小店
        message['yesterday_sales'] = text['total_volume']  # 昨日销量
        message['yesterday_money'] = text['total_amount']  # 昨日销售额
        message['category'] = text['category']  # 类别
        message['video'] = text['video_count']  # 关联视频
        message['live'] = text['live_count']  # 关联直播
        message['rate'] = '{:.2%}'.format(text['average_conversion_rate'])  # 昨日转化率
        message['image'] = text['shop_icon']  # 图片链接
        data.append(message)
    return data


def rank(text):
    data = []
    text = json.loads(text)
    text = text['data']['list']
    for text in text:
        message = {}
        message['rank'] = text['rank']  # 排名
        message['name'] = text['brand_name']  # 品牌名
        message['yesterday_sales'] = text['day_order_count']  # 昨日销量
        message['amount'] = text['amount']  # 销售额
        message['product_count'] = text['product_count']  # 商品数
        message['video'] = text['aweme_count']  # 关联视频
        message['live'] = text['live_count']  # 关联直播
        message['label'] = text['label']  # 品牌类目
        message['image'] = text['brand_logo']  # 图片链接
        data.append(message)
    return data


def run(page, size):
    username = '13974973299'
    password = 'syoungwenao'
    response = login(username, password)
    url_list = ['yesterdaySaleRank', 'yesterdayHotRank', 'liveRank', 'allDayRank', 'specialtyToday', '']  # 从列表中分别取出数值爬取
    for i in range(len(url_list)):
        url = 'https://api-service.chanmama.com/v1/home/rank/' + str(url_list[i])
        # 接口数据（前4个是一样的）
        params = (
            ('category', '美妆护理'),
            ('page', page),
            ('size', size),
        )
        if url_list[i] == 'yesterdaySaleRank':
            print('开始爬取抖音销量榜————————————')
            text = get_the_page(url, params, response)
            message = yesterday_sale_rank(text)
            print(message)
            print('抖音销售榜爬取完毕————————————')
        elif url_list[i] == 'yesterdayHotRank':
            print('开始爬取抖音热推榜————————————')
            text = get_the_page(url, params, response)
            message = yesterday_hot_rank(text)
            print(message)
            print('抖音热推榜爬取完毕————————————')
        elif url_list[i] == 'liveRank':
            print('开始爬取实时销量榜————————————')
            text = get_the_page(url, params, response)
            message = live_rank(text)
            print(message)
            print('实时销量榜爬取完毕————————————')
        elif url_list[i] == 'allDayRank':
            print('开始爬取全天销量榜————————————')
            text = get_the_page(url, params, response)
            message = all_day_rank(text)
            print(message)
            print('全天销量榜爬取完毕————————————')
        elif url_list[i] == 'specialtyToday':
            print('开始爬取抖音小店榜————————————')
            params = (
                ('category', '美妆护理'),
                ('order_by', 'amount'),
                ('page', page),
                ('size', size)
            )
            text = get_the_page(url, params, response)
            message = speciality_today(text)
            print(message)
            print('抖音小店榜爬取完毕————————————')
        # 最后一个榜单的网址特殊，额外放出来
        if url_list[i] == '':
            print('开始爬取商品品牌榜榜————————————')
            url = 'https://api-service.chanmama.com/v1/brand/rank/'
            params = (
                ('day_type', 'day'),
                ('day', '2021-08-23'),
                ('category', '美妆护理'),
                ('sort', 'amount'),
                ('page', page),
                ('size', size)
            )
            text = get_the_page(url, params, response)
            message = rank(text)
            print(message)
            print('商品品牌榜爬取完毕————————————')


if __name__ == '__main__':
    # run(page, size)，page是从哪一页开始爬取数据，size是爬取数据的数量
    run(1, 300)
