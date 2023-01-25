
import requests, json,datetime, random, time, sys, lxml.html, sqlite3, discord, re
from multiprocessing import Process
from log import read, get_working_proxy, add_to_shopify_db
import nested_lookup 

urls = {
        'undefeated' : 'https://undefeated.com/collections/all/products.json?limit=250&page=',
        'kith' : ['https://kith.com/collections/new-arrivals/products.json?limit=250&page=', 'https://kith.com/collections/kith-monday-program/products.json?limit=250&page=']
        }

headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }

class ShopifyMonitor:
    def __init__(self):        
        self.info = {
                "store" : "",
                'id' : '',                
                "url" : "", 
                "image" : "",
                'keywords' : '',
                "price" : "",
                "title" : "",               
                "stock" : {}} 
       
    def checkstock(self, zone):
        try:            
            for store in urls.keys():                  
                self.info['store'] = store                
                if store == 'kith':
                    for link in urls['kith']:                   
                        self.one_link(link, zone)
                else:                    
                    self.one_link(urls[store], zone)
                    
        except Exception as err:
            print(err)
            self.checkstock(zone)
        return 0

    def one_link(self,link, zone):
        count = 1         
        r = get_working_proxy('{}{}'.format(link, str(count)), 'shopify', headers, 'us').json()
        #print(len(r['products']))        
        while len(r['products']) > 1:       
            start = time.time()  
            for item in range(len(r['products'])): #total products                                          
                temp = []  
                self.info['id'] = str(r['products'][item]['id'])                
                self.info['image'] = r['products'][item]['images'][0]['src']
                self.get_url(item, r)                
                self.info['title'] = r['products'][item]['title']
                self.info['keywords'] = r['products'][item]['handle'].split('-')                                                
                self.info['price'] = '$' + str(r['products'][item]['variants'][0]['price'])
                for variants in range(len(r['products'][item]['variants'])): #total available variants in products                            
                    if str(r['products'][item]['variants'][variants]['available']).lower() == 'true':                      
                        if str(r['products'][item]['variants'][variants]['option1']) in ['-']:
                            temp.append([str(r['products'][item]['variants'][variants]['option2']),str(r['products'][item]['variants'][variants]['id'])])
                        elif r['products'][item]['variants'][variants]['option2'] == None:
                            if str(r['products'][item]['variants'][variants]['option1']).lower() in ['default title']:
                                temp.append(['One Size',str(r['products'][item]['variants'][variants]['id']) ])
                            else:
                                temp.append([str(r['products'][item]['variants'][variants]['option1']),str(r['products'][item]['variants'][variants]['id']) ])
                        else:
                            temp.append(['{} | {}'.format(str(r['products'][item]['variants'][variants]['option1']),str(r['products'][item]['variants'][variants]['option2'])),str(r['products'][item]['variants'][variants]['id'])])
                            
                self.info['stock'] = temp 
                temp = []
                
                add_to_shopify_db(self.info, start, 'shopify', 'us')
                    
            count += 1
            r = get_working_proxy('{}{}'.format(link, str(count)), 'shopify', headers, 'us').json()
        
    def get_url(self, index, page):
        if self.info['store'] == 'undefeated':
            self.info['url'] = 'https://undefeated.com/collections/all/products/' + page['products'][index]['handle'] + '?variant=' + self.info['id']
        elif self.info['store'] == 'kith':
            self.info['url'] = 'https://kith.com/products/'+ str(page['products'][index]['handle'])

def shopifyMain(flag):
  
   
    #inforList = read()
    
    ShopifyMonitor().checkstock('us')
    '''
    r = get_working_proxy(urls['kith'][0], 'shopify', headers, 'us').json()   
    with open('data.txt', 'w') as f:
        json.dump(r, f,indent=4)
        f.close()
   '''
shopifyMain(True)
#https://undefeated.com/collections/all/products.json
#https://undefeated.com/products.json product page
#https://undefeated.com/pages.json <<<raffle link in "handle" https://undefeated.com/pages/jordan-aj-1-retro-high-og-online-raffle