import time, random, os.path, json, requests, cloudscraper, sqlite3, pickle, nested_lookup
from dhooks import Webhook, Embed

def tksQuickTask(link):
    link.replace('/', '%2F')
    link.replace(':', '%3A')
    return 'https://thekickstationapi.com/quick-task.php?link=' + link + '&autostart=true'
    
def cybersoleQuickTask(link):
    return ' https://cybersole.io/dashboard/tasks?quicktask=' + link

def projectdestroyQuickTask(link):
    return 'https://api.destroyerbots.io/quicktask?url=' + link

def ghostQuickTask(site, link):
    storelist = ['FootLockerUS', 'FootLockerCA', 'KidsFootLocker', 'FootAction',  'ChampsSports','Eastbay', 'SupremeUS', 'SupremeEU', 'Finishline', 'JDSports', 'Hibbett', 'AdidasUS', 'AdidasGB', 'AdidasCA', 'AdidasDE', 'AdidasPH', 'AdidasMY', 'AdidasSG', 'AdidasAU', 'AdidasTH', 'AdidasCZ', 'AdidasDK', 'AdidasES', 'AdidasGR', 'AdidasGR', 'AdidasIE', 'AdidasIT', 'AdidasNL', 'AdidasNO', 'AdidasRU', 'AdidasAT']
    for i in storelist:        
        if i.lower() == site:
            return 'https://api.ghostaio.com/quicktask/send?site={}&input={}'.format(i, link)
            
        else:
            return link

def read():
    f = open('information.txt', 'rb')
    a = pickle.load(f)
    f.close()
    return a

def write(output):
    f = open('information.txt', 'wb')
    pickle.dump(output, f)
    f.close()
    return 0
def search(key, container):
    return nested_lookup.nested_lookup(key, container)

def supreme_embed(product, embed):    
    embed.add_field(name='**Keywords**', value= product["title"], inline=False)
    embed.add_field(name='**Color**', value= product["color"])
    embed.add_field(name='**Price**', value= product["price"])
    embed.set_title("**{}**".format(product["title"]), product['url'])    
    stock = ''
    embed.set_thumbnail('http:' + str(product["image"]))   
    for s in product['status']:
        stock = stock + '{}\n'.format(s)    
    embed.add_field(name='**Catalog**', value= product['cata'], inline= False)
    embed.add_field(name='**Avaiable**', value= str(stock), inline=False)
    embed.add_field(name= '**Links**', value= "[{}]({}) | [{}]({})".format("Cart Link", 'https://www.supremenewyork.com/shop/cart', "Check Out", 'https://www.supremenewyork.com/checkout'), inline=False)
    embed.add_field(name= '**Quick Task**', value= "[{}]({}) | [{}]({}) | [{}]({}) | [{}]({})".format("Cyber", cybersoleQuickTask(product['url']) , "TKS", tksQuickTask(product['url']), 'PD', projectdestroyQuickTask(product['url']), 'Ghost', ghostQuickTask(product['store'], product['url'])), inline=False)  
    return embed

