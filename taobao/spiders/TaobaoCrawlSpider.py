# coding:utf-8
from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
import re
import sys
import json
from taobao.items import TaobaoItem
reload(sys)
sys.setdefaultencoding('utf-8')


class TaobaoSpider(CrawlSpider):
    name = "taobao"
    settings = get_project_settings()
    print(settings.get('GOODS_TYPE_CAT'))
    allowed_domains = ["tmall.com"]
    start_urls = [
        'https://list.tmall.com/search_product.htm?cat='+settings.get('GOODS_TYPE_CAT')]

    def parse(self, response):
        sel = Selector(response)
        con = sel.xpath('//a[contains(@href,"detail.tmall.com/item.htm?id")]')
        page = sel.xpath('//a[contains(@class,"ui-page-next")]')
        # yield Request('https://detail.tmall.com/item.hbtm?id=524546739131',callback=self.con_pares);
        print (response.url);
        for c in con:
            l = c.xpath('@href').extract()[0];
            m = re.match('.*detail\.tmall\.com\/item\.htm\?id\=(\d*)\&.*',l);
            id = m.group(1);
            yield Request('https://detail.tmall.com/item.htm?id='+id,callback=self.con_pares);

        for p in page:
            l = p.xpath('@href').extract()[0];
            m = re.match('.*\?cat\='+self.settings.get('GOODS_TYPE_CAT')+'\&s\=(\d*)\&.*',l);
            id = m.group(1);
            if int(id) < int(self.settings.get('GOODS_SUM')):
                yield Request('https://list.tmall.com/search_product.htm?cat='+self.settings.get('GOODS_TYPE_CAT')+'&s='+id,callback=self.parse);

    def con_pares(self, response):
        print (response.url);
        sel = Selector(response)
        item = TaobaoItem()
        # 获取商品名
        name = sel.xpath('//head/title/text()').extract()[0].strip()
        m = re.match('(.*)\-tmall\.com.*', name)
        name = m.group(1)
        item['name'] = name.encode('utf-8')
        #self.file.write('---商品名称-----' + name + '\n')
        # print ('---商品名称-----' + name + '\n')
        # # 商品默认图片
        img = sel.xpath(
            '//ul[@id="J_UlThumb"]/li/a/img/@src').extract()[0].strip()
        img = img.replace('_60x60q90.jpg', '')
        item['img'] = img.encode('utf-8')
        # print(img);
        # 商品ID
        l = sel.xpath(
            '//a[@id="J_AddFavorite"]/@data-aldurl').extract()[0].strip()
        m = re.match('.*itemId\=(\d*).*', l)
        gid = m.group(1)
        item['gid'] = gid.encode('utf-8')
        # print(gid)
        # SEO 关键字
        keywords = sel.xpath(
            '//meta[@name="keywords"]/@content').extract()[0].strip()
        item['keywords'] = keywords.encode('utf-8')
        # print(keywords)

        # SEO 描述
        description = sel.xpath(
            '//meta[@name="description"]/@content').extract()[0].strip()
        item['description'] = description.encode('utf-8')
        # print(description)

        # 价格属性
        price_attr = {}
        jgd = sel.xpath('//ul[contains(@class,"J_TSaleProp")]')
        for jg in jgd:
            jddd = []
            jgvs = jg.xpath('li')
            for jgv in jgvs:
                v = {}
                v['price_id'] = jgv.xpath('@data-value').extract()[0].strip()
                v['price_value'] = jgv.xpath(
                    'a/span/text()').extract()[0].strip()
                jddd.append(v)
                price_attr[jg.xpath('@data-property').extract()[0].strip()] = jddd

        item['price_attr'] = price_attr


        # 价格值
        scr = sel.xpath(
            '//script[contains(text(),"skuMap")]/text()').extract()[0].encode('utf-8')
        scr = scr[scr.find('"skuMap":') +
                  9:scr.find(',"valLoginIndicator"') - 1]
        scr = eval(scr)
        scrimg = sel.xpath('//ul[@id="J_UlThumb"]/li/a/img/@src').extract();
        scri =0;
        for scrs in scr:
            scr[scrs]['imgurl'] =scrimg[scri%len(scrimg)].encode('utf-8').replace('_60x60q90.jpg','')
            scri =scri +1

        item['price_value'] = scr;




        # 商品属性
        attrs = sel.xpath('//table[@class="tm-tableAttr"][1]/tbody/tr')
        attr = {}
        pa = "null"
        for tr in attrs:
            if tr.xpath('@class'):
                pa = tr.xpath('th/text()').extract()[0].strip()
                attr[pa] = {}
            else:
                key = tr.xpath('th/text()').extract()[0].strip()
                value = tr.xpath(
                    'td/text()').extract()[0].encode('gbk', 'ignore').decode('gbk').strip()
                attr[pa][key] = value

        item['attr'] = attr
        # print(attr);
        return item;
        #item['text'] = sel.xpath('//table[@class="description"]/div/text()').extract()[0].strip();
        # txt = tex.decode('unicode_escape');
        # print tex;
        # html_parser = HTMLParser.HTMLParser();
        # txt = html_parser.unescape(tex);
        # print txt;
        # m = re.match('.*skuMap(.*)valLoginIndicator.*',scr);
        # value = m.group(1);
        # print value;
        # file = open('dat.json','wb')
        # line = json.dumps(item['text']);
        # file.write(line.decode('unicode_escape'))
        #return item
