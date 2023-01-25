import requests, os, sys, discord, time, datetime
from discord.utils import get
import json
from log import read, write
from collections import defaultdict



TOKEN = 'NjYxMzUxMjc3MDk1Mjg4ODQ1.XgqJXw.a344R2t7j6mCMLVaDvwanY4Pmd4'
#test TOKEN = 'NjYxMzUxMjc3MDk1Mjg4ODQ1.XqoJ9Q.8S-stUn4sjj81f5Ay7zqxcB2Qzg'
#haru token: 'NjYyNzQyNTIyNzc4NDg0NzQ3.Xq4H_w.xEUQlM2MyckCEltvSR_c7UHHi1I'
#discord bot token
client = discord.Client()
digit_keyword_store = ['walmart', 'bestbuy', 'target', 'gamestop']
class Webhook:
	def __init__(self, url, **kwargs):

		"""
		Initialise a Webhook Embed Object
		"""

		self.url = url 
		self.msg = kwargs.get('msg')
		self.color = kwargs.get('color')
		self.title = kwargs.get('title')
		self.title_url = kwargs.get('title_url')
		self.author = kwargs.get('author')
		self.author_icon = kwargs.get('author_icon')
		self.author_url = kwargs.get('author_url')
		self.desc = kwargs.get('desc')
		self.fields = kwargs.get('fields', [])
		self.image = kwargs.get('image')
		self.thumbnail = kwargs.get('thumbnail')
		self.footer = kwargs.get('footer')
		self.footer_icon = kwargs.get('footer_icon')
		self.ts = kwargs.get('ts')


	def add_field(self,**kwargs):
		'''Adds a field to `self.fields`'''
		name = kwargs.get('name')
		value = kwargs.get('value')
		inline = kwargs.get('inline', False)

		field = { 

		'name' : name,
		'value' : value,
		'inline' : inline

		}

		self.fields.append(field)

	def set_desc(self,desc):
		self.desc = desc

	def set_author(self, **kwargs):
		self.author = kwargs.get('name')
		self.author_icon = kwargs.get('icon')
		self.author_url = kwargs.get('url')

	def set_title(self, **kwargs):
		self.title = kwargs.get('title')
		self.title_url = kwargs.get('url')

	def set_thumbnail(self, url):
		self.thumbnail = url

	def set_image(self, url):
		self.image = url

	def set_footer(self,**kwargs):
		self.footer = kwargs.get('text')
		self.footer_icon = kwargs.get('icon')
		ts = kwargs.get('ts')
		if ts == True:
			self.ts = str(datetime.datetime.utcfromtimestamp(time.time()))
		else:
			self.ts = str(datetime.datetime.utcfromtimestamp(ts))


	def del_field(self, index):
		self.fields.pop(index)

	@property
	def json(self,*arg):
		'''
		Formats the data into a payload
		'''
		data = {}
		data["embeds"] = []
		embed = defaultdict(dict)
		if self.msg: data["content"] = self.msg
		if self.author: embed["author"]["name"] = self.author
		if self.author_icon: embed["author"]["icon_url"] = self.author_icon
		if self.author_url: embed["author"]["url"] = self.author_url
		if self.color: embed["color"] = self.color 
		if self.desc: embed["description"] = self.desc 
		if self.title: embed["title"] = self.title 
		if self.title_url: embed["url"] = self.title_url 
		if self.image: embed["image"]['url'] = self.image
		if self.thumbnail: embed["thumbnail"]['url'] = self.thumbnail
		if self.footer: embed["footer"]['text'] = self.footer
		if self.footer_icon: embed['footer']['icon_url'] = self.footer_icon
		if self.ts: embed["timestamp"] = self.ts 

		if self.fields:
			embed["fields"] = []
			for field in self.fields:
				f = {}
				f["name"] = field['name']
				f["value"] = field['value']
				f["inline"] = field['inline'] 
				embed["fields"].append(f)

		data["embeds"].append(dict(embed))

		empty = all(not d for d in data["embeds"])

		if empty and 'content' not in data:
			print('You cant post an empty payload.')
		if empty: data['embeds'] = []

		return json.dumps(data, indent=4)
	def post(self):
		"""
		Send the JSON formated object to the specified `self.url`.
		"""

		headers = {'Content-Type': 'application/json'}

		result = requests.post(self.url, data=self.json, headers=headers, timeout=10, verify=False)

