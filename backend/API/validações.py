import requests


def validacao_cnpj(cnpj):
    url_base = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

    response = requests.get(url=url_base)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        resultado = response.json()





