from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import uuid4, UUID


class Base(DeclarativeBase):
    pass

class cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150))
    cpf: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    senha: Mapped[str] = mapped_column(String(150), index=True)
    data_nascimento: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(100))
    numero_telefone_pessoal: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(30))
    estado: Mapped[str] = mapped_column(String(30))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

    produtos: Mapped[list['produto_servico_cliente']] = relationship(
        back_populates="cliente"
    )

class clientePOST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    cpf: str
    data_nascimento: str
    senha: str
    email: str
    numero_telefone_pessoal: str
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str

class clienteLOGIN(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf : str
    senha : str

class clienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str

class fornecedor(Base):
    __tablename__ = 'fornecedor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    senha: Mapped[str] = mapped_column(String(150), index=True)
    nome_oficial_empresa: Mapped[str] = mapped_column(String(150))
    nome_cormecial_empresa: Mapped[str] = mapped_column(String(150))
    situacao_cadastral: Mapped[str] = mapped_column(String(20))
    data_abertura: Mapped[str] = mapped_column(String(20))
    natureza_juridica: Mapped[str] = mapped_column(String(150))
    cnae: Mapped[str] = mapped_column(String(150)) # Atividade econômica
    capital_social: Mapped[float] = mapped_column(Float)
    porte_empresa: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))
    numero_telefone_empresa: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(20))
    uf: Mapped[str] = mapped_column(String(2))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

class fornecedorREQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_oficial_empresa: str
    cnpj: str
    senha: str
    email: str
    numero_telefone_empresa: str


class fornecedorPOST(BaseModel):  # class despesasPOST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str
    nome_oficial_empresa: str
    nome_cormecial_empresa: str
    situacao_cadastral: str
    data_abertura: datetime
    natureza_juridica: str
    cnae: str
    capital_social: float
    porte_empresa: str
    email: str
    numero_telefone_empresa: str
    cep: str
    uf: str
    cidade: str
    bairro: str
    logradouro: str


class fornecedorLOGIN(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str

class fornecedorResponde(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_oficial_empresa: str

class produto_servico_cliente(Base):
    __tablename__ = 'produto_servico_cliente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_servico_cliente_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    classificacao_produto_servico: Mapped[str] = mapped_column(String(50))
    nome_produto_servico: Mapped[str] = mapped_column(String(150))
    cpf_vendendor: Mapped[str] = mapped_column(String(100),ForeignKey('cliente.cpf'), index=True)
    detalhes_produto_servico: Mapped[str] = mapped_column(String(150), index=True)
    data_do_cadastro_produto_servico: Mapped[str] = mapped_column(String(30))
    valor_custo_produto_servico: Mapped[float] = mapped_column(Float)
    ICMS_do_produto_servico: Mapped[str] = mapped_column(String(150))
    valor_com_IMCS_produto_servico: Mapped[float] = mapped_column(Float)
    valor_final_de_venda_produto_servico: Mapped[float] = mapped_column(Float)
    margem_de_lucro_produto_servico: Mapped[float] = mapped_column(Float)

    cliente: Mapped['cliente'] = relationship(back_populates="produtos")


class produto_servico_cliente_REQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf : str
    classificacao_produto_servico: str
    nome_produto_servico: str
    detalhes_produto_servico: str
    valor_custo_de_venda_produto_servico: float
    valor_final_de_venda_produto_servico: float

class produto_servico_cliente_POST(produto_servico_cliente_REQUEST):
        uuid: UUID

class produto_servico_cliente_Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    classificacao_produto_servico: str
    detalhes_produto_servico: str
    data_do_cadastro_produto_servico: str
    valor_custo_produto_servico: float
    ICMS_do_produto_servico: str
    valor_com_IMCS_produto_servico: float
    valor_final_de_venda_produto_servico: float
    margem_de_lucro_produto_servico: float

class produto_servico_fornecedor(Base):
    __tablename__ = 'produtos_servico_produto'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    classificacao_produto_servico: Mapped[str] = mapped_column(String(50))
    cpf_vendendor: Mapped[str] = mapped_column(ForeignKey('fornecedor.cnpj'), index=True)
    detalhes_produto_servico: Mapped[str] = mapped_column(String(150))
    data_do_cadastro_produto_servico: Mapped[str] = mapped_column(String(30))
    valor_custo_produto_servico: Mapped[float] = mapped_column(Float)
    ICMS_do_produto_servico: Mapped[str] = mapped_column(String(150))
    valor_com_IMCS_produto_servico: Mapped[float] = mapped_column(Float)
    valor_final_de_venda_produto_servico: Mapped[float] = mapped_column(Float)
    margem_de_lucro_produto_servico: Mapped[float] = mapped_column(Float)

    class produto_servico_fornecedor_REQUEST(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        cnpj: str
        classificacao_produto_servico: str
        detalhes_produto_servico: str
        valor_custo_produto_servico: float
        valor_final_de_venda_produto_servico: float
