import requests
from fastapi import HTTPException
from pprint import pprint


def validacao_cnpj(cnpj, nome_oficial_empresa):
    """
    Valida CNPJ contra a API BrasilAPI.
    
    Args:
        cnpj: String com 14 dígitos do CNPJ
        nome_oficial_empresa: Nome oficial da empresa para validar
    
    Returns:
        Dict com os dados da empresa
    
    Raises:
        HTTPException: Se o CNPJ for inválido ou não encontrado
    """
    url_base = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

    try:
        response = requests.get(url=url_base, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=503, detail='Serviço de validação indisponível - timeout')
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail='Erro ao conectar ao serviço de validação')
    except requests.HTTPError as e:
        if response.status_code == 404:
            raise HTTPException(status_code=400, detail='CNPJ não encontrado ou inválido')
        elif response.status_code == 429:
            raise HTTPException(status_code=429, detail='Muitas requisições - tente novamente em alguns segundos')
        else:
            raise HTTPException(status_code=400, detail=f'Erro ao validar CNPJ: {response.status_code}')
    
    try:
        resultado = response.json()
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=502, detail='Resposta inválida do serviço de validação')

    # Validar se a razão social corresponde
    if resultado.get('razao_social', '').upper() != nome_oficial_empresa.upper():
        raise HTTPException(
            status_code=400, 
            detail=f'Nome da empresa não corresponde. Esperado: {resultado.get("razao_social")}'
        )

    # Retornar dados validados
    return {
        'cnpj': resultado.get('cnpj', ''),
        'nome_oficial_empresa': resultado.get('razao_social', ''),
        'nome_cormecial_empresa': resultado.get('nome_fantasia', ''),
        'situacao_cadastral': resultado.get('situacao_cadastral', ''),
        'data_abertura': resultado.get('data_inicio_atividade'),
        'natureza_juridica': resultado.get('natureza_juridica', ''),
        'cnae': resultado.get('cnae_fiscal', ''),
        'capital_social': resultado.get('capital_social', 0),
        'porte_empresa': resultado.get('porte', ''),
        'uf': resultado.get('uf', ''),
        'cep': resultado.get('cep', ''),
        'cidade': resultado.get('municipio', ''),
        'bairro': resultado.get('bairro', ''),
        'logradouro': resultado.get('logradouro', ''),
    }


if __name__ == '__main__':
    try:
        resposta = validacao_cnpj(cnpj='00000000000191', nome_oficial_empresa='Banco do Brasil SA')
        pprint(resposta)
    except HTTPException as e:
        print(f"Erro: {e.detail}")