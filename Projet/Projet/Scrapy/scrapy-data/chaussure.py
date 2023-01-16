import pymongo
import scrapy
#from scrapy.exceptions import DropItem

class ChaussureSpider(scrapy.Spider):
    name = "chaussure"

    custom_settings = {
        "USER_AGENT": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',

    }


    def start_requests(self):
        # Connect to MongoDB
        client = pymongo.MongoClient(host='mongodb',
                        port=27017, 
                        username='root', 
                        password='root',
                        authSource="admin")

        db = client["db"]
        db.collectiona.drop()
        #db.collectionb.drop()
        collection1 = db["collectiona"]
        #collection2 = db["collectionb"]
        

        # Scrape data from site 1
        for i in range(0,241,24):
            url1 = f'https://www.courir.com/fr/c/femme/chaussures/?start={i}&sz=24'
            yield scrapy.Request(url=url1, callback=self.parse_site1, meta={"collection": collection1})

        # Scrape data from site 2
        for i in range(0,28,1):
            url2 = f'https://www.footlocker.fr/fr/category/femme/chaussures.html?currentPage={i}'
            yield scrapy.Request(url=url2, callback=self.parse_site2, meta={"collection": collection1})


    def parse_site1(self, response):
        collection = response.meta["collection"]

        chaussures = response.xpath('//*[@class="product__tile js-product-tile"]/div/div[2]')
        for chaussure in chaussures:
            marque = chaussure.xpath('./div[1]/h2/span[1]/text()').get()
            nom = chaussure.xpath('./div[1]/h2/span[2]/text()').get()
            prix = chaussure.xpath('./div[2]/div[2]/span[1]/text()').get()
            site = 'Courir'
            lien = response.url  

            data = {
                'nom': nom,
                'prix' : prix,
                'site': site,
                'lien': lien
            }

            if prix:
                data['prix'] = prix = prix.lstrip("\u20ac\u00a0")
                data['prix'] = prix = prix.rstrip("\u20ac")
                data['prix'] = float(data['prix'].replace(",", "."))

                 # Insert data into MongoDB
                collection.insert_one(data)
                #yield data
                
            else:
               del data 
           
           

    def parse_site2(self, response):
        collection = response.meta["collection"]

        chaussures = response.xpath('//*[@id="main"]/div/div[2]/div/div[2]/div/div[2]/ul[1]/li/div[@class="ProductCard"]')
        for chaussure in chaussures:
            r = response.url
            lien = f"{r}{chaussure.xpath('./a/@href').extract_first()}"
            nom = chaussure.xpath('./a/span/span/text()').get()
            nom = nom.upper()
            prix = chaussure.xpath('./a/span[3]/span/text()').get()
            site = 'Footlocker'
            data = {
                'nom': nom,
                'prix' : prix,
                'site': site,
                'lien': lien
            }

            if prix:
                data['prix'] = prix = prix.lstrip("\u20ac\u00a0")
                data['prix'] = prix = prix.rstrip("\u20ac")
                data['prix'] = float(data['prix'].replace(",", "."))

                 # Insert data into MongoDB
                collection.insert_one(data)
                #yield data
            
            else:
               del data 

           

