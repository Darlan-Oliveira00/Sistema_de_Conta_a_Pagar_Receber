from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated


router = APIRouter(prefix="/cadastro", tags=["cadastro"])
SessionDep= Annotated[Session, Depends(get_session)]

@router.post(path='/login/', response_model=clienteGET,
         responses={404: {'description': 'Usuario nao encotrado '}})
async def login(cliente_login: clienteGET, session: SessionDep) -> clienteGET:
    cpf_HASH = cpf_hash(cpf=cliente_login.cpf)

    if cliente_valido := session.execute(select(cliente).where(cliente.cpf == cpf_HASH)).scalar_one():
        if verificar_senha(senha=cliente_login.senha, hash_salvo=cliente_valido.senha):
            return clienteGET.model_validate(cliente_valido)
    raise HTTPException(status_code=404,detail='Usuario nao encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> clientePOST:
    cpf_HASH = cpf_hash(cpf=cliente_cadastro.cpf)
    senha_HASH = senha_hash(senha=cliente_cadastro.senha)


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