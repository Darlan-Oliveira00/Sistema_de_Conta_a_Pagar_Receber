from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login_cliente', response_model=clienteResponse,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login_cliente(cliente_login: clienteLOGIN, session: SessionDep) -> clienteResponse:
    cpf = normalidado_cpf(cpf=cliente_login.cpf)
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf)

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
    cpf = normalidado_cpf(cpf=cliente_cadastro.cpf)
    cliente_valido = validacao_cpf(cpf=cpf,
                                     nome_completo=cliente_cadastro.nome,
                                     data_nascimento=cliente_cadastro.data_nascimento,)

    if cliente_valido != 200:
        raise HTTPException(status_code=400, detail='Erro na validação do CPF')

    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf)
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
    cnpj = normalidado_cnpj(fornecedor_login.cnpj)
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
async def cadastro_fornecedor(fornecedor_cadastro: fornecedorREQUEST,
                              session: SessionDep) -> fornecedorPOST | HTTPException:
    cnpj = normalidado_cnpj(cnpj=fornecedor_cadastro.cnpj)
    fornecedor_dados = validacao_cnpj(cnpj=cnpj,
                                      nome_oficial_empresa=fornecedor_cadastro.nome_oficial_empresa)

    if isinstance(fornecedor_dados, int):
        raise HTTPException(status_code=400, detail='Erro na validação do CNPJ')

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

@router.post('/produto_servico_cliente', response_model=produto_servico_cliente_Response)
async def cadastro_produto_servico(produto_servico_cliente_cadastro: produto_servico_cliente_REQUEST,
                                   session: SessionDep) -> produto_servico_cliente_Response | HTTPException:
    cpf = normalidado_cpf(produto_servico_cliente_cadastro.cpf)
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf)


    imcs = lambda x: x * 0.18
    valor_com_imcs = float(imcs(produto_servico_cliente_cadastro.valor_final_de_venda_produto_servico))
    margem = (lambda x,y, z: x - (y + z) )
    marga_de_lucro = float(margem(produto_servico_cliente_cadastro.valor_final_de_venda_produto_servico,
                            produto_servico_cliente_cadastro.valor_custo_de_venda_produto_servico,
                            valor_com_imcs))

    novo_uuid =  uuid4()

    produto_servico_novo = produto_servico_cliente(
        produto_servico_cliente_uuid = novo_uuid,
        classificacao_produto_servico = produto_servico_cliente_cadastro.classificacao_produto_servico,
        nome_produto_servico = produto_servico_cliente_cadastro.nome_produto_servico,
        cpf_vendendor = cpf_HASH,
        detalhes_produto_servico = produto_servico_cliente_cadastro.detalhes_produto_servico,
        data_do_cadastro_produto_servico = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'),
        valor_custo_produto_servico = produto_servico_cliente_cadastro.valor_custo_de_venda_produto_servico,
        ICMS_do_produto_servico = "18%",
        valor_com_IMCS_produto_servico = valor_com_imcs,
        valor_final_de_venda_produto_servico = produto_servico_cliente_cadastro.valor_final_de_venda_produto_servico,
        margem_de_lucro_produto_servico = marga_de_lucro,
    )

    session.add(produto_servico_novo)
    session.commit()
    session.refresh(produto_servico_novo)

    return produto_servico_cliente_Response.model_validate(produto_servico_novo)

@router.post('/produto_servico_fornecedor', response_model=produto_servico_fornecedor_Response)
async def cadastro_produto_servico(produto_servico_fornecedor_cadastro: produto_servico_fornecedor_REQUEST,
                                   session: SessionDep) -> produto_servico_fornecedor_Response | HTTPException:
    cnpj = normalidado_cpf(produto_servico_fornecedor_cadastro.cnpj)
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cnpj)


    imcs = lambda x: x * 0.18
    valor_com_imcs = float(imcs(produto_servico_fornecedor_cadastro.valor_final_de_venda_produto_servico))
    margem = (lambda x,y, z: x - (y + z) )
    marga_de_lucro = float(margem(produto_servico_fornecedor_cadastro.valor_final_de_venda_produto_servico,
                            produto_servico_fornecedor_cadastro.valor_custo_produto_servico,
                            valor_com_imcs))

    novo_uuid = uuid4()

    produto_servico_novo = produto_servico_fornecedor(
        uuid = novo_uuid,
        classificacao_produto_servico = produto_servico_fornecedor_cadastro.classificacao_produto_servico,
        nome_produto_servico = produto_servico_fornecedor_cadastro.nome_produto_servico,
        cnpj_vendendor = cnpj_HASH,
        detalhes_produto_servico = produto_servico_fornecedor_cadastro.detalhes_produto_servico,
        data_do_cadastro_produto_servico = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'),
        valor_custo_produto_servico = produto_servico_fornecedor_cadastro.valor_custo_produto_servico,
        ICMS_do_produto_servico = "18%",
        valor_com_IMCS_produto_servico = valor_com_imcs,
        valor_final_de_venda_produto_servico = produto_servico_fornecedor_cadastro.valor_final_de_venda_produto_servico,
        margem_de_lucro_produto_servico = marga_de_lucro,
    )

    session.add(produto_servico_novo)
    session.commit()
    session.refresh(produto_servico_novo)

    return produto_servico_fornecedor_Response.model_validate(produto_servico_novo)

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
    raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

@router.post('/despesas', response_model=despesasPOST)
async def cadastro_despesas(fornecedor_cadastro_despesas: despesasPOST, session: SessionDep) -> despesasPOST:
        despesas_novo = fornecedor(
            cpf_cnpj_recebedor=fornecedor_cadastro_despesas.cpf_cnpj_recebedor,
            cpf_cnpj_pagador=fornecedor_cadastro_despesas.cpf_cnpj_pagador,
            data_evento=fornecedor_cadastro_despesas.data_evento,
            tipo_de_despesas=fornecedor_cadastro_despesas.tipo_de_despesas,
            data_evento=fornecedor_cadastro_despesas.data_de_evento,
        )

        session.add(despesas_novo)
        session.commit()
        session.refresh(despesas_novo)

        return despesasPOST.model_validate(despesas_novo)'''