import json

ARQUIVO_DADOS = 'dados.json'

def atualizar_extrato(conta,tipo,valor):
    with open(ARQUIVO_DADOS, 'r') as arquivo:
        dados = json.load(arquivo)
    match tipo:
        case 'Depositar':
            for i in dados:
                if i == conta:
                    extrato = dados[i]['extrato']['transaction']+(f'+{valor}, ')
                    dados[i]['extrato']['transaction'] = extrato
                    with open(ARQUIVO_DADOS, 'w') as arquivo:
                        json.dump(dados,arquivo,indent=5)
                    return True
            return False
        case 'Sacar':
            for i in dados:
                if i == conta:
                    extrato = dados[i]['extrato']['transaction'] + (f'-{valor}, ')
                    dados[i]['extrato']['transaction'] = extrato
                    with open(ARQUIVO_DADOS, 'w') as arquivo:
                        json.dump(dados,arquivo,indent=5)
                        return True
            return False
        
def criar_conta(titular, saldo_inicial):
    with open(ARQUIVO_DADOS, 'r') as arquivo:
        dados = json.load(arquivo)
    for i in dados:
        if titular == dados[i]['Nome']: ## aqui verifica se ja tem o nome cadastrado
            return ('Nome_invalido')
    numero = str(len(dados) + 1)
    dados[numero] = {'Nome':titular,'Saldo': saldo_inicial,'extrato':{'transaction':''}}

    with open(ARQUIVO_DADOS, 'w') as arquivo:
        json.dump(dados, arquivo, indent=5)

    print(f'\n{titular} a sua conta foi criada:\n\nN° da conta {numero}\nSaldo:{saldo_inicial}\n')
    return ('Conta_criada')

def depositar(titular,conta,valor):
    with open(ARQUIVO_DADOS, 'r') as arquivo:
        dados = json.load(arquivo)
    for i in dados:
        if str(conta) == i and dados[i]['Nome'] == titular:
            depositando = (dados[i]['Saldo']) + valor
            dados[i]['Saldo'] = depositando
            with open(ARQUIVO_DADOS,'w') as arquivo:
                json.dump(dados,arquivo,indent= 5)
            print(f'Deposito concluido, seu novo saldo é {depositando}')
            atualizar_extrato(conta = conta,tipo= 'Depositar',valor = valor)
            return ('Deposito_concluido')
    print('conta nao encontrada')
    return ('Deposito_falhou')

def sacar(titular, conta, valor):
    with open(ARQUIVO_DADOS, 'r') as arquivo:
        dados = json.load(arquivo)
    for i in dados:
        if i == str(conta) and dados[i]['Nome'] == titular and dados[i]['Saldo'] > 0 and dados[i]['Saldo'] >= valor:
            sacando  = (dados[i]['Saldo']) - valor
            dados[i]['Saldo'] = sacando
            with open(ARQUIVO_DADOS,'w') as arquivo:
                json.dump(dados,arquivo, indent= 5)
            atualizar_extrato(conta = conta,tipo= 'Sacar',valor = valor)
            print(f'Saque Concluido, seu novo saldo é {sacando}')
            return 'Saque_concluido'
        if i == str(conta) and dados[i]['Saldo'] < valor and dados[i]['Nome'] == titular:
            print('Saldo inferior ao valor solicitado')
            return 'Sem_saldo'
    print('\nconta não encontrada\n')
    return 'Conta_not_found'

def adicionando_transferencia(conta2,valor):
    with open(ARQUIVO_DADOS,'r') as arquivo:
        dados = json.load(arquivo)
    for i in dados:
        if i == str(conta2):
            depositando = dados[i]['Saldo'] + valor
            dados[i]['Saldo'] = depositando
            with open(ARQUIVO_DADOS,'w') as arquivo:
                json.dump(dados,arquivo,indent = 5)
            atualizar_extrato(conta = conta2,tipo= 'Depositar',valor = valor)
            return True
    return False

def transferir(conta1,conta2,valor):
    with open(ARQUIVO_DADOS,'r') as arquivo:
        dados = json.load(arquivo)
    for i in dados:
        if i == str(conta1) and dados[i]['Saldo'] >= valor:
            if adicionando_transferencia(conta2,valor) == True:
                nome = dados[i]['Nome']
                print(f'Foi retirado {valor} da conta de {nome}')
                tranferindo = dados[i]['Saldo'] - valor
                dados[i]['Saldo'] = tranferindo
                with open (ARQUIVO_DADOS,'w') as arquivo:
                    json.dump(dados,arquivo, indent=5)
                atualizar_extrato(conta = conta1,tipo= 'Sacar',valor = valor)
                recebedor = dados[conta2]['Nome']
                print(f'Foi depositado {valor} na conta do(a) {recebedor}')
                return 'transferencia_concluida'
            if adicionando_transferencia(conta2,valor) == False:
                print(f'A conta {conta2} nao esta cadastrada em nosso sistema')
                return 'conta_nao_cadastrada'
            
        if i == str(conta1) and dados[i]['Saldo'] < valor:
            print(f'Saldo da conta {conta1} está abaixo de {valor}')
            return 'conta_pagadora_sem_saldo'
    print(f'Conta {conta1} não esta cadastrada em nosso sistema')
    return 'conta_pagadora_nao_cadastrada'

