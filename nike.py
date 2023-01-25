import requests, json,datetime, random, time, sys, lxml.html, sqlite3, discord, re
from multiprocessing import Process
from log import read, get_working_proxy
import nested_lookup 

urls = {
    'ca' : 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=60&filter=marketplace%28CA%29&filter=language%28en-GB%29&filter=inStock%28true%29&filter=productInfo.merchPrice.discounted%28false%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title',
    'snkrs' : 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=60&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title',
    'cn' : 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=60&filter=marketplace%28CN%29&filter=language%28zh-Hans%29&filter=inStock%28true%29&filter=productInfo.merchPrice.discounted%28false%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title',
    'jp' : 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=60&filter=marketplace%28JP%29&filter=language%28ja%29&filter=inStock%28true%29&filter=productInfo.merchPrice.discounted%28false%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title',
    'gb' : 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=60&filter=marketplace%28GB%29&filter=language%28en-GB%29&filter=inStock%28true%29&filter=productInfo.merchPrice.discounted%28false%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title',
    'us' : 'https://api.nike.com/product_feed/threads/v2?filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&anchor=0&count=60&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title'
}

webhooks = {
        'bestbuy' : ['https://discordapp.com/api/webhooks/704824749783515307/z11mqmaRUM4jAmsf3EmPYSI0NJtPyxFmLpm8cFhVjWwc-LoOjryG7S29LWTFi3WultJE'],
        'gamestop' : ['https://discordapp.com/api/webhooks/704824627804897392/KDJEMHTlOx8PM6I64JfOBQQYSKSgKeslRDDqDAZ1Uwop01W3i7slkCA6Ou8pPFx5aEgz'],
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

class NikeMonitor:
    def __init__(self,skuList):
     
        self.skuList = skuList
        
        self.info = {"store" : "",'entrydate':'',"publishdate":"",'exclusiveaccess':'','type':'','status':'','method':'','subtitle':'',"url" : "", 'style':'',"image" : "","price" : "","title" : "",'color':'',"stock" : {}} 
       
    def checkstock(self, zone):
        try:
           
            start = time.time()
            r = get_working_proxy(urls['snkrs'], 'nike', headers, 'us').json()            
            for item in range(len(r['objects'])): #total products
                temp = {}
                if 'productInfo' in r['objects'][item].keys():
                    for product in range(len(r['objects'][item]['productInfo'])): #total SKU in products
                        #if any(s.lower() for s in self.skuList for s in r['objects'][item]['productInfo'][product]['productContent']['title'].lower().split()):                            
                        c = 0
                        self.info['title'] = r['objects'][item]['productInfo'][product]['productContent']['title']
                        self.info['image'] = r['objects'][item]['productInfo'][product]['imageUrls']['productImageUrl']
                        self.info['color'] = r['objects'][item]['productInfo'][product]['productContent']['colorDescription']   
                        self.info['store'] = 'Nike ' + zone.upper() 
                        self.info['type'] = r['objects'][item]['productInfo'][product]['merchProduct']['publishType']
                        self.info['exclusiveaccess'] = r['objects'][item]['productInfo'][product]['merchProduct']['exclusiveAccess']
                        self.info['publishdate']   = r['objects'][item]['productInfo'][product]['merchProduct']['commercePublishDate']
                        self.info['gender'] = " / ".join(str(x) for x in r['objects'][item]['productInfo'][product]['merchProduct']['genders'])
                        self.info['status'] = r['objects'][item]['productInfo'][product]['merchProduct']['status']
                        self.info['style'] = r['objects'][item]['productInfo'][product]['merchProduct']['styleColor']
                        self.info['url'] = 'https://www.nike.com/launch/t/' + r['objects'][item]['publishedContent']['properties']['seo']['slug']
                        self.info['price'] = '$' + str(r['objects'][item]['productInfo'][product]['merchPrice']['currentPrice'])
                        self.info['subtitle'] = r['objects'][item]['publishedContent']['nodes'][product]['properties']['title']
                        if 'launchView' in r['objects'][item]['productInfo'][product].keys():
                            self.info['entrydate'] = r['objects'][item]['productInfo'][product]['launchView']['startEntryDate']
                            self.info['method'] = r['objects'][item]['productInfo'][product]['launchView']['method']
                        
                        #r['objects'][item]['publishedContent']['properties']['products']
                        for sku in range(len(r['objects'][item]['productInfo'][product]['availableSkus'])):                        
                            if c == 0:
                            #if r['objects'][item]['productInfo'][product]['skus'][sku]['productId'] == r['objects'][item]['productInfo'][product]['availableSkus'][sku]['productId'] and \
                            #r['objects'][item]['productInfo'][product]['availableSkus'][sku]['id'] == r['objects'][item]['productInfo'][product]['skus'][sku]['id'] :
                                
                                temp.update({r['objects'][item]['productInfo'][product]['skus'][sku]['nikeSize']:r['objects'][item]['productInfo'][product]['availableSkus'][sku]['level']})
                        self.info['stock'] = temp
                        temp = {}
               
                print(self.info)
         
                #
                        #self.add_to_db(start, 'nike', zone)
        except Exception:
            print('Loading main page failed')
            self.checkstock(zone)
        return 0



def list_recursive(mydict, path=(), output='' ):
    try:
        if type(mydict) == dict:
            print(0)
        elif type(mydict) == list:
            print(0)

    except Exception:
        print(output)

def NikeMain(flag):
  
   
    #inforList = read()
    
    NikeMonitor(read()['keywords']['nike']).checkstock('us')
  
    '''
    r = get_working_proxy(urls['snkrsus'], 'nike', headers, 'us').json()      
    #keys = nested_lookup.nested_lookup('productInfo',r)
    #js = json.load(keys[1])
    print(r['objects'][0]['publishedContent']['nodes'][0]['properties']['title'])
    print(r['objects'][0]['productInfo'][0]['skus'][0]['id'])
    print(r['objects'][0]['productInfo'][0]['availableSkus'][0]['id'])
    print(len(r['objects'][0]['publishedContent']['properties']['products']))
    print(r['objects'][0]['publishedContent'].keys())
    print(len(r['objects'][0]['publishedContent']['properties']))
    print(len(r['objects']))
    print(r['objects'][0].keys())
    print(r['pages']['totalPages'])
    print(r['pages']['totalResources'])
    #print(r['objects'][0]['publishedContent']['properties']['products'])
    #print(r['objects'][0]['productInfo'][0]['skus'])
    print('\n')
    #print(len(r['objects'][0]['productInfo'][0]['merchProduct']['genders']))
    print('\n')
    #print(r['objects'][0]['productInfo'][0]['merchProduct'].keys())
    print('\n')
    #print(r['objects'][0]['productInfo'][0]['availableSkus'][0].keys())
    #print(r['objects'][0]['productInfo'][0]['merchProduct']['styleCode'])
   '''
    '''
    r = get_working_proxy(urls['us'], 'nike', headers, 'us').json()     
    #print(json.dumps(r['objects'][6], indent=4))
    s = []
    y = []
    t = []
    for item in range(len(r['objects'])):
        if 'productInfo' in r['objects'][item].keys():
            for product in range(len(r['objects'][item]['productInfo'])):
                s.append(nested_lookup.nested_lookup('slug',r['objects'][item]['productInfo'][product]))
                #if r['objects'][item]['productInfo'][product]['merchProduct']['status'] not in s:
                #    s.append(r['objects'][item]['productInfo'][product]['merchProduct']['styleColor'])
            y.append(item)
        else:
            t.append(item)
    print(len(s))
    print(s)
    print(t)
    print(y)

    '''
    
    '''
    #producttype = 'flow' 'launch'
    #status = ['hold', 'active', 'closeout']
    #product type = ['footwear', 'apparel', 'equipment']
    #not product = [1, 5, 10, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 27, 32, 33, 37, 39, 40, 43, 44, 45, 46, 48, 50, 
    #51, 52, 53, 54, 56]
    
    #b = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ") #convert datetime
    #c = datetime.datetime.now() #get time now then minus with b
    #get hour > b.hour, get date 
    '''
    
    '''  
    with open('data.txt', 'w') as f:
        json.dump(r['objects'][2], f,indent=4)
        f.close()

    r = get_working_proxy(urls['us'], 'nike', headers, 'us').json()   
    print(r['objects'][2]['productInfo'][0]['launchView']['startEntryDate'])
    '''
NikeMain(True)
