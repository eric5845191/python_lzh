# coding:utf-8
# 0620update plus https://www.douban.com/group/zufan/discussion?start=0
# 1009 update substitute urllib2 to requests
# 1011 update substitute xlrc to openpyxl, 修改long的判断逻辑，用到padans的value_counts()
# 1014 update 添加多线程


import requests
import re
from bs4 import BeautifulSoup
import openpyxl
# import time
import pandas
from multiprocessing import Pool
import random


# file=open('d:/rent.txt','w')
# file = open('/Users/ryu/Documents/rent.txt', 'w')

num = 0
find = 0


def enco(str):
    return str.decode('utf-8').encode('utf-8')


key = ['转租', '一室', '公寓', '女']
word = []
for i in key:
    word.append(enco(i))

# 读取黑名单
blacklist = ['豆花', '麦芽糖', 'Icoya抹茶控', 'liaozhi104', '寓青春公寓', '★静★', '笼中鸟', '杨先生', '我爱未婚夫', '橙子男生聚会', '寓青春公寓小颖', '池夏主题自拍馆', '熊takuda', 'cxw781205', '快乐城邦', 'chennan720', '虹口足球场出租', '李姐', '完美N+1', '复式公寓', '实体≌和谐公寓', '一房东一室户', '爱吃猪的大熊猫', 'cxw513', '蘑菇公寓普陀', '风兮一潇潇', '木马人', '自如客房屋管家', '别开枪是我！', '豆芽菜', '自如管家-赵亮',
             '打翻你的屁屁', '闵行租房', 'LONELY', '超超', '噢妙', '上海自如管家', '白菜', '我是管家', '管家 吴俊林', '*maomi*', '雨泽?vampire fo', 'dada', '暖暖', '小星星', 'LILI', '小白兔', '漂泊伪艺文', '小蚂蚁', '小白菜', 'heihei', 'komi', '苏苏苏苏', '布丁', 'Richard有话说', '雷', '全力以赴', '会哭的猫', '话梅', 'tutulalala', '青年汇', '长拾', '岛是海哭碎的心', 'ivan王', '123木头人', '百合', 'Happy^~^', 'dada']
# blacklist=[enco(i) for i in black]

