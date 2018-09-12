class Passagens:
	def __init__(self):
		self.price = ''
		self.url = ''
		self.info = {}
		self.cluster = []
		self.preco = ''
		self.comp = ''

	def set_preco(self,preco):
		self.preco = preco
		if '.' in preco:
			preco = preco.split('.')
			self.preco = preco[0]+preco[1]


	def set_url_and_info(self,url):
		self.url = url
		itin = url.split("/")
		self.info['from'] = itin[7]
		self.info['to'] = itin[8]
		self.info['from_d'] = itin[9]

	def get_url(self):
		return self.url

	def set_price(self,price):
		self.price = price

	def set_cluster(self,cluster):
		self.cluster = cluster

	def set_comp(self,comp):
		self.comp = comp



class Pesquisa:
	def __init__(self):
		self.day = ''
		self.week_day = ''
		self.part_of_day = ''

	def set_part_of_day(self,pod):
		hora = int(pod)
		if hora>18:
			self.part_of_day = 'noite'
		elif hora<6:
			self.part_of_day = 'madrugada'
		elif hora<12:
			self.part_of_day = 'manha'
		else:
			self.part_of_day = 'tarde'

	def set_week_day(self,wd):
		self.week_day = wd

	def set_day(self,day):
		self.day = day
