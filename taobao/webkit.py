from scrapy.http import Request, FormRequest, HtmlResponse
from selenium import webdriver
import settings

class WebkitDownloader( object ):
                browser = webdriver.Chrome();
    def process_request( self, request, spider ):

        if spider.name in settings.WEBKIT_DOWNLOADER:
            if( type(request) is not FormRequest ):
                browser.get(request.url);
                print request.url;
                ret = browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8');
                f = open('x.html','wb');
                return HtmlResponse(url=request.url,body =)
                f.write(browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8'));
                browser.close();