def shopify_embed(product, embed):
    stock = []
    embed.set_title("**{}**".format(product["title"]), product['url'])   
    embed.add_field(name='**Keywords**', value= ' '.join(product['keywords']), inline=False)
    embed.add_field(name='**ID**', value= product["id"])
    embed.add_field(name='**Price**', value= product["price"], inline= False)
  
    for s in product['stock']:        
        stock.append('[{}]({})'.format(s[0],'https://{}.com/cart/{}:1'.format(product['store'], s[1])))

    if len(stock) <= 5:
        embed.add_field(name='**ATC**', value= ' \n '.join(stock), inline=False)
    else:
        embed.add_field(name='**ATC**', value= ' \n '.join(stock[:len(stock)//2]))
        embed.add_field(name='**ATC**', value= ' \n '.join(stock[len(stock)//2:]))
  
    embed.add_field(name= '**Quick Task**', value= "[{}]({}) | [{}]({}) | [{}]({}) | [{}]({})".format("Cyber", cybersoleQuickTask(product['url']) , "TKS", tksQuickTask(product['url']), 'PD', projectdestroyQuickTask(product['url']), 'Ghost', ghostQuickTask(product['store'], product['url'])), inline=False)  
   
    embed.set_thumbnail(str(product["image"]))   
    return embed


def send_to_webhooks(product, alert, webhooks, monitor):
    embed = Embed(
    description= "**<{}>**".format(alert),
    color=0xff4242,
    timestamp='now'  # sets the timestamp to current time
    )
    #print("[{}]({}) | [{}]({}) | [{}]({}) | [{}]({})".format("Cyber", log.cybersoleQuickTask(product['url']) , "TKS", log.tksQuickTask(product['url']), 'PD', log.projectdestroyQuickTask(product['url']), 'Ghost', log.ghostQuickTask(product['store'], product['link'])))
  
    
    image = 'https://cdn.discordapp.com/attachments/656441208830164992/697147827247120447/1.png'
    embed.set_author(name='{} MONITOR'.format(product['store'].upper()), icon_url=image)
    if 'supreme' in monitor:
        embed = supreme_embed(product, embed)
    elif 'shopify' in monitor:
        embed = shopify_embed(product, embed)
   
    #embed.set_footer('Haru Monitor', icon_url=image)
 
   
 
    for link in webhooks:
        hook = Webhook(link)
        hook.send(embed=embed)
        print("SUCCESS POST {} TO {} MONITOR".format(product["title"], product['store'])) 


def get_proxy(proxyL):
    '''
    (list) -> dict
    Given a proxy list <proxy_list>, a proxy is selected and returned.
    '''
    try:
        # Choose a random proxy
        proxyS = proxyL
        proxies = {}
        proxy = proxyS.split(':')
        
        if proxyS.count(':') == 3:
            proxies = {
            "http": 'http://{}:{}@{}:{}/'.format(proxy[2],proxy[3],proxy[0],proxy[1]),
            "https": 'https://{}:{}@{}:{}/'.format(proxy[2],proxy[3],proxy[0],proxy[1]),
        }
        elif proxyS.count(':') == 1:
            proxies = {
            "http": 'http://{}:{}/'.format(proxy[0],proxy[1]),
            "https": 'https://{}:{}/'.format(proxy[0],proxy[1]),
        }
        else:
            print("ERROR: WRONG PROXY TYPE <{}>, PLEASE INPUT 2 TYPES: \n 1/ IP:PORT (1.1.1.1:9999)\n 2/ IP:PORT:ID:PASS (1.1.1.1:9999:username:password)".format(proxyS))
            #delete_from_txt("proxies.txt", proxyS)
            #os.system('taskkill /f /FI "WINDOWTITLE eq {}.py" /t'.format(monitor))    
            #os.system('start "{}.py" cmd /D /C "python {}.py && pause"'.format(monitor, monitor))
			    
        # Set up the proxy to be used        
        return proxies
    except Exception as err:
        print(err)
        pass
    # Return the proxy
    
def get_working_proxy(link, store, headers, zone):
    count = 1
    response = ""
    session = requests.Session()    
    proxyL = read()['proxy'][zone]
   
    flag = False
    while flag == False:
        if len(proxyL) == 0:  
            ra = ""
            proxy = ra
        else:
            ra = random.choice(proxyL)
            proxy = get_proxy(ra)
        try:           
            if store in ['gamestop', 'adidas', 'yeezy']:
                cs = cloudscraper.create_scraper()
               
                if proxy == ra:
                    response = cs.get(link)
                else:
                    response = cs.get(link, proxies = proxy)
            else:
                if proxy == ra:
                    response = session.get(link, headers = headers)
                else:
                    response = session.get(link, proxies = proxy, headers = headers)
        
            return response

        except Exception:                
            print("\nPROXY {} IS NOT WORKING ON  <{}>".format(ra, link))  
           
            if len(proxyL) > 0:                            
                ra = random.choice(proxyL)
                proxy = get_proxy(ra)
                print("GOT NEW PROXY {}\n".format(ra))
            else:
                ra = ""
                proxy = "" 
            count = count + 1
            if count > 5:
                flag = True


                
def add_to_db(product, start, monitor, zone):    
    # Mark instock and OOS         
    whook = read()
    end = time.time()
    hook = whook['webhooks'][monitor][zone]
    
    stock = str(product['status'])    
    # Create database
    conn = sqlite3.connect('supreme.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS {}(link TEXT UNIQUE, title TEXT, instock TEXT)""".format(product['store']))

    # Add product to database if it's unique
    try:        
        c.execute("""INSERT INTO {} (link, title, instock) VALUES (?, ?, ?)""".format(product['store']), (product['url'], product["title"], stock))

        print("Found new product <{}> <{}> ({}) IN {}s.".format(product["store"].upper(),product["title"],product['color'], str(round((end - start), 3))))        
        
        if 'sold out' not in product['status']:                              
            send_to_webhooks(product, 'NEW PRODUCT', hook, monitor)
        else:
            print('Product <{}> <{}> is OOS'.format(product['title'] + ' | ' + product['color'], product['status']))
    except Exception:       
        
        c.execute("SELECT * FROM {} WHERE link='%s'".format(product['store']) %(product["url"]))
        data = c.fetchall()       
        if stock != "sold out":            
            if data[0][2] == "sold out":
                c.execute("""UPDATE {} SET instock = ? WHERE link = ?""".format(product['store']), (product["status"], product["url"]),)
                print("<{}> <{}> is RESTOCKING Catched in {}s.".format(product["store"].upper(),product["title"] + ' | ' + product['color'], str(round((end - start), 3))))
        
                send_to_webhooks(product, 'RESTOCK', hook, monitor)
            elif (len(stock) > len(data[0][2]) ) and data[0][2] != "sold out":
                print("<{}> <{}> is RESTOCKING Catched in {}s.".format(product["store"].upper(),product["title"] + " | " + product['color'], str(round((end - start), 3))))
                c.execute("""UPDATE {} SET instock = ? WHERE link = ?""".format(product['store']), (str(product["status"]), str(product["url"])),)
               
                send_to_webhooks(product, 'RESTOCK', hook, monitor)
            else:
                print("Product <{}>  [{}] in <{}> ALREDY IN DATA".format(product["title"] + ' | ' + product['color'], product["title"], product['store'].upper()))
    
    # Close database
    conn.commit()
    c.close()
    conn.close()

    # Return whether or not it's a new product
    return product

def add_to_shopify_db(product, start, monitor, zone):    
    # Mark instock and OOS         
    hook = read()['webhooks'][monitor][product['store']]
    end = time.time()
    
    
    stock = str(product['stock'])    
    keywords = str(product['keywords'])
    # Create database
    conn = sqlite3.connect('shopify.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS {}(link TEXT UNIQUE, title TEXT, keywords TEXT, instock TEXT)""".format(product['store']))

    # Add product to database if it's unique
    try:        
        c.execute("""INSERT INTO {} (link, title, keywords, instock) VALUES (?, ?, ?, ?)""".format(product['store']), (product['url'],product["title"],  keywords, stock))

        print("Found new product <{}> <{}> ({}) IN {}s.".format(product["store"].upper(),product["title"],str(product['id']), str(round((end - start), 3))))        
        
        if len(product['stock']) != 0:      
                            
            send_to_webhooks(product, 'NEW PRODUCT', hook, monitor)
 
    except Exception:      
       
        c.execute("SELECT * FROM {} WHERE link='%s'".format(product['store']) %(product["url"]))
        data = c.fetchall() 
      
        #print(data[0][3])
        '''
        for s in [']', '[', ',', "'"]:
            data = data.replace(s, '')
        for q in range(len(product['stock'])):
        '''
        if str(product['stock']) != data[0][3]:           
            c.execute("""UPDATE {} SET instock = ? WHERE link = ?""".format(product['store']), (product["stock"], product["url"]),)
            print("<{}> <{}> is RESTOCKING Catched in {}s.".format(product["store"].upper(),product["title"] + ' | ' + product['url'], str(round((end - start), 3))))
            send_to_webhooks(product, 'RESTOCK', hook, monitor)
        else:
            print("Product <{}>  [{}] in <{}> ALREDY IN DATA".format(product["title"] + ' | ' + product['id'], product["url"], product['store'].upper()))
        #compare by len
       
    # Close database
    conn.commit()
    c.close()
    conn.close()

    # Return whether or not it's a new product
    return product