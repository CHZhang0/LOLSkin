import requests
import os

# 获取英雄ID
def get_id():
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    response = requests.get(url=url, headers=headers).json()
    heros = response['hero']
    # 英雄列表
    heroIds = []
    for hero in heros:
        heroId = hero['heroId']
        heroIds.append(heroId)
    return heroIds


# 获取皮肤
def get_skin(heroIds):
    for heroId in heroIds:
        url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(heroId)
        response = requests.get(url=url, headers=headers).json()
        skins = response['skins']

        # 第二种方法。可爬到炫彩
        for skin in skins:
            # 皮肤url
            img_urls = skin['mainImg']
            # 皮肤名称
            img_name = skin['name']
            # 文件夹名称
            hero_name = skin['heroName']

            # 判断有无炫彩
            if img_urls:
                save(hero_name, img_name, img_urls)
            else:
                img_urls = skin['chromaImg']
                save(hero_name, img_name, img_urls)

# 保存数据
def save(hero_name, img_name, img_urls):
    path = 'LOLSkins/'
    if not os.path.exists(path + hero_name):
        os.mkdir(path + hero_name)

    img_content = requests.get(url=img_urls, headers=headers).content
    # 用于替换图片名称中出现的'/'字符
    img_name = img_name.replace('/', ' ')
    path = 'LOLSkins/' + hero_name + '/' + img_name + '.jpg'
    with open(path, 'wb') as fp:
        fp.write(img_content)
        print(img_name + '下载完成')


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        # 防盗链
        'Referer': 'https://lol.qq.com/'
    }

    if not os.path.exists('LOLSkins'):
        os.mkdir('LOLSkins')

    heroIds = get_id()
    get_skin(heroIds)