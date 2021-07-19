import requests


class Lot:
	def __init__(self, parcel_id: str, street_number: str, street_name: str):
		self.parcel_id = parcel_id
		self.street_number = street_number
		self.street_name = street_name

	def getAddressStr(self) -> str:
		return str(self.street_number) + ' ' + self.street_name

	def __str__(self):
		return self.getAddressStr() + ' | ' + self.parcel_id


# get every lot in the city
def searchTotalValue(min: str, max: str = '', allowDuplicates=True):
	"""
	Searches http://revere.patriotproperties.com/default.asp by street name

	:param query: Search string
	:param allowDuplicates: choose to allow or disallow returning duplicates
	:return: list of Lot objects
	"""

	lots = []

	url = 'http://revere.patriotproperties.com/SearchResults.asp?SearchParcel=&SearchBuildingType=&SearchLotSize=&SearchLotSizeThru=&SearchTotalValue=' + min + '&SearchTotalValueThru=' + max + '&SearchOwner=&SearchYearBuilt=&SearchYearBuiltThru=&SearchFinSize=&SearchFinSizeThru=&SearchSalePrice=&SearchSalePriceThru=&SearchStreetName=&SearchBedrooms=&SearchBedroomsThru=&SearchNeighborhood=&SearchNBHDescription=&SearchSaleDate=&SearchSaleDateThru=&SearchStreetNumber=&SearchBathrooms=&SearchBathroomsThru=&SearchLUC=&SearchLUCDescription=&SearchBook=&SearchPage=&SearchSubmitted=yes&cmdGo=Go'

	response = None

	while True:
		try:
			response = requests.post(url)
		except requests.exceptions.ConnectionError:
			continue
		break

	cookie = response.cookies.get_dict()
	response_text = response.text

	pages = 1

	multiple_pages = response_text.find('Next Page') != -1
	if multiple_pages:
		start_pages_amount = response_text.find('>Print page')
		start_page_number = response_text.find('of ', start_pages_amount)
		end_pages_amount = response_text.find('<', start_pages_amount)
		pages = int(response_text[start_page_number + 3:end_pages_amount])

	print('Pages: ' + str(pages))

	page_numbers = range(1, pages + 1)

	current_page_number = 0

	street_numbers = []
	while True:
		try:
			page_number = page_numbers[current_page_number]
		except IndexError:
			break

		if page_number == 1:
			url = 'http://revere.patriotproperties.com/SearchResults.asp?SearchParcel=&SearchBuildingType=&SearchLotSize=&SearchLotSizeThru=&SearchTotalValue=' + str(
				min) + '&SearchTotalValueThru=' + str(
				max) + '&SearchOwner=&SearchYearBuilt=&SearchYearBuiltThru=&SearchFinSize=&SearchFinSizeThru=&SearchSalePrice=&SearchSalePriceThru=&SearchStreetName=&SearchBedrooms=&SearchBedroomsThru=&SearchNeighborhood=&SearchNBHDescription=&SearchSaleDate=&SearchSaleDateThru=&SearchStreetNumber=&SearchBathrooms=&SearchBathroomsThru=&SearchLUC=&SearchLUCDescription=&SearchBook=&SearchPage=&SearchSubmitted=yes&cmdGo=Go'

			print('Loading page ' + str(page_number))

			try:
				response = requests.post(url, timeout=5)
			except requests.exceptions.ConnectionError:
				print('Timed out reloading ' + str(page_number))
				continue

			current_page_number += 1
			page_text = response.text
		else:
			url = 'http://revere.patriotproperties.com/SearchResults.asp?page=' + str(page_number)
			print('Loading page ' + str(page_number))
			cookie_str = ''
			try:
				cookie_str = 'ASPSESSIONIDCASCQSQR=' + cookie['ASPSESSIONIDCASCQSQR']

			except KeyError:
				pass

			headers = {
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'en-US,en;q=0.9',
				'Connection': 'keep-alive',
				'Cookie': cookie_str,
				'DNT': '1',
				'Host': 'revere.patriotproperties.com',
				'Referer': 'http://revere.patriotproperties.com/SearchResults.asp?page=' + str(page_number - 1),
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
			}

			# print('Cookie: ' + str(cookie))
			# print('Header cookie: ' + cookie_str + ';')
			try:
				page = requests.get(url, timeout=5, headers=headers)
			except requests.exceptions.ConnectTimeout:
				print('Timed out. Reloading ' + str(page_number))
				continue

			current_page_number += 1
			cookie = cookie
			page_text = page.text

		next_idx = 0
		lot_available = page_text.find('?AccountNumber', next_idx) != -1

		while lot_available:
			account_idx = page_text.find('?AccountNumber', next_idx)

			parcel_idx = page_text.find('>', account_idx)
			end_idx = page_text.find('<', parcel_idx)

			street_number_idx = page_text.find('<TD>', end_idx)
			end_street_number_idx = page_text.find('&', street_number_idx)

			start_street_name = page_text.find('bottom">', end_street_number_idx)
			end_street_name = page_text.find('</A', start_street_name)

			parcel_id = page_text[parcel_idx + 1:end_idx]
			street_number = page_text[street_number_idx + 4:end_street_number_idx]
			street_name = page_text[start_street_name + 8:end_street_name]

			appending_lot = Lot(parcel_id, street_number, street_name)
			# print('\t' + appending_lot.__str__())
			# print(appending_lot.__str__())
			if not allowDuplicates:
				if street_number not in street_numbers:
					lots.append(appending_lot)
					street_numbers.append(street_number)
			else:
				lots.append(appending_lot)

			next_idx = end_street_name
			lot_available = page_text.find('?AccountNumber', next_idx) != -1

	print('Loaded ' + str(len(lots)) + ' lots')
	return lots


