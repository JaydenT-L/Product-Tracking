import requests, json,  time, lxml.html, sqlite3
from dhooks import Webhook, Embed
from multiprocessing import Process
from log import read, get_working_proxy

headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }

webhooks = {
        'walmart' : ['https://discordapp.com/api/webhooks/701276545624440832/MS9v_lNscJeRyHvjeLa4ewt0Y_mskhSQYuNl-BDIXSKPChQG1YALJC92PVynK-V6gCFZ'],
        'bestbuy' : ['https://discordapp.com/api/webhooks/701276375906254848/PJRXlf985ILXojHU4ynlsA7ao4AopK5BWxY8zekyEQ3MU-EaOEIeebnkc1CqG5CJHCLk'],
        'target' : ['https://discordapp.com/api/webhooks/701276456944402522/WOPVidyHpciWqYFvBB3a-LsOdzXHOPo-Tc9kqYaHWMC9Ck-Ql0UAEWRMjd4_mKFNwsqN'],
        'gamestop' : ['https://discordapp.com/api/webhooks/701276603983986739/0EMVgtVGGdB6A7cxh4XzsTgnajeoku5nTnfU9cichX5Oheh-_0p6fTBYibeqk-OtC7vF']
        }
'''
webhooks = {
        'bestbuy' : ['https://discordapp.com/api/webhooks/704824749783515307/z11mqmaRUM4jAmsf3EmPYSI0NJtPyxFmLpm8cFhVjWwc-LoOjryG7S29LWTFi3WultJE'],
        'gamestop' : ['https://discordapp.com/api/webhooks/704824627804897392/KDJEMHTlOx8PM6I64JfOBQQYSKSgKeslRDDqDAZ1Uwop01W3i7slkCA6Ou8pPFx5aEgz'],
        }
'''
headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }

 


def send_to_webhook(product):
    embed = Embed(
    description= "**[{}]({})**".format(product["title"], product["url"]),
    color=0xff4242,
    timestamp='now'  # sets the timestamp to current time
    )
    
    image = 'https://cdn.discordapp.com/attachments/656441208830164992/697147827247120447/1.png'
    
    embed.set_author(name='{} MONITOR'.format(product['store'].upper()), icon_url=image)
    embed.add_field(name='**Product ID**', value= product["id"])
    if len(product["price"]) > 0:
        embed.add_field(name='**Price**', value= product["price"])
    if len(product["atc"]) > 0:
        embed.add_field(name='**ATC**', value= "[{}]({})".format("Buy here", product["atc"]))
    
    embed.add_field(name= '**Links**', value= "[{}]({}) | [{}]({})".format("Cart Link", product["cart"], "Check Out", product['checkout']))
    embed.set_footer(text="Haru{}s Monitor".format("'"), icon_url=image)
    embed.set_thumbnail(product["image"])        
    for link in webhooks[product['store']]:
        hook = Webhook(link)
        hook.send(embed=embed)
        print("SUCCESS POST {} TO {} MONITOR".format(product["title"], product['store']))    
                
