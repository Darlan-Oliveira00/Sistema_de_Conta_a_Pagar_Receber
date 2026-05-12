from fastapi import APIRouter, Depends, HTTPException
import traceback
from datetime import datetime

from backend.API.validações import validacao_cnpj
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login_cliente', response_model=clienteGET,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login_cliente(cliente_login: clienteGET, session: SessionDep) -> clienteGET:
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_login.cpf)
    
    cliente_valido = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()
    
    if cliente_valido:
        if verificar_senha(senha=cliente_login.senha, hash_salvo=cliente_valido.senha):
            return clienteGET.model_validate(cliente_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> clientePOST:
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cliente_cadastro.cpf)
    senha_HASH = senha_hash(senha=cliente_cadastro.senha)

    cliente_existe = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()
    
    if cliente_existe is None:
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
    raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')


@router.post(path='/login_fornecedor', response_model=fornecedorGET,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login_fornecedor(fornecedor_login: fornecedorGET, session: SessionDep) -> fornecedorGET:
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=fornecedor_login.cnpj)

    fornecedor_valido = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()
    
    if fornecedor_valido:
        if verificar_senha(senha=fornecedor_login.senha, hash_salvo=fornecedor_valido.senha):
            return fornecedorGET.model_validate(fornecedor_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/fornecedor', response_model=fornecedorPOST)
async def cadastro_fornecedor(fornecedor_cadastro: fornecedorREQUEST, session: SessionDep) -> fornecedorPOST:
    try:
        # Validar CNPJ contra BrasilAPI
        fornecedor_dados = validacao_cnpj(
            cnpj=fornecedor_cadastro.cnpj, 
            nome_oficial_empresa=fornecedor_cadastro.nome_oficial_empresa
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro na validação: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f'Erro ao validar CNPJ: {str(e)}')

    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=fornecedor_cadastro.cnpj)
    fornecedor_existe = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()
    
    if fornecedor_existe is not None:
        raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

    senha_HASH = senha_hash(senha=fornecedor_cadastro.senha)

    try:
        data_abertura = fornecedor_dados['data_abertura']
        if isinstance(data_abertura, str):
            data_abertura = datetime.strptime(data_abertura, '%Y-%m-%d').date()
        
        # Criar novo fornecedor com dados validados
        fornecedor_novo = fornecedor(
            cnpj=cnpj_HASH,
            senha=senha_HASH,
            nome_oficial_empresa=fornecedor_dados['nome_oficial_empresa'],
            nome_cormecial_empresa=fornecedor_dados['nome_cormecial_empresa'],
            situacao_cadastral=fornecedor_dados['situacao_cadastral'],
            data_abertura=data_abertura,  # ← Agora é datetime.date
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

        print(f"Criando fornecedor: {fornecedor_novo}")
        session.add(fornecedor_novo)
        session.commit()
        session.refresh(fornecedor_novo)
        print(f"Fornecedor criado com sucesso: {fornecedor_novo.id}")
        
        return fornecedorPOST.model_validate(fornecedor_novo)
        
    except ValueError as e:
        session.rollback()
        print(f"Erro de validação de dados: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f'Erro nos dados: {str(e)}')
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar fornecedor: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Erro ao cadastrar fornecedor: {str(e)}')