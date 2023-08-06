# import json
import requests
import ybc_config


__PREFIX = ybc_config.config['prefix']
__WEATHER_URL = __PREFIX + ybc_config.uri + '/weather'


def _get_data(cityName=''):

    data = {}
    data['cityName'] = cityName
    url = __WEATHER_URL

    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            return res
    raise ConnectionError('获取天气结果失败', r.content)


def today(cityname=''):
    """
    查询指定城市名称的 今日天气
    :param cityname: 城市名称
    :return:
        success: list['上海', '2017年12月22日', '星期五', '7℃~14℃', '东南风微风', '较冷', '建议着厚外套加毛衣等服装。年老体弱者宜着大衣、呢外套加羊毛衫。']
        failed: -1，包含名字为空或者没有找到对应的城市
    """
    if cityname == '':
        return -1

    res = _get_data(cityname)
    if res['result'] is None:
        return -1

    res_data = []
    res_today = res['result']['today']
    res_data.append(res_today['city'])
    res_data.append(res_today['date_y'])
    res_data.append(res_today['week'])
    res_data.append(res_today['temperature'])
    res_data.append(res_today['wind'])
    res_data.append(res_today['dressing_index'])
    res_data.append(res_today['dressing_advice'])
    return res_data


def week(cityname=''):
    """
    查询指定城市的 这周天气
    :param cityname: 城市名称
    :return:
        success: list[]，元素为将来七天的天气信息
        failed: -1，包含名字为空或者没有找到对应的城市
    """
    if cityname == '':
        return -1
    res = _get_data(cityname)
    if res['result'] is None:
        return -1

    res_data = []
    res_today = res['result']['today']
    res_future = res['result']['future']
    for k,v in res_future.items():
        res_data.append([res_today['city'],v['date'],v['week'],v['temperature'],v['weather'],v['wind']])
    return res_data

def main():
    print(today('北京'))
    print(today(''))
    print(today('XXX'))
    print(week('北京'))

if __name__ == '__main__':
    main()