def extrato(conta):
    with open(ARQUIVO_DADOS,'r') as arquivo:
        dados= json.load(arquivo)
    for i in dados:
        if i == conta:
            extrato = dados[i]['extrato']
            print(extrato)
            return True
    print('conta nao cadastrada')
    return False

def perguntar_continuar():
    while True:
        r = input('\nGostaria de fazer mais alguma movimentação? (S/N)').lower().strip()
        if r in ('s', 'sim'):
            return True
        if r in ('n', 'nao'):
            print('Qualquer duvida estamos a disposição!\nAté Breve')
            return False
        print('Opção invalida')

def verificar_nome(nome):
    if not nome.replace(' ','').isalpha():
        print('\nSomente letras são permitidas no nome\n')
        return False
    return True

def verificar_conta(conta):
    try:
        int(conta)
        return True
    except ValueError:
        print('\nnumero de conta invalido\n\n')
        return False

def verificar_valor(valor):
    try:
        valor  = float(valor)
        if valor > 0 :
            return True
        else:
            print('\nentrada invalida, valido apenas numeros positivos\n')
            return False
    except ValueError:
        print('\nentrada invalida para deposito, utilize apenas numeros\n')
        return False   



if __name__ == '__main__':

    interaçoes = True
    while interaçoes:
        interacao_inicial = input('\nOque gostaria de fazer hoje:\n\n(1) Criar Conta\n(2) depositar\n(3) Sacar\n(4) Transferir\n(5) Extrato\n')

        match interacao_inicial:
            case '1':

                nome_check = True
                while nome_check:
                    nome = input('Para Abrir um conta digite seu nome completo:\n\n').strip()
                    if verificar_nome(nome):
                        nome_check = False
                    
                abrir = criar_conta(nome,0)
                if abrir == 'Nome_invalido':
                    print('Já existe um conta Aberta em seu Nome\n\n')
                    continue
                if abrir == 'Conta_criada':
                    if not perguntar_continuar():
                        interaçoes = False
                else:
                    print('Erro ao Executar')
                    continue
            case '2':
                nome_check = True
                while nome_check:
                    nome = input('\nPara realizar o deposito digite o seu nome cadastrado:\n').strip()
                    if verificar_nome(nome) == True:
                        nome_check = False

                conta_check = True
                while conta_check:
                    conta = input('\nDigite a conta de deposito:\n').strip()
                    if verificar_conta(conta) == True:
                        conta_check = False    
                
                valor_verificar = True
                while valor_verificar:
                    valor= input('\nQual valor gostaria de despositar:\n')

                    if verificar_valor(valor) == True:
                        valor_verificar = False    
                        valor = float(valor)

                abrir = depositar(nome,conta,valor)
                if abrir == 'Deposito_concluido':
                    if not perguntar_continuar(): 
                        interaçoes= False
                else:
                    print('Erro ao Executar')
                    continue
            case '3':
                nome_check = True
                while nome_check:
                    nome = input('\nPara realizar o deposito digite o seu nome cadastrado:\n').strip()
                    if verificar_nome(nome) == True:
                        nome_check = False

                conta_check = True
                while conta_check:
                    conta = input('\nDigite a conta de deposito:\n').strip()
                    if verificar_conta(conta) == True:
                        conta_check = False   

                valor_verificar = True
                while valor_verificar:
                    valor= input('\nQual valor gostaria de sacar:\n')
                    if verificar_valor(valor) == True:
                        valor = float(valor)
                        valor_verificar = False    

                abrir = sacar(nome,conta,valor)
                match abrir:
                    case 'Saque_concluido':
                        if not perguntar_continuar(): 
                                interaçoes= False    
                    case 'Sem_saldo':
                        continue
                    case 'Conta_not_found':
                        continue
                    case _:
                        print('Erro ao Executar')
                        continue              
            case '4':
                conta_check_pagadora = True
                while conta_check_pagadora:
                    conta_pagadora = input('\nDigite a conta pagadora:\n').strip()
                    if verificar_conta(conta_pagadora) == True:
                        conta_check_pagadora = False   

                conta_check_recebedora = True
                while conta_check_recebedora:
                    conta_Recebedor = input('\nDigite a conta recebedora :\n').strip()
                    if verificar_conta(conta_Recebedor) == True:
                        conta_check_recebedora= False   

                valor_verificar = True
                while valor_verificar:
                    valor= input('\nQual valor gostaria de Transferir:\n')
                    if verificar_valor(valor) == True:
                        valor_verificar = False    
                        valor = float(valor)

                abrir = transferir(conta_pagadora,conta_Recebedor,valor)
                match abrir:
                    case 'transferencia_concluida':
                        if not perguntar_continuar(): 
                            interaçoes= False
                    case 'conta_nao_cadastrada':
                        continue
                    case 'conta_pagadora_nao_cadastrada':
                        continue
                    case 'conta_pagadora_sem_saldo':
                        continue
                    case _:
                        print('erro na execução')
                        continue
            case '5':
                conta = input('\nDigite o numero da conta:\n').strip()
                if not verificar_conta(conta):
                    continue
                abrir = extrato(conta)
                match abrir:
                    case True:
                        if not perguntar_continuar(): 
                            interaçoes= False