async def show(msg, content, info):
	if content[1]  == 'proxy':
		
		if len(content) >= 3:
			try:
				await msg.channel.send(info['proxy'][content[2]])
			except Exception:
				await msg.channel.send("Format: ::show proxy [zone]\n<ex> ::show proxy us\nBasic proxy zone:{}".format(info['proxy'].keys()))
		else:
			await msg.channel.send(info['proxy'])
	elif content[1]  == 'keywords':		
		if len(content) >= 3:
			try:
				await msg.channel.send(info['keywords'][content[2]])
			except Exception:
				await msg.channel.send("Format: ::show keywords [store]\n<ex> ::show keywords supreme\nBasic proxy zone:{}".format(info['keywords'].keys()))
		else:
			await msg.channel.send(info['keywords'])
	elif content[1] in ['delay', 'users', 'channels']:
		await msg.channel.send('{} : {}'.format(content[1].upper(), info[content[1]]))
	return 0

async def add(msg, content, info):
	if content[1] == 'proxy':
		try:
			if len(content) > 4:
				for x in content[3:]:
					info['proxy'][content[2]].append(x)
				write(info)
				await msg.channel.send("Success add {} to proxy list".format(content[3:]))					
			elif len(content) == 4:
				info['proxy'][content[2]].append(content[3])
				write(info)
				await msg.channel.send("Success add {} to proxy list".format(content[3:]))					
			
		except Exception:
			await msg.channel.send("Please input right format. ::add proxy zone [proxy(es)]\n<EX> ::add proxy us 1:1:1:1\n::add proxy eu 1:1:1:1 2:2:2:2 3:3:3:3")					
			
	elif content[1].lower() in ['keywords', 'users', 'channels']:			
		try:						
			if content[1] == 'keywords':    				
				if (content[2] in digit_keyword_store) and (content[3].isdigit()):
					if len(content) >=5:
						for x in content[3:]:
							info['keywords'][content[2]].append(x)
						write(info)
					else:	
						info['keywords'][content[2]].append(content[3])				
						write(info)
					
				else:
					info['keywords'][content[2]].append(content[3:])	
					write(info)
				await msg.channel.send("Success add {} to {} list".format(content[3].lower(),content[1]))
			else:
				info[content[1]].append(content[2])					
				write(info)
				await msg.channel.send("Success add {} to {} list".format(content[2],content[1]))					
				
		except Exception:
			await msg.channel.send("PLEASE ENTER RIGHT FORMAT. ::add ['keywords', 'users', 'channels'] {}".format([info['keywords'].keys()]))
	return 0


async def deleteall(msg, content, info):
	if len(content) >= 2:
		a = list(info['keywords'].keys()) + list(info['proxy'].keys())

		if (content[1] in ['keywords', 'proxy']) and (content[2] in (a)):
			info[content[1]][content[2]] = []
			write(info)
			await msg.channel.send("Success delete  all keywords from {} list".format(content[2]))
	
		else:
			await msg.channel.send("PLEASE ENTER RIGHT FORMAT.\n::deleteall [keywords, proxy] {}".format(a))
			
	return 0

async def delete(msg, content, info):
	try:		
		if len(content) >= 3:			
			if (content[1] == 'proxy') and (content[2] in ['us', 'eu', 'jp']) :
				
				if content[3] in info['proxy'][content[2]]:
					info['proxy'][content[2]].remove(content[3])
					write(info)
				await msg.channel.send('SUCCESS DELETE {} IN {}'.format(content[3], content[2]))
			elif (content[1] == 'keywords') and (content[2] in info['keywords'].keys()):
				if (content[2] not in digit_keyword_store) and (content[3:] in info['keywords'][content[2]]):
					info['keywords'][content[2]].remove(content[3:])
					write(info)
				elif (content[2] in digit_keyword_store) and (content[3] in info['keywords'][content[2]]):
					info['keywords'][content[2]].remove(content[3])
					write(info)
				await msg.channel.send('SUCCESS DELETE {} IN {}'.format(content[3].upper(), content[2].upper()))
			elif (content[1] in ['users', 'channels']) and (content[2] in info[content[1]]):
				info[content[1]].remove(content[2])
				write(info)
				await msg.channel.send('SUCCESS DELETE {} IN {}'.format(content[2].upper(), content[1].upper()))
			else:
				await msg.channel.send("CAN'T FIND {} IN {} LIST".format(content[2].upper(), content[1].upper()))
			
	except Exception as err:
		print(err)
		await msg.channel.send("Please enter right format.\n\n::delete proxy [us, eu, jp] [item]\n\n::delete [users, channels] [item]\n\n::delete keywords {} [item]".format(list(info['keywords'].keys())))			
	
	return 0

