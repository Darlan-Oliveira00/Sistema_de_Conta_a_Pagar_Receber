import requests
from pprint import pprint
from rich import status


def validacao_cnpj(cnpj, nome_oficial_empresa):
    url_base = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

    response = requests.get(url=url_base)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return response.status_code
    else:
        resultado = response.json()
        if resultado['razao_social'] == nome_oficial_empresa.upper():
            return {'cnpj' : resultado['cnpj'],
                    'nome_oficial_empresa': resultado['razao_social'],
                    'nome_cormecial_empresa': resultado['nome_fantasia'],
                    'situacao_cadastral':resultado['situacao_cadastral'],
                    'data_abertura':resultado['data_inicio_atividade'],
                    'natureza_juridica':resultado['natureza_juridica'],
                    'cnae':resultado['cnae_fiscal'],
                    'capital_social':resultado['capital_social'],
                    'porte_empresa':resultado['porte'],
                    'uf': resultado['uf'],
                    'cep': resultado['cep'],
                    'cidade': resultado['municipio'],
                    'bairro': resultado['bairro'],
                    'logradouro': resultado['logradouro'],}
        return 400


if __name__ == '__main__':
    resposta = validacao_cnpj(cnpj='00000000000191', nome_oficial_empresa='Banco do Brasil SA')
    pprint(resposta)