def searchAddresses(query: str, allowDuplicates=True) -> list[Lot]:
	"""
	Searches http://revere.patriotproperties.com/default.asp by street name

	:param query: Search string
	:param allowDuplicates: choose to allow or disallow returning duplicates
	:return: list of Lot objects
	"""

	lots = []

	url = 'http://revere.patriotproperties.com/SearchResults.asp?SearchParcel=&SearchBuildingType=&SearchLotSize=&SearchLotSizeThru=&SearchTotalValue=&SearchTotalValueThru=&SearchOwner=&SearchYearBuilt=&SearchYearBuiltThru=&SearchFinSize=&SearchFinSizeThru=&SearchSalePrice=&SearchSalePriceThru=&SearchStreetName=' + query + '&SearchBedrooms=&SearchBedroomsThru=&SearchNeighborhood=&SearchNBHDescription=&SearchSaleDate=&SearchSaleDateThru=&SearchStreetNumber=&SearchBathrooms=&SearchBathroomsThru=&SearchLUC=&SearchLUCDescription=&SearchBook=&SearchPage=&SearchSubmitted=yes'

	response = None

	while True:
		try:
			response = requests.post(url)
		except requests.exceptions.ConnectionError:
			continue
		break

	cookie = response.cookies.get_dict()
	response_text = response.text

	pages = 1

	multiple_pages = response_text.find('Next Page') != -1
	if multiple_pages:
		start_pages_amount = response_text.find('>Print page')
		start_page_number = response_text.find('of ', start_pages_amount)
		end_pages_amount = response_text.find('<', start_pages_amount)
		pages = int(response_text[start_page_number + 3:end_pages_amount])

	print('Pages: ' + str(pages))

	page_numbers = range(1, pages + 1)

	current_page_number = 0

	street_numbers = []
	while True:
		try:
			page_number = page_numbers[current_page_number]
		except IndexError:
			break

		if page_number == 1:
			url = 'http://revere.patriotproperties.com/SearchResults.asp?SearchParcel=&SearchBuildingType=&SearchLotSize=&SearchLotSizeThru=&SearchTotalValue=&SearchTotalValueThru=&SearchOwner=&SearchYearBuilt=&SearchYearBuiltThru=&SearchFinSize=&SearchFinSizeThru=&SearchSalePrice=&SearchSalePriceThru=&SearchStreetName=' + query + '&SearchBedrooms=&SearchBedroomsThru=&SearchNeighborhood=&SearchNBHDescription=&SearchSaleDate=&SearchSaleDateThru=&SearchStreetNumber=&SearchBathrooms=&SearchBathroomsThru=&SearchLUC=&SearchLUCDescription=&SearchBook=&SearchPage=&SearchSubmitted=yes'
			print('Loading ' + query + ' page ' + str(page_number))

			try:
				response = requests.post(url, timeout=5)
			except requests.exceptions.ConnectionError:
				print('Timed out reloading ' + str(page_number))
				continue

			current_page_number += 1
			page_text = response.text
		else:
			url = 'http://revere.patriotproperties.com/SearchResults.asp?page=' + str(page_number)
			print('Loading ' + query + ' page ' + str(page_number))
			cookie_str = ''
			try:
				cookie_str = 'ASPSESSIONIDSCQCTRRQ=' + cookie['ASPSESSIONIDSCQCTRRQ']
			except KeyError:
				pass

			headers = {
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'en-US,en;q=0.9',
				'Connection': 'keep-alive',
				'Cookie': cookie_str,
				'DNT': '1',
				'Host': 'revere.patriotproperties.com',
				'Referer': 'http://revere.patriotproperties.com/SearchResults.asp?page=' + str(page_number - 1),
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
			}

			# print('Cookie: ' + str(cookie))
			# print('Header cookie: ' + cookie_str + ';')
			try:
				page = requests.get(url, timeout=5, headers=headers)
			except requests.exceptions.ConnectTimeout:
				print('Timed out. Reloading ' + str(page_number))
				continue

			current_page_number += 1
			cookie = cookie
			page_text = page.text

		next_idx = 0
		lot_available = page_text.find('?AccountNumber', next_idx) != -1

		while lot_available:
			account_idx = page_text.find('?AccountNumber', next_idx)

			parcel_idx = page_text.find('>', account_idx)
			end_idx = page_text.find('<', parcel_idx)

			street_number_idx = page_text.find('<TD>', end_idx)
			end_street_number_idx = page_text.find('&', street_number_idx)

			start_street_name = page_text.find('bottom">', end_street_number_idx)
			end_street_name = page_text.find('</A', start_street_name)

			parcel_id = page_text[parcel_idx + 1:end_idx]
			street_number = page_text[street_number_idx + 4:end_street_number_idx]
			street_name = page_text[start_street_name + 8:end_street_name]

			if query.lower() in street_name.lower():
				appending_lot = Lot(parcel_id, street_number, street_name)
				# print(appending_lot.__str__())
				if not allowDuplicates:
					if street_number not in street_numbers:
						lots.append(appending_lot)
						street_numbers.append(street_number)
				else:
					lots.append(appending_lot)

			next_idx = end_street_name
			lot_available = page_text.find('?AccountNumber', next_idx) != -1

	print('Loaded ' + str(len(lots)) + ' lots')
	return lots


