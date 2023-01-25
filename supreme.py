import requests, json,  random, time, lxml.html
from multiprocessing import Process
from log import get_working_proxy, add_to_db

headers = {
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
  'Referer' : '',
  'Accept':
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
  "Cache-Control": "max-age=0",
  'Sec-Fetche-Dest' : 'style',
  'Sec-Fetche-Mode' : 'no-cors',
  
  'Connection': "keep-alive",
  'User-Agent' : ''
}
userAgent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1)', 'AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/70.0.3538.77', 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X)', 'AppleWebKit/536.26 (KHTML, like Gecko)',  'Version/6.0 Mobile/10A5376e Safari/8536.25', 'Chrome/81.0.4044.129', 'Safari/537.36']

                
class SupremeMonitor:
    def __init__(self, site, store, monitor, zone):
        self.zone = zone
        self.monitor = monitor
        self.site = site        
        self.session = requests.Session()        
        self.info = {"store" : store+zone,'zone' : self.zone,'cata':'','color':'',"url" : "","image" : "","price" : "","title" : "","status" : ""} 
       
    def checkstock(self):       
        headers['Referer'] = self.site + '/shop/'
        r = get_working_proxy(self.site + '/shop/',self.info['store'], headers, self.zone)        
        a = lxml.html.fromstring(r.content)
        b = a.xpath('//*[@id="shop-scroller"]//a/@href')        
        for item in b:
            if b != None:
                headers['Referer'] = self.site + item
                headers['User-Agent'] = random.choice(userAgent)
                r = get_working_proxy(self.site + item,self.info['store'],headers,self.zone)
                a = lxml.html.fromstring(r.content)
                c = a.xpath('//button/@data-url')                           
                for subitem in c:
                    if 'alt=' not in subitem:                        
                        start = time.time()
                        headers['Referer'] = self.site + subitem
                        headers['User-Agent'] = random.choice(userAgent)
                        r = get_working_proxy(self.site + subitem,self.info['store'],headers,self.zone)
                        if r != None:
                            a = lxml.html.fromstring(r.content)                                
                            self.info['url'] = headers['Referer']                        
                            self.one_link(self.info['url'], 1)                           

                            if len(self.info['status']) != 0 or len(self.info['url']) != 0:                                
                                add_to_db(self.info, start, self.monitor, self.zone)     
                             
    def one_link(self, link, count):      
        headers['Referer'] = link
        headers['User-Agent'] = random.choice(userAgent)
        r = get_working_proxy(link,self.info['store'],headers,self.zone)
        self.info['cata'] = link.split('/')[4]
        if r != None:
            a = lxml.html.fromstring(r.content)                
            self.info['url'] = headers['Referer']              
            self.info['title'] = a.xpath('//*[@id="details"]/h2/text()')               
            if len(self.info['title']) > 0:
                self.info['title'] = self.info['title'][0]
                self.info['color'] = a.xpath('//*[@id="details"]/p[1]/text()')[0]
                self.info['image'] = a.xpath('//*[@id="img-main"]/@src')[0]
                self.info['price'] = a.xpath('//*[@id="details"]/p[3]/span/text()')[0]
                s = a.xpath('//*[@id="s"]/option/text()')                          
                if len(s) == 0:
                    s = a.xpath('//*[@id="add-remove-buttons"]/b/text()')
                    if len(s) == 0:
                        s = a.xpath('//*[@id="add-remove-buttons"]/input/@value')                                   
                self.info['status'] = s  
                #add_to_db(self.info, 0)                
            else:
                print("<FAIL> on loading this <{}>, {} time(s)".format(self.info['url'], count))
                count += 1
                self.one_link(link, count)    


def SupremeMain(flag):    
    while flag == True:
        print("...Loading Data")               
        print('Start searching items...')
        Process( target = SupremeMonitor('https://www.supremenewyork.com', 'supreme', 'supreme', 'us').checkstock()).start
        #Process( target = SupremeMonitor('https://www.supremenewyork.com','supreme', 'supreme','us').one_link('https://www.supremenewyork.com/shop/shirts/gl8yhj40t/c6eoa9vgn', 1)).start
        flag = True
    return 0
SupremeMain(True)