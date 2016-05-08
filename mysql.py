# -*- coding: utf-8 -*-
from scrapy.http import Request, FormRequest, HtmlResponse
from selenium import webdriver
from scrapy import Selector
import time
import re
import MySQLdb

# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.Accept-Language'] = 'zh-CN,zh;q=0.8'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.accept-encoding'] = 'gzip, deflate, sdch'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.referer'] = 'https://nengliangsm.tmall.com/category.htm?spm=a220o.1000855.w10141499-10532015174.3.48T2xO&search=y&scene=taobao_shop'
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.user-agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.66 Safari/537.36"
# webdriver.DesiredCapabilities.CHROME[
#     'phantomjs.page.customHeaders.accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
# webdriver.DesiredCapabilities.CHROME['phantomjs.page.customHeaders.cookie'] = 'cna=4TmgD48x9hQCAXFrGBsRS63k; pnm_cku822=179UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktwTHNJcUp%2BRHFMdyE%3D%7CU2xMHDJ7G2AHYg8hAS8XKgQkCkwtSzdGaD5o%7CVGhXd1llXGdbZF5mXWlTZltgV2pIdU92SHZPdUxwS3VBf0Z8SXdZDw%3D%3D%7CVWldfS0SMg40CioWKAgmSjtIeEhsUSAecE5nWnQidA%3D%3D%7CVmhIGCcbOwI3FyseJhw8BTgBPh4iFikUNAg1AD0dIRQuETENMAg8ajw%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; _tb_token_=Wmo8wx3RrSa9; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=true; uc3=nk2=G4mkbT%2Fi4%2FVeluw%3D&id2=WvENId01Qds%3D&vt3=F8dASm%2B9Olxw5RTfxL4%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; uss=VWomByBdqwDXpZWOIqzF1JU7MVNtqw4kukvvpp8TGYp213VnV3DCtc%2Fucg%3D%3D; lgc=xieiyanghui; tracknick=xieiyanghui; cookie2=90f8a78bf12b59cebd75182b915826de; cookie1=VW8d80BZwacDWJ3Or8sl1QJ4y9T1N5sR4CJ8Cd1vis8%3D; unb=91683733; skt=ae6b960c5fc15c40; t=3c8c250898fd6a888480c059dcb87fc3; _l_g_=Ug%3D%3D; _nk_=xieiyanghui; cookie17=WvENId01Qds%3D; login=true; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=12721; whl=-1%260%260%260; l=AnV1KRkVGEapGf/UJ1l2BedEBfsvbykE'


db = MySQLdb.connect(host="localhost", user="root",passwd="xiehui", db="mall258", charset='utf8')
cur = db.cursor()
cur.execute("select g_number,g_id from goods");
b = cur.fetchall()
browser = webdriver.Chrome();

for a in b:
    url = 'https://detail.tmall.com/item.htm?id='+str(a[0]);
    browser.get(url);
    # fi = open('hh.html','wb');
    # fi.write(bb);

    # print browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8')
    time.sleep(10)
    # b = browser.find_elements_by_id('description')[0].text;
    bb = browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8');
    # fi = open('hh.html','wb');
    # fi.write(bb);
    hbb = HtmlResponse(url='https://detail.tmall.com/item.htm?id=521893618096',body =bb);
    s = Selector(hbb)
    ss= s.xpath('//div[@id="description"]/div').extract()[0].encode('utf-8')
    src = re.compile('src\=\"\/\/[^\"]*\.png\"');
    ss = re.sub(src,"",ss);
    src = re.compile('alt\=\"[^\"]*\.jpg\"');
    ss = re.sub(src,"",ss);
    src = re.compile('data-ks-lazyload');
    ss = re.sub(src,"src",ss);
    cur.execute('update goods set g_text = %s where g_id = %s',[ss,a[1]] );

cur.commit();
cur.close();
db.close();
browser.close();

