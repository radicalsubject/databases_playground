
from lxml import html
import traceback
from fake_useragent import UserAgent
from requests_html import HTMLSession, AsyncHTMLSession
import random
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import asyncio, threading
# def main():

async def scrape(query):

	# proxies = [{'http':'193.9.158.30:8085','https':'193.9.158.30:8085'},{'http':'46.161.62.121:8085','https':'46.161.62.121:8085'}]

	proxies = []

	ua = UserAgent()

	session = AsyncHTMLSession()

# asession = AsyncHTMLSession()
# r = await asession.get(API)
# await r.html.arender()
# resp=r.html.raw_html

	headers = {'User-Agent':ua.random,'Host':'google.com','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7','Cache-Control': 'no-cache','Connection': 'keep-alive','Upgrade-Insecure-Requests':'1'}

	# catalog_number = input('Введите каталожный номер:')
	catalog_number = query

	print('Пожалуйста, ожидайте...')

	try:

		warnings.simplefilter('ignore')

		if proxies:

			proxy = random.choice(proxies)


			r = await session.get('https://www.alfa.com/en/catalog/'+catalog_number+'/',headers=headers,verify=False,proxies={'http': 'http://'+proxy['http']},timeout=20)

			

		else:

			r = await session.get('https://www.alfa.com/en/catalog/'+catalog_number+'/',headers=headers,verify=False,timeout=20)


		await r.html.arender(timeout=10)

		js = r.html.html

		tree = html.fromstring(js)

		price = tree.xpath('//tr[@class="item-row"]/td/text()')

		weight = tree.xpath('//tr[@class="item-row"]/td/text()')

		sku = tree.xpath('//tr[@class="item-row"]/td/text()')
		print(tree)

		if (price and sku and weight):

			print ('{0:15} | {1:15}'.format('Pack Size','Price (EUR)'))
			print ('{0:15} | {1:15}'.format(sku[1], price[2]))
			return '{0:15} | {1:15}'.format(sku[1], price[2])

		else:

			print('Нет информации для этого каталожного номера...')

	except Exception as e:

		print(e)

		# continue


# if __name__ == "__main__":
# 	main()
