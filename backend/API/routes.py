from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated


router = APIRouter(prefix="/cadastro", tags=["cadastro"])
SessionDep= Annotated[Session, Depends(get_session)]

@router.get(path='/login/{cfp_hash}', response_model=clienteGET,
         responses={404: {'description': 'Livro não encontrado'}})
async def login(cliente: clienteGET, session: SessionDep) -> bool:
    if cliente_login := session.execute(select(cliente).where(cliente.cpf == cliente.)).scalar_one():
        return LivroRespota.model_validate(livro)
    raise HTTPException(status_code=404,detail='Livro não encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> clientePOST:

    cliente_novo = cliente(
        nome = cliente_cadastro.nome,
        cpf = cliente_cadastro.cpf,
        data_nascimento = cliente_cadastro.data_nascimento,
        senha = cliente_cadastro.senha,
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