def writeToCSV(file_name, *queries):
	file = open(file_name, 'w')
	file.write('Address,Parcel ID\n')
	for i in range(0, len(queries)):
		queryData = searchAddresses(queries[i], allowDuplicates=False)
		for lot in queryData:
			file.write(lot.getAddressStr() + ',' + lot.parcel_id + '\n')
	file.close()


def writeAllLots(allowDuplicates=False):
	lots = searchTotalValue('0', allowDuplicates=allowDuplicates)

	a_file = open('parcel_ids/a_addresses.csv', 'w')
	a_file.write('parcel_ids/Address,Parcel ID\n')
	b_file = open('parcel_ids/b_addresses.csv', 'w')
	b_file.write('Address,Parcel ID\n')
	c_file = open('parcel_ids/c_addresses.csv', 'w')
	c_file.write('Address,Parcel ID\n')
	d_file = open('parcel_ids/d_addresses.csv', 'w')
	d_file.write('Address,Parcel ID\n')
	e_file = open('parcel_ids/e_addresses.csv', 'w')
	e_file.write('Address,Parcel ID\n')
	f_file = open('parcel_ids/f_addresses.csv', 'w')
	f_file.write('Address,Parcel ID\n')
	g_file = open('parcel_ids/g_addresses.csv', 'w')
	g_file.write('Address,Parcel ID\n')
	h_file = open('parcel_ids/h_addresses.csv', 'w')
	h_file.write('Address,Parcel ID\n')
	i_file = open('parcel_ids/i_addresses.csv', 'w')
	i_file.write('Address,Parcel ID\n')
	j_file = open('parcel_ids/j_addresses.csv', 'w')
	j_file.write('Address,Parcel ID\n')
	k_file = open('parcel_ids/k_addresses.csv', 'w')
	k_file.write('Address,Parcel ID\n')
	l_file = open('parcel_ids/l_addresses.csv', 'w')
	l_file.write('Address,Parcel ID\n')
	m_file = open('parcel_ids/m_addresses.csv', 'w')
	m_file.write('Address,Parcel ID\n')
	n_file = open('parcel_ids/n_addresses.csv', 'w')
	n_file.write('Address,Parcel ID\n')
	o_file = open('parcel_ids/o_addresses.csv', 'w')
	o_file.write('Address,Parcel ID\n')
	p_file = open('parcel_ids/p_addresses.csv', 'w')
	p_file.write('Address,Parcel ID\n')
	q_file = open('parcel_ids/q_addresses.csv', 'w')
	q_file.write('Address,Parcel ID\n')
	r_file = open('parcel_ids/r_addresses.csv', 'w')
	r_file.write('Address,Parcel ID\n')
	s_file = open('parcel_ids/s_addresses.csv', 'w')
	s_file.write('Address,Parcel ID\n')
	t_file = open('parcel_ids/t_addresses.csv', 'w')
	t_file.write('Address,Parcel ID\n')
	u_file = open('parcel_ids/u_addresses.csv', 'w')
	u_file.write('Address,Parcel ID\n')
	v_file = open('parcel_ids/v_addresses.csv', 'w')
	v_file.write('Address,Parcel ID\n')
	w_file = open('parcel_ids/w_addresses.csv', 'w')
	w_file.write('Address,Parcel ID\n')
	x_file = open('parcel_ids/x_addresses.csv', 'w')
	x_file.write('Address,Parcel ID\n')
	y_file = open('parcel_ids/y_addresses.csv', 'w')
	y_file.write('Address,Parcel ID\n')
	z_file = open('parcel_ids/z_addresses.csv', 'w')
	z_file.write('Address,Parcel ID\n')

	for lot in lots:
		print(lot.getAddressStr() + '\n\tParcel ID: ' + lot.parcel_id)
		first_letter = lot.street_name[0]
		line = lot.getAddressStr() + ',' + lot.parcel_id

		if first_letter.lower() == 'a':
			a_file.write(line + '\n')
		elif first_letter.lower() == 'b':
			b_file.write(line + '\n')
		elif first_letter.lower() == 'c':
			c_file.write(line + '\n')
		elif first_letter.lower() == 'd':
			d_file.write(line + '\n')
		elif first_letter.lower() == 'e':
			e_file.write(line + '\n')
		elif first_letter.lower() == 'f':
			f_file.write(line + '\n')
		elif first_letter.lower() == 'g':
			g_file.write(line + '\n')
		elif first_letter.lower() == 'h':
			h_file.write(line + '\n')
		elif first_letter.lower() == 'i':
			i_file.write(line + '\n')
		elif first_letter.lower() == 'j':
			j_file.write(line + '\n')
		elif first_letter.lower() == 'k':
			k_file.write(line + '\n')
		elif first_letter.lower() == 'l':
			l_file.write(line + '\n')
		elif first_letter.lower() == 'm':
			m_file.write(line + '\n')
		elif first_letter.lower() == 'n':
			n_file.write(line + '\n')
		elif first_letter.lower() == 'o':
			o_file.write(line + '\n')
		elif first_letter.lower() == 'p':
			p_file.write(line + '\n')
		elif first_letter.lower() == 'q':
			q_file.write(line + '\n')
		elif first_letter.lower() == 'r':
			r_file.write(line + '\n')
		elif first_letter.lower() == 's':
			s_file.write(line + '\n')
		elif first_letter.lower() == 't':
			t_file.write(line + '\n')
		elif first_letter.lower() == 'u':
			u_file.write(line + '\n')
		elif first_letter.lower() == 'v':
			v_file.write(line + '\n')
		elif first_letter.lower() == 'w':
			w_file.write(line + '\n')
		elif first_letter.lower() == 'x':
			x_file.write(line + '\n')
		elif first_letter.lower() == 'y':
			y_file.write(line + '\n')
		elif first_letter.lower() == 'z':
			z_file.write(line + '\n')
	print('\nDone!')


if __name__ == '__main__':
	lots = searchAddresses('Revere Beach Blvd', allowDuplicates=False)

	for lot in lots:
		print(lot.street_number + ' ' + lot.street_name)
		print('\tParcel ID: ' + lot.parcel_id)
	print('\nLot count: ' + str(len(lots)))
