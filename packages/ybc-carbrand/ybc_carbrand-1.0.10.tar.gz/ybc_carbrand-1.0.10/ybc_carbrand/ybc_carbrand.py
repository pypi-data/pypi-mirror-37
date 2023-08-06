import json
import os

_PATH = os.path.abspath(__file__)
_DATA_PATH = os.path.split(_PATH)[0]+'/data/carbrands.json'


def brands():
    """
    功能：获取所有汽车品牌。

    参数：无

    返回：所有汽车品牌
    """
    f = open(_DATA_PATH, encoding='utf-8')
    fileJson = json.load(f)
    return fileJson


def main():
    print(brands())


if __name__ == '__main__':
    main()
