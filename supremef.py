import requests, json, random, time, os, lxml.html, sqlite3
from multiprocessing import Process
from log import read, get_working_proxy, add_to_db

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


def get_links(linklist):   
    try:
        inforList = read()
        
        print('<SUCCESS> LOADED <Infor> and <Proxies>\nDELAY SET TO {}'.format(inforList['delay']))
                
        conn = sqlite3.connect('supreme.db')
        c = conn.cursor()      
        for i in linklist.keys():     
            try:
                c.execute("SELECT * FROM {}".format(i))            
                data = c.fetchall()     
                
                for datakey in data:
                    for inforkey in  inforList['keywords']['supreme']:
                        a = datakey[1].lower().split()
                    
                        if any(item in a for item in inforkey):                          
                            linklist[i].append(datakey[0])
            except Exception:                
                pass
        # Close database
        conn.commit()
        c.close()
        conn.close()
    except Exception as err:
        print('<FALSE><ERROR> {}'.format(err))
        pass
    return linklist, inforList

class SupremeMonitor:
    def __init__(self, site, store, monitor, zone):
        self.zone = zone
        self.monitor = monitor
        self.site = site        
        self.session = requests.Session()        
        self.info = {"store" : store+zone,'zone': self.zone,'cata':'','color':'',"url" : "","image" : "","price" : "","title" : "","status" : ""} 
       
    def one_link(self, link, count):      
        headers['Referer'] = link
        headers['User-Agent'] = random.choice(userAgent)
        r = get_working_proxy(link,self.info['store'],headers,self.zone)
  
        self.info['cata'] = link.split('/')[4]
        if r != None:
            a = lxml.html.fromstring(r.content)    
            start = time.time()            
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
                add_to_db(self.info, start, self.monitor, self.zone)                
            else:
                print("<FAIL> on loading this <{}>, {} time(s)".format(self.info['url'], count))
                count += 1
                self.one_link(link, count)     

def SupremeFMain(flag):    
    
    print("...Loading Data")
    linkl, infor = get_links({'supremeus': [], 'supremeeu':[], 'supremejp':[]})
    last_update = time.ctime(os.path.getmtime("information.txt"))
    
    while flag == True:
        if last_update != time.ctime(os.path.getmtime("information.txt")):
            print('<KEYWORD UPDATE> Reloading data')
            linkl, infor= get_links(linkl)
            last_update = time.ctime(os.path.getmtime("information.txt"))     
            flag = True   
        else:         
            for store in linkl:
                for link in linkl[store]:
                    Process( target = SupremeMonitor('https://www.supremenewyork.com', store, 'supremef', 'us').one_link(link, 1)).start
      
                    #SupremeMonitor(proxy, 'https://www.supremenewyork.com', store).one_link(link, 1) 
        time.sleep(int(infor['delay']))

SupremeFMain(True)