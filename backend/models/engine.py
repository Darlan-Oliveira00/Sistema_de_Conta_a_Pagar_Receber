from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Float
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Base(DeclarativeBase):
    pass

class cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150))
    cpf: Mapped[str] = mapped_column(String(150), index=True)
    senha: Mapped[str] = mapped_column(String(150), index=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime)
    email: Mapped[str] = mapped_column(String(100))
    numero_telefone_pessoal: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(30))
    estado: Mapped[str] = mapped_column(String(30))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

class clientePOST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    cpf: str
    data_nascimento: datetime
    senha: str
    email: str
    numero_telefone_pessoal: str
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str

class clienteGET(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf : str
    senha : str


class fornecedor(Base):
    __tablename__ = 'fornecedor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = mapped_column(String(150), index=True)
    senha: Mapped[str] = mapped_column(String(150), index=True)
    nome_oficial_empresa: Mapped[str] = mapped_column(String(150))
    nome_cormecial_empresa: Mapped[str] = mapped_column(String(150))
    situacao_cadastral: Mapped[str] = mapped_column(String(20))
    data_abertura: Mapped[datetime] = mapped_column(DateTime)
    natureza_juridica: Mapped[str] = mapped_column(String(150))
    cnae: Mapped[str] = mapped_column(String(150)) # Atividade econômica
    capital_social: Mapped[float] = mapped_column(Float)
    porte_empresa: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))
    numero_telefone_empresa: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(9))
    uf: Mapped[str] = mapped_column(String(2))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))


class fornecedorPOST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str
    nome_oficial_empresa: str
    nome_cormecial_empresa: str
    situacao_cadastral: str
    natureza_juridica: str
    data_abertura: datetime
    natureza_juridica: str
    cnae: str
    capital_social: str
    porte_emprese: str
    email: str
    numero_telefone_empresa: str
    cep: str
    uf: str
    cidade: str
    bairro: str
    logradouro: str


class fornecedorGET(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str