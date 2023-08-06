import json
import os

data_path = os.path.abspath(__file__)
data_path = os.path.split(data_path)[0]+'/data/'

def all_cities():
    """
    获取所有的城市
    :return: 按照 json 组织的所有城市列表
    """
    f = open(data_path + "cities.json", encoding='utf-8')
    fileJson = json.load(f)
    return fileJson

def provinces():
    """
    获取所有的省份
    :return: 按照 json 组织的所有省份列表
    """
    f = open(data_path + "provinces.json", encoding='utf-8')
    fileJson = json.load(f)
    return fileJson

def cities(proName=''):
    """
    根据省份获取城市
    :param proName: 省份名称
    :return:
        success: 按照 json 组织的指定省份城市列表
        failed: -1，包含省份名为空，以及没有找到对应省份的情况
    """
    if proName == '':
        return -1
    f = open(data_path + "provs_cities.json", encoding='utf-8')
    fileJson = json.load(f)
    cities_list = fileJson.get(proName)

    if cities_list == None:
        return -1
    else:
        return cities_list


def main():
    print(all_cities())
    print(provinces())
    print(cities('湖南'))
    print(cities(''))
    print(cities('你好'))


if __name__ == '__main__':
    main()