read = ['53736314', '53820075', '49679682', '54247257', '54133946', '54215540', '54247223', '54191059', '54155135', '53468910', '54121784', '54247194', '54065217', '53851461', '54239202', '48811355', '54247146', '53930413', '52468414', '53974747', '54064228', '53807316', '54231070', '54150312', '54060005', '52680828', '54246841', '54190935', '54239254', '53743202', '52974037', '54240867', '54202323', '54155647', '52302094', '53381640', '54205844', '54234893', '54021263', '54080703', '54035026', '54246173', '54246143', '54193460', '54231279', '51086709', '54140601', '54165379', '54132107', '54150713', '54200143', '54191952', '52706891', '53574456', '54196287', '52585777', '45102377', '53743654', '48756635', '53818172', '53730350', '54249891', '50631143', '53843132', '53851775', '54253194', '54189257', '54239111', '54210622', '54237456', '54252807', '53623517', '54214766', '53480687', '54241504', '54177788', '53767039', '54253025', '54152801', '53734047', '53886450', '51381983', '53806306', '54186884', '51136045', '53555879', '54182485', '53945712', '54233313', '54252625', '54097596', '49551069', '54038869', '54210234', '54252512', '50669066', '54214358', '54238854', '53327055', '54182655', '54247328', '54252147', '54022554', '54242187', '54250640', '53806168', '52861034', '54134555', '52575766', '52645928', '54251162', '53740492', '44532928', '53701220', '54021671', '53899454', '54216099', '54248918', '54204426', '52993811', '54199580', '54254301', '54214023', '53704488', '54254288', '53529585', '53769095', '53874973', '54150416', '49913503', '53990650', '54253627', '54245580', '54253633', '54233833', '53805059', '53613035', '54061022', '53685285', '53713077', '53987913',
        '54253595', '52789688', '54212125', '44666006', '54104235', '54230976', '53921911', '54210529', '54179126', '54066088', '54244314', '54172882', '54045868', '54254913', '54183624', '52734461', '53537499', '54349507', '54232064', '54028840', '51413354', '54344452', '53601279', '54362398', '54347314', '54374781', '54217136', '54320295', '51485411', '54348569', '53693203', '53942919', '53293294', '49975988', '54198595', '54331036', '54142679', '54377238', '54358385', '54353133', '54264136', '53828889', '53774967', '54132798', '54312625', '54356707', '54094116', '54291752', '40646666', '53753553', '53214428', '54361668', '54109147', '54354950', '54093413', '54102002', '54372384', '53949719', '54004090', '41209073', '54340357', '54305519', '54317845', '52886352', '54376063', '53943453', '54366296', '54375945', '54342053', '54367574', '53161510', '53646395', '54367058', '54361349', '54147651', '54389249', '54389232', '54387899', '54389124', '49892688', '54383443', '54389037', '52848523', '54138545', '54141496', '54381972', '54157839', '54339281', '54356311', '54385455', '54382427', '54293412', '54312444', '54349445', '54348953', '54305305', '54051507', '54348679', '51030260', '54368546', '50540370', '54270487', '53775268', '54350735', '54010668', '54078971', '54384889', '54353152', '54348461', '54062165', '33892508', '54385970', '54291465', '52872880', '53396867', '54213514', '53820129', '53681872', '53946548', '54016294', '54300485', '54191586', '53828526', '54384493', '54382695', '53256311', '54332149', '52707624', '54389654', '54294229', '53828939', '54389475', '54281725', '54303533', '54389402', '54389399', '54385957', '53976761', '54027367', '54273379', '54236975']


book = openpyxl.load_workbook("/Users/ryu/Documents/rent.xlsx")
sh = book.get_sheet_by_name(book.get_sheet_names()[0])
for i in sh.rows:
    if i[2].value != 'id':
        read.append(str(i[2].value))

    # 如果被标记为黑名单
    if i[4].value == 'b':
        # print str(sh.cell_value(r,2)) +'nn'+ str(r+1) z
        # print sh.cell_value(r,1)
        print i[1].value, 'is black'
        blacklist.append(i[1].value.encode('utf-8'))


named = ''

groups = {'上海租房': 'https://www.douban.com/group/shanghaizufang/discussion?start=',
          '上海租房@长宁租房/徐汇/静安租房': 'https://www.douban.com/group/zufan/discussion?start=',
          '上海短租日租小组 ': 'https://www.douban.com/group/chuzu/discussion?start=',
          '上海短租': 'https://www.douban.com/group/275832/discussion?start=',
          '上海租房@长宁淞虹路、北新泾': 'https://www.douban.com/group/CNZF/discussion?start='
          }

wb = openpyxl.load_workbook("/Users/ryu/Documents/rent.xlsx")
sheetname = wb.get_sheet_names()[0]
ws = wb[sheetname]


user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

]


