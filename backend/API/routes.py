from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated

from backend.models.engine import clientePOST

router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login_cliente', response_model=clienteResponse,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login_cliente(cliente_login: clienteLOGIN, session: SessionDep) -> clienteResponse:
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_login.cpf)

    cliente_valido = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()

    if cliente_valido:
        if verificar_senha(senha=cliente_login.senha, hash_salvo=cliente_valido.senha):
            return clienteResponse.model_validate(cliente_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> HTTPException | clientePOST:
    print(cliente_cadastro.cpf)
    cliente_valido = validacao_cpf(cpf=cliente_cadastro.cpf,
                                     nome_completo=cliente_cadastro.nome,
                                     data_nascimento=cliente_cadastro.data_nascimento,)

    if cliente_valido == int:
        return HTTPException(status_code=404, detail='erro na validação de cliente')

    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_cadastro.cpf)
    senha_HASH = senha_hash(senha=cliente_cadastro.senha)

    cliente_existe = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()

    if cliente_existe is not None:
        raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

    cliente_novo = cliente(
        nome=cliente_cadastro.nome,
        cpf=cpf_HASH,
        data_nascimento=cliente_cadastro.data_nascimento,
        senha=senha_HASH,
        email=cliente_cadastro.email,
        numero_telefone_pessoal=cliente_cadastro.numero_telefone_pessoal,
        cep=cliente_cadastro.cep,
        estado=cliente_cadastro.estado,
        cidade=cliente_cadastro.cidade,
        bairro=cliente_cadastro.bairro,
        logradouro=cliente_cadastro.logradouro,
    )

    session.add(cliente_novo)
    session.commit()
    session.refresh(cliente_novo)

    return clientePOST.model_validate(cliente_novo)


@router.post(path='/login_fornecedor', response_model=fornecedorResponde,
             responses={404: {'description': 'Usuario nao encontrado'},
                        401: {'description': 'Senha incorreta'}
                        })
async def login_fornecedor(fornecedor_login: fornecedorLOGIN, session: SessionDep) -> fornecedorResponde:
    cnpj = ''.join(re.sub(r'\W', '', fornecedor_login.cnpj))
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cnpj)

    fornecedor_valido = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()

    if fornecedor_valido:
        if verificar_senha(senha=fornecedor_login.senha, hash_salvo=fornecedor_valido.senha):
            return fornecedorResponde.model_validate(fornecedor_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/fornecedor', response_model=fornecedorPOST)
async def cadastro_fornecedor(fornecedor_cadastro: fornecedorREQUEST, session: SessionDep) -> fornecedorPOST | HTTPException:
    fornecedor_dados = validacao_cnpj(cnpj=fornecedor_cadastro.cnpj,
                                      nome_oficial_empresa=fornecedor_cadastro.nome_oficial_empresa)

    if isinstance(fornecedor_dados, int):
        raise HTTPException(status_code=400, detail='Erro na validação do CNPJ')

    cnpj = ''.join(re.sub(r'\W', '', fornecedor_cadastro.cnpj))
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cnpj)
    senha_HASH = senha_hash(senha=fornecedor_cadastro.senha)

    fornecedor_existe = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()

    if fornecedor_existe is not None:
        raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

    fornecedor_novo = fornecedor(
        cnpj=cnpj_HASH,
        senha=senha_HASH,
        nome_oficial_empresa=fornecedor_dados['nome_oficial_empresa'],
        nome_cormecial_empresa=fornecedor_dados['nome_cormecial_empresa'],
        situacao_cadastral=fornecedor_dados['situacao_cadastral'],
        data_abertura=fornecedor_dados['data_abertura'],
        natureza_juridica=fornecedor_dados['natureza_juridica'],
        cnae=fornecedor_dados['cnae'],
        capital_social=fornecedor_dados['capital_social'],
        porte_empresa=fornecedor_dados['porte_empresa'],
        email=fornecedor_cadastro.email,
        numero_telefone_empresa=fornecedor_cadastro.numero_telefone_empresa,
        cep=fornecedor_dados['cep'],
        uf=fornecedor_dados['uf'],
        cidade=fornecedor_dados['cidade'],
        bairro=fornecedor_dados['bairro'],
        logradouro=fornecedor_dados['logradouro'],
    )

    session.add(fornecedor_novo)
    session.commit()
    session.refresh(fornecedor_novo)

    return fornecedorPOST.model_validate(fornecedor_novo)




'''
@router.post('/produto_servico', response_model=produto_servicoPOST)
async def cadastro_cliente(produto_servico_cadastro: produto_servicoPOST, session: SessionDep) -> produto_servicoPOST:

    if [] == (cliente_existe := session.execute(select(produto_servico).where(produto_servico.uuid == )).all()):

        cliente_novo = cliente(
            nome = cliente_cadastro.nome,
            cpf = cpf_HASH,
            data_nascimento = cliente_cadastro.data_nascimento,
            senha = senha_HASH,
            email = cliente_cadastro.email,
            numero_telefone_pessoal = cliente_cadastro.numero_telefone_pessoal,
            cep = cliente_cadastro.cep,
            estado = cliente_cadastro.estado,
            cidade = cliente_cadastro.cidade,
            bairro = cliente_cadastro.bairro,
            logradouro = cliente_cadastro.logradouro,
        )

        session.add(cliente_novo)
        session.commit()
        session.refresh(cliente_novo)

        return clientePOST.model_validate(cliente_novo)
    raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')'''