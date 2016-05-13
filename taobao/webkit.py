
import MySQLdb
import MySQLdb.cursors
db = MySQLdb.connect(host="localhost", user="root",
                     passwd="xiehui", db="mall258", charset='utf8')
cur = db.cursor()

cur.execute('select u_name from user')
gtas = cur.fetchall()
print(gtas)

# class WebkitDownloader( object ):
#                 browser = webdriver.Chrome();
#     def process_request( self, request, spider ):

#         if spider.name in settings.WEBKIT_DOWNLOADER:
#             if( type(request) is not FormRequest ):
#                 browser.get(request.url);
#                 print request.url;
#                 ret = browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8');
#                 f = open('x.html','wb');
#                 return HtmlResponse(url=request.url,body =)
#                 f.write(browser.page_source.encode('gbk','ignore').decode('gbk').encode('utf-8'));
#                 browser.close();
