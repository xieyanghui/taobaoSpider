# -*- coding: UTF-8 -*-
from scrapy.http import Request, FormRequest, HtmlResponse
from selenium import webdriver
from scrapy import Selector
import MySQLdb
import MySQLdb.cursors
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.Accept-Language'] = 'zh-CN,zh;q=0.8'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.accept-encoding'] = 'gzip, deflate, sdch'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.referer'] = 'https://www.taobao.com/'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.user-agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
# webdriver.DesiredCapabilities.CHROME['phantomjs.page.customHeaders.cookie'] = 'thw=cn; cna=RxiHDxJFHXwCAXFrGBXRpVPs; _tb_token_=jIaFMXEaSHKx; v=0; uc3=sg2=BxJI75OXv%2BrGwlSyO3%2B%2Bo%2FZOZqNe6puD3ZG1gASYsEo%3D&nk2=G4mkbT%2Fi4%2FVeluw%3D&id2=WvENId01Qds%3D&vt3=F8dASm%2ByjaXjByDtmH0%3D&lg2=URm48syIIVrSKA%3D%3D; existShop=MTQ2MTE4MjUzNw%3D%3D; uss=AVYvf3Duh%2FIsmVrp%2BMC6poj0OKS1WqsQ8h2JUxK6nvbT2m7xE%2BBIcRwi7w%3D%3D; lgc=xieiyanghui; tracknick=xieiyanghui; sg=i32; skt=fe1681a19b5153bc; _cc_=URm48syIZQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; cookie2=5c8ec8953b5b446a3e3a65595f342c81; cookie1=VW8d80BZwacDWJ3Or8sl1QJ4y9T1N5sR4CJ8Cd1vis8%3D; mt=ci=0_1; unb=91683733; t=d0c722bfc572b3738c58d0da5a6f309a; _nk_=xieiyanghui; cookie17=WvENId01Qds%3D; uc1=cookie14=UoWxMPYJV4WW%2Fw%3D%3D&existShop=true&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=URm48syIZJfmYzXrEixrAg%3D%3D&tag=3&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261461188964713; l=Ak5OHd05N8yZg3TB6BQ91sUvHi4RNBLE'

browser = webdriver.Chrome()
db = MySQLdb.connect(host="localhost", user="root",
                     passwd="xiehui", db="mall258", charset='utf8')
cur = db.cursor()

cur.execute('select g_number,g_id from goods WHERE g_text like "%描述加载中%" OR ISNULL(g_text)')
gtas = cur.fetchall()
for n in gtas:
    try:
        browser.get("https://detail.tmall.com/item.htm?id="+n[0])
        time.sleep(5)
        b = browser.find_elements_by_id('description')[0].text;
        bb = browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8');
        hbb = HtmlResponse(url='https://detail.tmall.com/item.htm?id='+n[0],body =bb);
        s = Selector(hbb)
        ss= s.xpath('//div[@id="description"]/div').extract()[0].encode('utf-8')
        src = re.compile('src\=\"\/\/[^\"]*\.png\"');
        ss = re.sub(src,"",ss);
        src = re.compile('alt\=\"[^\"]*\.jpg\"');
        ss = re.sub(src,"",ss);
        src = re.compile('data-ks-lazyload');
        ss = re.sub(src,"src",ss);
        print (n[1])
        cur.execute('update goods set g_text = %s where g_id = %s',[ss,n[1]]);
        db.commit()
    except Exception, e:

        print ('-----------'+str(n[1]))
        cur.execute('DELETE FROM goods where g_id = %s',[n[1]]);
        db.commit()
    finally:
        pass


cur.close();
db.close();
browser.close()
# print browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8')


# print ss
