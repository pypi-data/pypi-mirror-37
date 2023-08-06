from pypinyin import pinyin, lazy_pinyin


def pin(text=''):
    """
    功能：获取汉字对应的带注音的拼音。

    参数：一个或多个汉字

    返回：带注音的拼音
    """
    if text == '':
        return -1
    res_list = pinyin(text)
    res = []
    for s in res_list:
        res.append(s[0])
    return '-'.join(res)


def pin1(text=''):
    """
    功能：获取汉字对应的不带注音的拼音。

    参数：一个或多个汉字

    返回：不带注音的拼音
    """
    if text == '':
        return -1
    return '-'.join(lazy_pinyin(text))


def duoyin(text=''):
    """
    功能：得到多音字。

    参数：一个汉字

    返回：该汉字所有带注音的拼音
    """
    if text == '' or len(text) != 1:
        return -1
    res = pinyin(text, heteronym=True)
    res_list = []
    for s in res[0]:
        res_list.append(s)
    return '-'.join(res_list)


def main():
    print(pin('你好'))
    print(pin1('你好'))
    print(duoyin('车'))


if __name__ == '__main__':
    main()
