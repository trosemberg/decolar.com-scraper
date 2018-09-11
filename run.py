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


def find_html_preco_final(passagem,browser):
	browser.visit(passagem.get_url())
	tamanho = 0
	while tamanho < 10:
		try:
			passagem.set_price(browser.find_by_css('.item-fare.fare-price'))
		except:
			pass
		tamanho = len(passagem.price)
	print("Foram encontradas {} Passagens de {from} para {to} de {from_d}" \
		"".format(tamanho,**passagem.info))
	print("Seus valores são de:")


def find_preco_final(passagem,browser,pesquisa,df):
	i = -1
	while (i<9):
		i=i+1
		try:
			preco = passagem.price[i].find_by_css('.amount.price-amount')
			if (i==0):
				print("\033[0;32m" + preco.first.html + "\033[0;0m", end = " ")
			else:
				print(preco.first.html, end = " ")
			passagem.set_preco(preco.first.html)
			df.loc[df.shape[0]] = [passagem.info['from'],passagem.info['to'],passagem.preco,pesquisa.week_day]\
				+[pesquisa.day,pesquisa.part_of_day,passagem.info['from_d']]
		except:
			passagem.set_price(browser.find_by_css('.item-fare.fare-price'))
			i= i-1
	print("\n\n")


def read_links():
	df = pd.read_csv("Dados.csv")
	with Browser('chrome', headless=True,incognito=True) as browser:
		browser.driver.set_window_size(1000, 600)
		with open("pages.csv","r") as pesquisa,open('Dados.csv',):
			print("Pesquisa de preço realizada em: " + strftime('%c'))
			for url in pesquisa:
				pesquisa = Pesquisa()
				pesquisa.set_week_day(strftime('%a'))
				pesquisa.set_part_of_day(strftime('%H'))
				pesquisa.set_day(strftime('%x'))
				passagem = Passagens()
				passagem.set_url_and_info(url)
				find_html_preco_final(passagem,browser)
				find_preco_final(passagem,browser,pesquisa,df)
	df.to_csv('Dados.csv', index= False)

if __name__ == '__main__':
	read_links()