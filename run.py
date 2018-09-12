import numpy as np
import pandas as pd
import os
import csv
from passagem_scraper import Passagens,Pesquisa
from time import strftime,sleep
from splinter import Browser

"""
	Pega os links para fazer o scrape do preço das 10 passagens mais baratas determinada
por um link do decolar.com . A partir disso, utiliza o Splynter para acessar o link,
deste link se retira todo o HTML fonte da parte a qual possui a class "Preço Final"
dentro deste vetor de 10 elementos onde tem "Preço Final", se itera este vetor loca-
lizando o valor deste preço.
"""
def find_html_cluster(passagem,browser):
	print('in find_html_cluster')
	browser.visit(passagem.get_url())
	flag = False
	while flag == False:
		try:
			for i in range(0,10):
				passagem.set_cluster(browser.find_by_css('.cluster-wrapper'))
				temp = passagem.cluster[i].find_by_css('.item-fare.fare-price')
				temp = temp.find_by_css('.amount.price-amount').first.html
				temp = passagem.cluster[i].find_by_css('.name').first.html
			flag = True
		except:
			pass

def find_preco_final(passagem,browser,pesquisa,df):
	print('in find preco final\n')
	for i in range(0,10):
		passagem.set_price(passagem.cluster[i].find_by_css('.item-fare.fare-price'))
		passagem.set_comp(passagem.cluster[i].find_by_css('.name').first.html)
		passagem.set_preco(passagem.price.find_by_css('.amount.price-amount').first.html)
		df.loc[df.shape[0]] = [passagem.info['from'],passagem.info['to'],passagem.preco,pesquisa.week_day]\
			+[pesquisa.day,pesquisa.part_of_day,passagem.info['from_d'],passagem.comp]


def read_links():
	df = pd.read_csv("Dados.csv")
	with Browser('chrome', headless=True,incognito=True) as browser:
		browser.driver.set_window_size(1000, 600)
		with open("pages.csv","r") as pesquisa,open('Dados.csv',):
			print("Pesquisa de preço realizada em: " + strftime('%c'))
			j = 0
			for url in pesquisa:
				j = j+1
				print('{}º LINK de 50'.format(j))
				pesquisa = Pesquisa()
				pesquisa.set_week_day(strftime('%a'))
				pesquisa.set_part_of_day(strftime('%H'))
				pesquisa.set_day(strftime('%x'))
				passagem = Passagens()
				passagem.set_url_and_info(url)
				find_html_cluster(passagem,browser)
				find_preco_final(passagem,browser,pesquisa,df)
	df.to_csv('Dados.csv', index= False)

if __name__ == '__main__':
	read_links()