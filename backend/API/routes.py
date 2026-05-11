from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["cadastro e login"])
SessionDep= Annotated[Session, Depends(get_session)]

@router.post(path='/login_cliente', response_model=clienteGET,
         responses={404: {'description': 'Usuario nao encotrado '}})
async def login(cliente_login: clienteGET, session: SessionDep) -> clienteGET:
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_login.cpf)

    if cliente_valido := session.execute(select(cliente).where(cliente.cpf == cpf_HASH)).all():
        cliente_valido = session.execute(select(cliente).where(cliente.cpf == cpf_HASH)).scalar_one()
        if verificar_senha(senha=cliente_login.senha, hash_salvo=cliente_valido.senha):
            return clienteGET.model_validate(cliente_valido)
        raise  HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404,detail='Usuario nao encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> clientePOST:
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_cadastro.cpf)
    senha_HASH = senha_hash(senha=cliente_cadastro.senha)

    if [] == (cliente_existe := session.execute(select(cliente).where(cliente.cpf == cpf_HASH)).all()):

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
    raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

@router.post(path='/login_fornecedor/', response_model= fornecedorGET,
         responses={404: {'description': 'Usuario nao encotrado '}})
async def login(fornecedor_login: fornecedorGET, session: SessionDep) -> fornecedorPOST:
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=fornecedor_login.cnpj)

    if fornecedor_valido := session.execute(select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)).all():
        fornecedor_valido = session.execute(select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)).scalar_one()
        if verificar_senha(senha=fornecedor_login.senha, hash_salvo=fornecedor_valido.senha):
            return fornecedorPOST.model_validate(fornecedor_valido)
        raise  HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404,detail='Usuario nao encontrado')


@router.post('/fornecedor', response_model=fornecedorPOST)
async def cadastro_fornecedor(fornecedor_cadastro: fornecedorPOST, session: SessionDep) -> fornecedorPOST:
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=fornecedor_cadastro.cnpj)
    senha_HASH = senha_hash(senha=fornecedor_cadastro.senha)

    if [] == (fornecedor_existe := session.execute(select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)).all()):
        fornecedor_novo = fornecedor(
            cnpj=cnpj_HASH,
            senha=senha_HASH,
            nome_oficial_empresa=fornecedor_cadastro.nome_oficial_empresa,
            nome_cormecial_empresa=fornecedor_cadastro.nome_cormecial_empresa,
            situacao_cadastral=fornecedor_cadastro.situacao_cadastral,
            data_abertura=fornecedor_cadastro.data_abertura,
            natureza_juridica=fornecedor_cadastro.natureza_juridica,
            cnae=fornecedor_cadastro.cnae,
            capital_social=fornecedor_cadastro.capital_social,
            porte_empresa= fornecedor_cadastro.porte_empresa,
            email=fornecedor_cadastro.email,
            numero_telefone_empresa=fornecedor_cadastro.numero_telefone_empresa,
            cep=fornecedor_cadastro.cep,
            uf=fornecedor_cadastro.uf,
            cidade=fornecedor_cadastro.cidade,
            bairro=fornecedor_cadastro.bairro,
            logradouro=fornecedor_cadastro.logradouro,
        )

        session.add(fornecedor_novo)
        session.commit()
        session.refresh(fornecedor_novo)

        return fornecedorPOST.model_validate(fornecedor_novo)
    raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')