 
import pickle, os, json
import psutil
from log import read, write 
a = {'keywords':{"bestbuy": ["2588445", "6364255", "6342915", "9928354", "6366565", "6321794", "6366565", "6257148", "6364253", "4612476", "6342914", "6343150", "5579380", "6401728"], 
                "walmart": ["047875882294", "815820020271"],
                "gamestop": ["11095774", "10101864", "11100847"],
                "target": ["52161278", "78452829"],
                "supreme": [["logo"], ["Military", "Coat"], ["box", "logo", "blue"], ["box", "logo"], ["air", "force", "1"], ["force"]], 
                'shopify' : [],
                'nike':[['nike'], ['air', 'max'], ['kd13'], ['jordan']]
                },
    'webhooks' : {
                    'tech':{
                            'walmart' : ['https://discordapp.com/api/webhooks/701276545624440832/MS9v_lNscJeRyHvjeLa4ewt0Y_mskhSQYuNl-BDIXSKPChQG1YALJC92PVynK-V6gCFZ'],
                            'bestbuy' : ['https://discordapp.com/api/webhooks/701276375906254848/PJRXlf985ILXojHU4ynlsA7ao4AopK5BWxY8zekyEQ3MU-EaOEIeebnkc1CqG5CJHCLk'],
                            'target' : ['https://discordapp.com/api/webhooks/701276456944402522/WOPVidyHpciWqYFvBB3a-LsOdzXHOPo-Tc9kqYaHWMC9Ck-Ql0UAEWRMjd4_mKFNwsqN'],
                            'gamestop' : ['https://discordapp.com/api/webhooks/701276603983986739/0EMVgtVGGdB6A7cxh4XzsTgnajeoku5nTnfU9cichX5Oheh-_0p6fTBYibeqk-OtC7vF']
                    },
                    'supreme':{
                        'us':['https://discordapp.com/api/webhooks/707054778135609364/JpBZgpvSZ_jS9rWFuG2IsbE1XTkySpQZARRFhCHC8gchusrH8SzBEv7cZb4YlFbvq2Tl'],
                        'eu':[],
                        'jp':[]
                    },
                    'supremef':{
                        'us':['https://discordapp.com/api/webhooks/706292681319645187/h9--KLSntntIXj_wOPQsaw3SCyk8cQfWZj75Y7ybRu-hyVMcCUcncpjYu3okzqhbs5rn'],
                        'eu':[],
                        'jp':[]
                    },
                    'nike':{
                        'us':['https://discordapp.com/api/webhooks/704824749783515307/z11mqmaRUM4jAmsf3EmPYSI0NJtPyxFmLpm8cFhVjWwc-LoOjryG7S29LWTFi3WultJE'],
                        'eu':[],
                        'jp':[]
                    },
                    'shopify':{
                        'undefeated':['https://discordapp.com/api/webhooks/657628294715277360/KHuW9IDzsKklykGKzR7nde4U9WNIRcQ__s84Jr31VxcdQqL4i9TKD05VRZq2iZfl7GPc'],
                        'kith' : ['https://discordapp.com/api/webhooks/662744754488082463/Btz2kB4s69K07XKDtTX0cZnbADKdbtGQGcSGVtln43jikvhACER0KXI20MtcmgGaqLN9']
                    },
                    'shopifyf':{

                    }
                    },
    'proxy':{
                        'us': ['154.21.52.204:1337:tfgqqrk:rhgmt',
                '154.21.53.37:1337:tfgqqrk:rhgmt',
                '154.21.50.206:1337:tfgqqrk:rhgmt',
                '154.21.54.19:1337:tfgqqrk:rhgmt',
                '154.21.51.162:1337:tfgqqrk:rhgmt',
                '154.21.52.232:1337:tfgqqrk:rhgmt'],
                        'jp':['154.21.52.204:1337:tfgqqrk:rhgmt',
                '154.21.53.37:1337:tfgqqrk:rhgmt',
                '154.21.50.206:1337:tfgqqrk:rhgmt',
                '154.21.54.19:1337:tfgqqrk:rhgmt',
                '154.21.51.162:1337:tfgqqrk:rhgmt',
                '154.21.52.232:1337:tfgqqrk:rhgmt'],
                        'eu':[],
                    },
       
    "delay": "2",
    "users" :['Kimochi#8538', 'Bonn#2000', 'dean#0001'],
    "channels" : ['630472520528822272']}
'''
Tree:
dict: webhooks ==> monitors => zone
      keyword  ==> stores
      proxy    ==> zone
      delay    ==> number
'''

write(a)
b = read()
print(b)
print(b['proxy']['us'])
print(len(b['proxy']['us']))