class TechMonitor:
    def __init__(self,skuList, zone):
        self.zone = zone
        self.skuList = skuList
        self.session = requests.Session()
        self.info = {"store" : "","url" : "","atc" : "","image" : "","price" : "","title" : "", "id" : "","status" : "","checkout":"","cart":""} 
           
    def BestBuy(self):                 
        for skuid in self.skuList:        
            start = time.time()
            self.info["url"] = "https://bestbuy.com/site/ip/{}.p".format(skuid)
            self.info['id'] = skuid
            self.info['store'] = "bestbuy"
            r = get_working_proxy(self.info['url'],self.info['store'],headers, self.zone)            
            try:   
                a = lxml.html.fromstring(r.content)    
                self.info['checkout'] = 'https://www.bestbuy.com/checkout/r/fast-track'
                self.info['cart'] = 'https://www.bestbuy.com/cart'                                   
                self.info['atc'] = "https://api.bestbuy.com/click/-/{}/cart".format(skuid)
                self.info['image']= a.xpath('//img[@class="primary-image"]/@src')[0]                
                self.info['price'] = a.xpath('//span[@class="sr-only"]/text()')[1]
                self.info['title'] = a.xpath('//h1[@class="heading-5 v-fw-regular"]/text()')[0]
                self.info['status'] = a.xpath('//button[@class="btn btn-disabled btn-lg btn-block add-to-cart-button"]/text()')                
                if len(self.info['status']) == 0:
                    self.info['status'] = a.xpath('//button[@class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button"]//text()')[0]
               
            except IndexError:                         
                pass                
            add_to_db(self.info, start)        

    def GameStop(self):
        for skuid in self.skuList:
            start = time.time()
            self.info['url'] = "https://www.gamestop.com/on/demandware.store/Sites-gamestop-us-Site/default/Product-Variation?dwvar_{}_condition=New&pid={}&quantity=1".format(skuid, skuid)
                 
            self.info['store'] = 'gamestop'  
            self.info['checkout'] = 'https://www.gamestop.com/checkout/login/'
            self.info['cart'] = 'https://www.gamestop.com/cart/'   
            t = get_working_proxy(self.info['url'],self.info['store'],headers, self.zone)    
        
            try:                  
                loaded_js = json.loads(t.text)
                self.info["id"] = loaded_js['gtmData']['productInfo']['productID']                   
                self.info["image"] = loaded_js['product']['images']['large'][0]['url']
                self.info["title"] = loaded_js['product']['productName']                   
                self.info['url'] = "https://www.gamestop.com/blaze/{}.html".format(skuid)
                self.info['price'] = loaded_js['product']['price']['sales']['formatted']
                self.info["status"] = loaded_js['gtmData']['productInfo']['availability']
            except Exception:
                pass          
            
            add_to_db(self.info, start)

    def Target(self):
        
        for skuid in self.skuList:            
            start = time.time()
            self.info["url"] = "https://www.target.com/p/blaze/-/A-{}".format(skuid)        
            self.info['store'] = 'target'           
            self.info['cart'] = 'https://www.target.com/co-cart'  
            self.info['checkout'] = 'https://www.target.com/co-login?interstitial=true&redirectToURL=%2Fco-review%3Fprecheckout%3Dtrue'
            r = get_working_proxy(self.info['url'],self.info['store'],headers,self.zone)
            try:
                a = lxml.html.fromstring(r.content)
                #https://redsky.target.com/v2/pdp/tcin/52161278
                
                jS = a.xpath('//*[@id="viewport"]/div[4]/script/text()')
                loaded_js = json.loads(jS[0])                
                for b in loaded_js["@graph"]:                    
                    if b["@type"] == "Product":                        
                        self.info["id"] = b["sku"]                        
                        self.info["image"] = b["image"]
                        self.info["title"] = b["name"]                        
                        self.info["status"] = b["offers"]["availability"]  
                       
            except Exception as err:                                          
                print("{} : {}".format(err, skuid))               
                pass                                   
            add_to_db(self.info, start)
        
    def Walmart(self):
        #get walmart UPCA bang cach search gtin13 bo~ so' 0 dau` tien
        for skuid in self.skuList:
            start = time.time()
            self.info['store'] = 'walmart' 
            self.info['url'] = "https://search.mobile.walmart.com/v1/products-by-code/UPC/{}?storeId=1".format(skuid)
            r = get_working_proxy(self.info['url'],self.info['store'],headers, self.zone)
            try:
                loaded_js = json.loads(r.text)  
                self.info['checkout'] = 'https://www.walmart.com/checkout/#/fulfillment'
                self.info['cart'] = 'https://www.walmart.com/cart'  
                
                self.info['atc'] = 'http://c.affil.walmart.com/t/api01?l=http%3A%2F%2Faffil.walmart.com%2Fcart%2FaddToCart%3Fitems%3D{}%7C1%26affp1%3D%7Capk%7C%26af'.format(loaded_js['data']['common']['productId']['wwwItemId'])
                self.info["id"] = loaded_js['data']['common']['productId']['wwwItemId']                    
                self.info["image"] = loaded_js['data']['common']['thumbnailImageUrl']
                self.info["title"] = loaded_js['data']['common']['name']                     
                self.info['url'] = loaded_js['data']['common']['productUrl']
                self.info['price'] = "${}".format(("%.2f" % (loaded_js['data']['inStore']['price']['priceInCents'] / 100.0)))
                
                s = get_working_proxy(self.info['url'],self.info['store'],headers, self.zone)
                a = lxml.html.fromstring(s.content)
                jS = a.xpath('//*[@id="item"]/text()')
                jss = json.loads(jS[0])           
                
                self.info['status'] = jss['item']['product']['buyBox']['products'][0]['availabilityStatus']
            except Exception:
                pass
            add_to_db(self.info, start)

def add_to_db(product, start):    
    # Mark instock and OOS       
    avaiable = ["InStock", "Add to Cart","In Stock", "Available", "OnlineOnly", "IN_STOCK" ]
    if product['status'] in avaiable  :
        product["status"] = "Y"
    else:
        product["status"] = "N"
    end = time.time()   
    
    # Create database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS {}(link TEXT UNIQUE, title TEXT, instock TEXT)""".format(product['store']))


    # Add product to database if it's unique
    try:        
        c.execute("""INSERT INTO {} (link, title, instock) VALUES (?, ?, ?)""".format(product['store']), (product['url'], product["title"], product["status"]))
        print("Found new product <{}> <{}> IN {}s.".format(product["store"].upper(),product["title"], str(round((end - start), 3))))
        
        if product['status'] == 'Y':
            send_to_webhook(product)
        
    except Exception:
        c.execute("SELECT * FROM {} WHERE link='%s'".format(product['store']) %(product["url"]))
        data = c.fetchall()        
        if product["status"] == "Y":
            if data[0][2] != "Y":
                c.execute("""UPDATE {} SET instock = ? WHERE link = ?""".format(product['store']), (product["status"], product["url"]))
                print("<{}> <{}> is RESTOCKING Catched in {}s.".format(product["store"].upper(),product["title"], str(round((end - start), 3))))
        
                send_to_webhook(product)
            else:
                print("Product <{}>  [{}] in <{}> ALREDY IN DATA".format(product["title"], product["id"], product['store'].upper()))
        else:
            print("Product <{}>  [{}] in <{}> IS OUT OF STOCK".format(product["title"], product["id"], product['store'].upper()))
    
    # Close database
    conn.commit()
    c.close()
    conn.close()

    # Return whether or not it's a new product
    return product

def TechMain(flag):
    
    while flag == True:
        inforList = read()['keywords']
       
        Process( target = TechMonitor(inforList["bestbuy"], 'us').BestBuy()).start
        Process( target = TechMonitor( inforList["walmart"], 'us').Walmart()).start
        Process( target = TechMonitor(inforList["target"], 'us').Target()).start
        Process( target = TechMonitor(inforList["gamestop"], 'us').GameStop()).start
        
TechMain(True)