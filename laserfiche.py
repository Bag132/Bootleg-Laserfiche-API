import requests
from requests import Response


def createAuthToken(repoId: str, customerId: str, username: str, password: str, applicationName: str = '',
					createCookie: bool = False) -> Response:
	create_token_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/AccessTokens/Create?createCookie=' + str(
		createCookie).lower() + '&customerId=' + customerId

	create_token_headers = {
		'accept': 'application/json',
		'Content-Type': 'application/json'
	}

	create_token_data = {
		'username': username,
		'password': password,
		'applicationName': applicationName
	}

	return requests.post(create_token_url, json=create_token_data, headers=create_token_headers)


def refreshAuthToken(repoId: str, keep_alive: int = 30, cookie: dict = None) -> Response:
	refresh_token_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/AccessTokens/Refresh'

	refresh_token_headers = {
		'accept': 'application/json',
		'Keep-Alive': str(keep_alive)
	}

	return requests.post(refresh_token_url, headers=refresh_token_headers, cookies=cookie)


def invalidateAuthToken(repoId: str, cookie: dict = None) -> Response:
	invalidate_token_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/AccessTokens/Invalidate'

	invalidate_token_headers = {
		'accept': 'application/json'
	}

	return requests.post(invalidate_token_url, headers=invalidate_token_headers, cookies=cookie)


password = 'Victor132'


def getAddresses(repoId: str, streetFolderId: str, cookie: dict = None) -> Response:
	get_addresses_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/Entries/' + streetFolderId + '/Laserfiche.Repository.Folder/children'

	get_addresses_headers = {
		'accept': 'application/json',
	}

	return requests.get(get_addresses_url, headers=get_addresses_headers, cookies=cookie)


def getAddressEntries(repoId: str, addressFolderId: str, cookie: dict = None) -> Response:
	get_address_docs_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/Entries/' + addressFolderId + '/Laserfiche.Repository.Folder/children'

	get_address_docs_headers = {
		'accept': 'application/json'
	}

	return requests.get(get_address_docs_url, headers=get_address_docs_headers, cookies=cookie)


def getDocumentFields(repoId: str, documentId: str, cookie: dict = None) -> Response:
	get_document_fields_url = 'https://api.laserfiche.com/repository/v1/Repositories/' + repoId + '/Entries/' + documentId + '/fields'

	get_document_fields_headers = {
		'accept': 'application/json'
	}

	return requests.get(get_document_fields_url, headers=get_document_fields_headers, cookies=cookie)


def setDocumentParcelID(repoId: str, documentId: str, parcelID: str, cookie: dict = None) -> Response:
	pass  # ToDo: Once granted authorization


if __name__ == '__main__':
	response = createAuthToken('052ecf80', '672803730', 'vlomba', 'Victor132')
	print(response.text)
