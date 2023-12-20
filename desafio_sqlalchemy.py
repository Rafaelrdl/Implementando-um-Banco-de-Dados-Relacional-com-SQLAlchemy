"""
    Módulo desafio = Implementando um Banco de Dados Relacional com SQLAlchemy
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

Base = declarative_base()


class Clientes(Base):
    """
        Representa um cliente no sistema.

        Atributos:
        - id (int): Identificador único do cliente.
        - nome (str): Nome do cliente.
        - cpf (str): CPF (Cadastro de Pessoas Físicas) do cliente, um número de identificação brasileiro.
        - endereco (str): Endereço do cliente.
        - contas (relationship): Relacionamento com a classe 'Contas' representando contas associadas ao cliente.

        Métodos:
        - __repr__: Retorna uma representação em string do cliente para facilitar a depuração e registro.

        Observação:
        Esta classe é projetada para ser usada com uma classe Base do SQLAlchemy para interações com o banco de dados.

    """
    __tablename__ = 'Cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    contas = relationship("Contas", back_populates="cliente")

    def __repr__(self):
        return f"Cliente('{self.nome}', '{self.cpf}', '{self.endereco}')"


class Contas(Base):
    """
        Representa uma conta no sistema.

        Atributos:
        - id (int): Identificador único da conta.
        - tipo (str): Tipo da conta.
        - agencia (str): Número da agência associada à conta.
        - num (int): Número da conta.
        - saldo (float): Saldo atual da conta.
        - id_cliente (int): Identificador do cliente associado à conta.

        Relacionamentos:
        - cliente (relationship): Relacionamento com a classe 'Clientes', representando o cliente associado a esta conta.

        Métodos:
        - __repr__: Retorna uma representação em string da conta para facilitar a depuração e registro.

        Observação:
        Esta classe é projetada para ser usada com uma classe Base do SQLAlchemy para interações com o banco de dados.
        """
    __tablename__ = 'Conta'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    saldo = Column(Float)
    id_cliente = Column(Integer, ForeignKey('Cliente.id'))

    cliente = relationship("Clientes", back_populates="contas")

    def __repr__(self):
        return f"Conta('{self.id}', '{self.tipo}', '{self.agencia}', '{self.num}', '{self.saldo}')"

engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

with Session(engine) as session:

    rafael = Clientes(
        nome="Rafael Ribeiro",
        cpf="657438674",
        endereco="Belo Horizonte/MG",
        contas=[Contas(
            tipo="Conta Corrente",
            agencia="0001",
            num="876564",
            saldo=1000.23
        )]
    )

    carlos = Clientes(
        nome="Carlos Roberto",
        cpf="657435632",
        endereco="Pará de Minas/MG",
        contas=[Contas(
            tipo="Conta Poupança",
            agencia="0013",
            num="136564",
            saldo=2467.23
        )]
    )


    session.add_all([rafael,carlos])
    session.commit()

stmt = select(Clientes).where(Clientes.nome.in_(["Rafael Ribeiro", "Carlos Roberto"]))
for clientes in session.scalars(stmt):
    print(clientes)

stmt_conta = select(Contas).where(Contas.tipo.in_(["Conta Corrente", "Conta Poupança"]))
for x in session.scalars(stmt_conta):
    print(x)


stmt_join = select(Clientes.nome, Contas.saldo, Contas.tipo).join_from(Contas, Clientes)
for nome, saldo, tipo in session.execute(stmt_join):
    print(f"Nome: {nome}, Saldo: {saldo}, Tipo de Conta {tipo}")
