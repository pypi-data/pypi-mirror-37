import json
import requests
import ybc_config

__PREFIX = ybc_config.config['prefix']
__PM_INFO_URL = __PREFIX + ybc_config.uri + '/pmInfo'

pm25_level = {
    '优': '一级',
    '良': '二级',
    '轻度污染': '三级',
    '中度污染': '四级',
    '重度污染': '五级',
    '严重污染': '六级'
}

pm25_affect = {
    '优': '空气质量令人满意，基本无空气污染',
    '良': '空气质量可接受，但某些污染物可能对极少异常敏感人群健康有较弱影响',
    '轻度污染': '易感人群症状有轻度加剧，健康人群出现刺激症状',
    '中度污染': '进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响',
    '重度污染': '心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普通出现症状',
    '严重污染': '健康人群运动耐受力降低，有明显强烈症状，提起出现某些疾病'
}

pm25_advise = {
    '优': '各类人群可正常活动',
    '良': '极少异常敏感人群减少户外活动',
    '轻度污染': '儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼',
    '中度污染': '儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼，一般人群适量减少户外运动',
    '重度污染': '儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群适量减少户外运动',
    '严重污染': '儿童、老年人和病人应停留在室内，避免体力消耗，一般人群应避免户外运动'
}


def pm25(city=''):
    if city == '':
        return -1
    url = __PM_INFO_URL
    data = {
        'city': city
    }

    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            if res['result']:
                res = r.json()['result'][0]
                pm = res['citynow']
                res_dict = {}
                # 获取监测点信息
                position = res['lastMoniData']
                res_dict['position'] = []
                count = 0
                sum = 0
                for val in position.values():
                    pos_list = {}
                    pos_list['posname'] = val['city']
                    pos_list['pm25'] = val['PM2.5Day']
                    pos_list['quality'] = val['quality']
                    res_dict['position'].append(pos_list)
                    if pos_list['pm25'] != "—":
                        count = count + 1
                        sum += int(pos_list['pm25'])

                # 获取城市pm2.5信息
                res_dict['city'] = city
                res_dict['pm25'] = str(sum // count)
                res_dict['quality'] = pm['quality']

                # 根据“空气质量”获取级别、影响、建议信息
                res_dict['level'] = pm25_level.get(res_dict['quality'])
                res_dict['affect'] = pm25_affect.get(res_dict['quality'])
                res_dict['advise'] = pm25_advise.get(res_dict['quality'])

                return res_dict

    raise ConnectionError('获取城市空气质量信息失败', r._content)


def main():
    print(pm25('北京'))


if __name__ == '__main__':
    main()