async def total(msg, content, info):
	if content[1] in ['users', 'channels']:
		await msg.channel.send("Total {} : {}".format(content[1], len(info[content[1]])))
	elif content[1] == 'proxy' and content[2] in ['us', 'eu', 'jp']:
		await msg.channel.send("Total {} : {}".format(content[2], len(info['proxy'][content[2]])))	
	elif content[1] == 'keywords' and content[2] in list(info['keywords'].keys()):
		await msg.channel.send("Total {} : {}".format(content[2],len(info['keywords'][content[2]])))	
	else:
		await msg.channel.send("PLEASE ENTER RIGHT FORMAT\n::total [user, channels]\n\n::total keywords {}\n\n::total proxy [us, eu, jp]".format(list(info['keywords'].keys())))	

	return 0
async def bot_command(msg, content, info):	

	dc = [i for i in info['keywords'].keys()]
	dc.append('proxy')		
	
	try:	
		if len(content) > 1:	
			if content[0] == '::add':
				await add(msg, content, info)				
			elif content[0]  == '::changedelay':
				if content[1].isdigit():
					info['delay'] = content[1]
					write(info)
					await msg.channel.send("SUCCESS SET DELAY TO {}".format(content[1]))
				else:
					await msg.channel.send("PLEASE ENTER NUMBER")
			elif content[0] == '::total':
				await total(msg, content, info)
			elif content[0]  =='::show':
				await show(msg, content, info)		
			elif content[0]  == '::delete':			
				await delete(msg,content,info)
			elif content[0] == '::deleteall':
				await deleteall(msg,content,info)
			elif content[0]  == '::start':			
				await main(0, msg, content[1])			
			elif content[0]  == '::stop':	
				await main(1, msg, content[1])
			
		elif len(content) == 1:					
			if content[0]  == '::help':
				a = 'List of command \n		::add [keyword] [zone] [content]\n    ::show [keyword] [store] [content]\n    ::delete [keyword, proxy] [zone, store] [content]\n\n	::delete [users, channels] [content]\n	::deleteall [keywords, proxy] [store, zone]\n	::changedelay [number]\n    ::start [monitor-name]\n	::stop [monitor-name]    <ex> ::stop tech\n	::help \n\nData files: \n		infor\n	proxies\nMonitors keywords:\n	supreme\n	supremef\n	tech\n	nike\nExample:\n		::add SupremeUS air force  \n    (for add keyword to nike monitor)\n DONT FORGET RESET MONITOR AFTER EACH CHANGE'
				await msg.channel.send(a)		
			elif content[0] == '::running':
				await main(2, msg, content[0])		
	except Exception as err:
		if KeyError:			
			await msg.channel.send("PLEASE ENTER RIGHT KEYWORD \n {}".format(dc))		  
		print(err)			
	return 0



''' --------------------------------- RUN --------------------------------- '''

async def main(flag, msg, cont):	
	if(__name__ == "__main__"):
		# Ignore insecure messages
		#requests.packages.urllib3.disable_warnings()
		try:
			if flag == 0:    			
				b = os.system('start "{}.py" cmd /D /C "python {}.py && pause"'.format(cont, cont))
				await msg.channel.send("Starting {} monitor. Please wait 3s for checking status".format(cont))  
				time.sleep(3)
				if len(os.popen('tasklist /FI "WINDOWTITLE eq {}.py"'.format(cont,)).read().strip().split('\n')) >= 2:
					await msg.channel.send("Monitor Started")     
				else:
					await msg.channel.send("Can't start the monitor {}".format(cont))   		
			elif flag == 1:								
				if len(os.popen('tasklist /FI "WINDOWTITLE eq {}.py"'.format(cont)).read().strip().split('\n')) >= 2:
					os.system('taskkill /f /FI "WINDOWTITLE eq {}.py" /t'.format(cont))	
					await msg.channel.send("Stopped {} monitors".format(cont))	
				else:
					await msg.channel.send("Can't find the monitor {}".format(cont))			
			elif flag == 2:
				a = {'supremef' : 'False',
					 'supreme' : 'False',
					 'tech' : 'False',
					 'nike' : 'False',
					 'shopify' : 'False',
					}
				s = ''
				for i in a.keys():				
					
					if len(os.popen('tasklist /FI "WINDOWTITLE eq {}.py"'.format(i)).read().strip().split('\n')) >= 2:						
						a[i] = 'True'				
					else:
						a[i] = 'False'
					s = s + '{} : {}\n'.format(i, a[i])
				await msg.channel.send(s)
		except Exception as err:   			     
			print(err)
			await msg.channel.send("Something Wrong, {} \n TELL KIMO FIX IT".format(err))

@client.event
async def on_read():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('--------')


@client.event
async def on_message(message):
	info = read()
	
	content = message.content.split()	
	if(str(message.channel.id) in info['channels']) or (str(message.author) in info['users']):
		if message.author.bot == False:
			print('{} <{}> <{}> | {}'.format(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),str(message.channel),str(message.author),str(message.content)))
		
			await bot_command(message, content, info)
client.run(TOKEN)