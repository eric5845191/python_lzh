# coding:utf-8
import re

file = open('d:\\baseroom_test.txt', 'r')
file_out = open('d:\\baseroom_kekka.txt', 'w')

lines = file.readlines()
spec = u"\n\r\t@%&#~!*_\"`\\-\\[\\]{}|:?;',=/\\.<>$>+￥^"
kuohao = u"""套票,仅限,提前,免费,入住,限时,限量,特惠,特价,促销,秒杀,包价,立减,售卖,套餐,专享,起订,连住,周末,今日,今夜,折,抢,价,含,预付,现付,券,起订,烟,宾,早,餐,门票
"""
kuohao = [i for i in kuohao.split(",")]
beside = u'''高级/豪华/商务/特惠/普通/数码/行政/经济/标准/促销'''
beside = [i for i in beside.split('/')]

for i in lines:
    i = i.decode('gbk')
    ori = i.replace('\n', '')
    i = i.replace(u'客房', u'间')
    i = i.replace(u'房', u'间')
    i = i.replace(u'标准间', u'标间')
    type = ''

    # 替换特殊符号
    for word in i:
        # print word
        if word in spec:
            # print word
            i = i.replace(word, "")
    # 处理括号
    i = i.encode('utf-8')
    match = re.findall('\（.*|\(.*', i)
    count = 0
    before = i.decode('utf-8')
    after = ''
    if len(match) > 0:
        after = match[0].decode('utf-8')
        before = i.decode('utf-8').replace(after, "")
        # print after
        for key in kuohao:
            if key in after:
                # print key
                # 这里编码有点问题
                try:
                    i = i.decode('utf-8')
                except:
                    pass
                i = i.replace(after, "")
                # i=before
                count = 1
                # print i
                type += '括号（特价信息等）'
        if count != 1:
            i = i.decode('utf-8')

    else:
        i = i.decode('utf-8')
    # print ori + '\t' + i
    # 展示before和after的结果
    # if len(after)>0:
        # print 'be:' + before + 'after:' + after
    # else:
        # print before

    # i=i.decode('utf-8')

    # 处理括号外规则
    # 包含高级/豪华/商务 等关键词

    before = i
    after = ''
    match2 = re.findall('\（.*|\(.*', i.encode('utf-8'))
    if match2:
        after = match[0].decode('utf-8')
    before = i.replace(after, "")

    count2 = 0
    # beside=[1]
    # print beside
    for besi in beside:
        if besi in before:
            # if 1:
            # print besi
            for snd in u'''单人,双人,大床,双床,标'''.split(','):
                if snd in before:
                    # if u'间' not in before:
                    # if not re.findall(r'单人.*间|双人.*间|大床.*间|双床.*间|标.*间',before.encode('utf-8')):
                                # before=before+u'间'
                    count2 = 1
                    i = re.sub(r'单人.*间|双人.*间|大床.*间|双床.*间|标.*间',
                               '', before.encode('utf-8'))
                    i = i.decode('utf-8')
                    if re.findall(r'单人.*间|双人.*间|大床.*间|双床.*间|标.*间', before.encode('utf-8')):
                        if '套' in re.findall(r'单人.*间|双人.*间|大床.*间|双床.*间|标.*间', before.encode('utf-8'))[0]:
                            # if u'套' in before:
                            i = i + u'套'
                            # print 'tao'
                        type += "大双床"

    if count2 > 0:
        if after:
            i = i + after
    # print ori
    # print ori + '\t' + i

    i = i.replace(u'间', '')

    line = ori + '\t' + i + '\t' + type.decode('utf-8') + '\n'
    # print line
    file_out.write(line.encode('mbcs'))