def crwalmain(url):
    eachurl = []
    groupnamethis = urldict[url]
    agent = random.choice(user_agents)
    headers = {
        'User-Agent': agent,
        'Host': 'www.douban.com',
        'Referer': url,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",

    }
    response = requests.get(url, headers=headers)
    html = response.text
    # html_en = enco(html)
    # print html_en
    soup = BeautifulSoup(html, 'lxml')
    # print html
    namelist = soup.findAll(
        'a', attrs={'href': re.compile("https://www.douban.com/people/\w+?/")})
    # namelist = soup.findAll('a', attrs={'href':re.compile("https://www.douban.com/group/people/\w+?/")})
    print 'totally %s users in this page' % len(namelist)
    thisnamelist = [x.string.encode('utf-8') for x in namelist]
    ps1 = pandas.Series(thisnamelist)
    counts1 = ps1.value_counts()

    for i in namelist:
        name = i.string.encode('utf-8')
        # name=i.string

        named.append(name)
        par = i.parent.parent
        title = par.find('a')['title'].encode('utf-8')
        urls = par.find('a')['href'].encode('utf-8')
        id = re.findall('https://www.douban.com/group/topic/(\d+)', urls)
        # print title+'\t'+name

        # black list
        # try:
        #     # id_num = re.findall(name.strip('?*'), html)
        #     id_num = counts1[name]
        # except:
        #     pass
        # id_num2 = re.findall(name.strip('?*'), named)
        id_num = counts1[name]
        ps = pandas.Series(named)
        counts = ps.value_counts()
        if name in named:
            id_num2 = counts[name]
        else:
            id_num2 = 0

        long = id_num + id_num2

        if long > 2:
            print name, 'appears %s times' % long
            print name, 'len1= %s , len2= %s' % (id_num, id_num2)
            if not name in blacklist:
                blacklist.append(name)

        # print name.decode('utf-8')
        # print name + 'allname:'
        if name in blacklist:
            # pass
            print name + 'in blakclist'
        else:
            # print type(id[0].strip())
            # print chardet.detect(id[0].strip())
            # print str(id[0].strip())
            if str(id[0].strip()) in read:
                print 'read\t' + title + '\t' + name
            else:
                # file.write(title + '\t' + name + '\t' +
                #            id[0] + '\t' + groupname.decode('utf-8').encode('utf-8') + '\t')
                # print title + '\t' + name + '\t' + id[0] + '\t' + groupname.decode('utf-8').encode('utf-8') + '\t'
                # # key word
                # for i in word:
                #     if i in title:
                #         file.write('\t' + i + ' ')

                # file.write('\n')

                # pattern = re.compile(ur'[^\u4e00-\u9fa5_a-zA-Z0-9,，/+]')
                pattern = re.compile(ur'[^\u4e00-\u9fa5_a-zA-Z0-9, ，\s【】/ +&)（）(！／]|中介')

                relist = pattern.findall(title.decode('utf-8'))
                reset = set(relist)
                # length = len(reset)
                length2 = len(relist)
                merge = ''.join(reset)
                # print u'提取出来的特殊符号：\n' + merge

                pattern = re.compile(ur'中介|微信|看房|业主|大三房|首次出租|得房率|拎包入住|紧邻地铁|好房1间|两房|黄金楼层|客户|直租|温馨|首选')
                a = pattern.findall(title.decode('utf-8'))

                if len(a) > 0:
                    print 'zhongjie a@@@@@@@@@@\n\n' + title
                    blacklist.append(name)
                else:
                    eachrow = [title, name, id[0], groupnamethis,
                               length2, merge]
                    # ws.append(eachrow)
                    print 'writing', title, '\n'
                    eachurl.append(eachrow)

    print 'this page is %s of %s \n' % (url, groupnamethis) + '*' * 66

    return(eachurl)
    # wbç.save("/Users/ryu/Documents/rent.xlsx")

    # time.sleep(3)


allurl = []
urldict = {}
for groupname in groups:
    num = 0
    named = []

    while num < 250:
        # while num<25:

        # url='https://www.douban.com/group/shanghaizufang/discussion?start=%s'%num
        url = groups[groupname] + str(num)
        urldict[url] = groupname
        allurl.append(url)

        num += 25
        # wb.save("/Users/ryu/Documents/rent.xlsx")

    # # print allurl
pool = Pool()
result = pool.map(crwalmain, urldict)
pool.close()
pool.join()

# # 多线程4.7s，测试单线程5.4s
# result = []
# for i in allurl:
#     j = crwalmain(i)
#     result.append(j)

print 'totally how many new iteams?', len(result)
# print result
print '\n*7',
count = 0
for i2 in result:
    for i in i2:
        if i:
            print i[0]
            ws.append(i)
            count += 1

wb.save("/Users/ryu/Documents/rent1104.xlsx")
print 'done with %s new iteams!' % count
