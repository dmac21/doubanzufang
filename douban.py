#coding:utf-8
import requests,time,json
import smtplib
import MySQLdb as mdb
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

#数据库配置
config={
        'host':'XXX',
        'port':3306,
        'user':'qdm168113689',
        'passwd':'XXX',
        'db':'qdm168113689_db',
        'charset':'utf8'
        }
conn=mdb.connect(**config)
cur=conn.cursor()
search_keyword=[u'两房一厅',u'两房']
reject_keyword=[u'求租',u'合租']

group_dict={
    '广州海珠租房':'496744',
    '广州天河租房':'495738',
    '广州白云租房':'BaiYunZuFanG',
    '广州越秀租房':'496743',
    '广州番禺租房':'PanYuZuFanG',
    '广州花都租房':'HuaDuZuFanG',
    '广州荔湾租房':'499977',
    '广州3号线+5号线+APM地铁沿线租房':'499986',
    '广州租房':'90742',
    '广州租房团':'532699'
}

email_dict={
    'A':'XXX@qq.com',
    'B':'XXX@qq.com'
}

headers={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'Connection': 'keep-alive',
    'Host': 'frodo.douban.com',
    'Authorization': 'Bearer b0221a89dd0e184510664f9d972a48cf',
    'User-Agent': 'api-client/0.1.3 com.douban.frodo/5.20.0 iOS/10.0.2 iPhone8,1 network/wifi'
}

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def insert_into_db(value):
    cur.execute('insert into doubanzufang values(%s,%s,%s,%s,%s,%s,%s)', value)
    pass

def check_if_id_exist(id):
    check_sql = "select id from doubanzufang where id='%s'" %id
    cur.execute(check_sql)
    result = cur.fetchall()
    return result

def check_if_true_to_us(title):
    for keyword in search_keyword:
        if keyword in title:
            return True
        else:
            return False

def check_if_hezu(title):
    for keyword in reject_keyword:
        if keyword in title:
            return False
        else:
            return True

def send_email(msg_to,content):
    msg_from='XXX@163.com'
    passwd='XXX'
    subject='新租房消息推送'
    msg=MIMEText(content, 'html', 'utf-8')
    msg['Subject']=subject
    msg['From']=_format_addr(u'来自豆瓣租房<%s>' %msg_from)
    msg['To']=','.join(msg_to)
    s = smtplib.SMTP('smtp.163.com')
    try:
        s.login(msg_from,passwd)
        s.sendmail(msg_from,msg_to,msg.as_string())
        print '发送成功'
    except:
        print '发送失败'
    finally:
        s.quit()

def main():
    s = requests.Session()
    serachtime = int(time.time())
    serachtime = str(serachtime)
    content_begin = '<html><body><table><tbody>'
    content_end = '</tbody></table></body></html>'
    for groupid in group_dict.values():
        url = 'https://frodo.douban.com/api/v2/group/%s/topics?&_ts=%s&alt=json&apikey=XXX&count=100&douban_udid=19822b6cd0b406ba4f0a054036f0131858916720&latitude=23.09070561548983&loc_id=118281&longitude=113.3309972194148&sortby=new&start=0&udid=4a5b1fedc42088efd9f0976872d50856b14f2a1c&version=5.20.0' %(groupid,serachtime)
        response = s.get(url, headers=headers, verify=False)
        data_dict = json.loads(response.text)
        print data_dict
        for topic in data_dict['topics']:
            topic_value = [topic['id'], topic['title'],topic['create_time'],topic['update_time'],topic['url'],topic['comments_count'], topic['like_count']]
            if check_if_hezu(topic['title']) ==True and check_if_true_to_us(topic['title'])==True:
                if check_if_id_exist(topic['id'])==():
                    insert_into_db(topic_value)
                    #接下来发送邮件
                    content_mid='<tr class="cen"><td><a href=%s>%s</a></td></tr>'%(topic['url'],topic['title'])
                    content_begin=content_begin+content_mid
    content=content_begin+content_end
    if content!='<html><body><table><tbody></tbody></table></body></html>':
        send_email(['XXX@qq.com','XXX@qq.com','XXX@qq.com'],content)

if __name__=='__main__':
        main()




