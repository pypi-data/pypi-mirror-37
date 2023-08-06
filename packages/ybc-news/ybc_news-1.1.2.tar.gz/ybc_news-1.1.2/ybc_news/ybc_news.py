import json
import requests
import ybc_config


__PREFIX = ybc_config.config['prefix']
__NEWS_URL = __PREFIX + ybc_config.uri + '/news'


def channels():
    """
    功能：获取新闻分类。

    参数：无。

    返回：所有新闻分类。
    """
    return ['头条', '社会', '国内', '国际', '娱乐', '体育', '军事', '科技', '财经', '时尚']


def news(channel='科技'):
    """
    功能：获取指定分类下的新闻。

    参数：channel是分类名称，默认为科技

    返回：该分类下的新闻（标题、时间、图片地址），若分类不存在默认返回"头条"
    """
    content = 'news'
    url = __NEWS_URL
    data = {'op': content, 'channel': channel}
    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            res = res['result']
            if res['stat'] == '1' and res['data']:
                news_list = []
                for item in res['data']:
                    res_info = [item['title'], item['date'], item['thumbnail_pic_s']]
                    news_list.append(res_info)
                return news_list
            else:
                return -1
    raise ConnectionError('获取新闻失败', r._content)

def main():
    print(channels())
    print(news("体育"))


if __name__ == '__main__':
    main()
