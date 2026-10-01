import json
import banco


# ===== Helper: função auxiliar pra evitar repetição no ARRANGE =====
def setup_banco_vazio():
    """Prepara o banco de teste limpo antes de cada teste."""
    banco.ARQUIVO_DADOS = 'dados_test.json'
    with open('dados_test.json', 'w') as f:
        json.dump({}, f)


# ===== Testes de transferencia =====

def test_transferir_funciona():
    setup_banco_vazio()
    banco.criar_conta('Maria', 0)
    banco.criar_conta('Lucas', 0)
    banco.depositar('Maria',1,50)
    resultado = banco.transferir('1','2', 50)
    assert resultado == 'transferencia_concluida'


# ===== Testes de criar_conta =====

def test_criar_conta_funciona():
    setup_banco_vazio()
    resultado = banco.criar_conta('Teste', 0)
    assert resultado == 'Conta_criada'


def test_criar_conta_duplicada():
    setup_banco_vazio()
    banco.criar_conta('João', 0)              # cria a primeira
    resultado = banco.criar_conta('João', 0)  # tenta criar de novo
    assert resultado == 'Nome_invalido'


# ===== Testes de depositar =====

def test_depositar_funciona():
    setup_banco_vazio()
    banco.criar_conta('Maria', 0)
    resultado = banco.depositar('Maria', 1, 500)
    assert resultado == 'Deposito_concluido'


def test_depositar_conta_inexistente():
    setup_banco_vazio()
    resultado = banco.depositar('Fantasma', 99, 100)
    assert resultado == 'Deposito_falhou'


# ===== Testes de sacar =====

def test_sacar_funciona():
    setup_banco_vazio()
    banco.criar_conta('Pedro', 0)
    banco.depositar('Pedro', 1, 500)
    resultado = banco.sacar('Pedro', 1, 200)
    assert resultado == 'Saque_concluido'


def test_sacar_valor_exato():
    """Testa que dá pra sacar o valor exato (bug do >= que a gente consertou)."""
    setup_banco_vazio()
    banco.criar_conta('Ana', 0)
    banco.depositar('Ana', 1, 100)
    resultado = banco.sacar('Ana', 1, 100)
    assert resultado == 'Saque_concluido'


def test_sacar_sem_saldo():
    setup_banco_vazio()
    banco.criar_conta('Lucas', 0)
    banco.depositar('Lucas', 1, 50)
    resultado = banco.sacar('Lucas', 1, 500)
    assert resultado == 'Sem_saldo'


# ===== Testes de verificar_valor =====

def test_verificar_valor_positivo():
    assert banco.verificar_valor('100') == True


def test_verificar_valor_negativo():
    assert banco.verificar_valor('-50') == False


def test_verificar_valor_texto():
    assert banco.verificar_valor('abc') == False


# ===== Teste de verificar_nome =====

def test_verificar_nome_valido():
    assert banco.verificar_nome('Anderson Silva') == True


def test_verificar_nome_com_numero():
    assert banco.verificar_nome('Anderson 123') == False
