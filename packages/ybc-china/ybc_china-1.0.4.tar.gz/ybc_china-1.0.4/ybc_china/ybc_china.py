import urllib.request
import urllib.parse
import json
import os

data_path = os.path.abspath(__file__)
data_path = os.path.split(data_path)[0]+'/data/'

def all_cities():
    '''获取所有城市'''
    f = open(data_path + "cities.json", encoding='utf-8')
    fileJson = json.load(f)
    return fileJson

def provinces():
    '''获取所有的省份'''
    f = open(data_path + "provinces.json", encoding='utf-8')
    fileJson = json.load(f)
    return fileJson

def cities(proname=''):
    '''根据省份获取城市'''
    if proname == '' :
        return -1
    f = open(data_path + "provs_cities.json", encoding='utf-8')
    fileJson = json.load(f)
    cities_list = fileJson.get(proname)
    return cities_list


def main():
    print(all_cities())
    print(provinces())
    print(cities('湖南'))

if __name__ == '__main__':
    main()
