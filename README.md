# Sistema Bancário em Python

Sistema de conta bancária via linha de comando com persistência em JSON. Permite criar contas, depositar, sacar, transferir entre contas e consultar extratos. Projeto construído como exercício de aprendizado, com validação de entrada e testes automatizados.

## O que faz

- Criar contas vinculadas a um titular
- Depositar valores em uma conta
- Sacar valores respeitando o saldo disponível
- Transferir valores entre duas contas (operação atômica — só acontece se origem tem saldo e destino existe)
- Consultar o extrato de movimentações de uma conta
- Persistir todos os dados em `dados.json` entre execuções

## Como rodar

Requer Python 3.10 ou superior (o projeto usa `match/case`, introduzido no 3.10).

1. Clone o repositório:

```
git clone https://github.com/cerolado/sistema-bancario-python.git
cd sistema-bancario-python
```

2. Antes da primeira execução, crie um arquivo `dados.json` na pasta do projeto com o conteúdo `{}` (um dicionário vazio).

3. Rode o programa:

```
python banco.py
```

4. Siga o menu interativo.

## Como rodar os testes

O projeto tem 13 testes automatizados cobrindo criação de contas, depósito, saque, transferência e as funções de validação.

1. Instale o pytest (se ainda não tiver):

```
python -m pip install pytest
```

2. Rode os testes:

```
python -m pytest test_banco.py -v
```

Saída esperada: `13 passed`.

## Estrutura do projeto

```
sistema-bancario-python/
├── banco.py          # Código principal: funções e menu interativo
├── test_banco.py     # Testes automatizados com pytest
├── .gitignore        # Arquivos ignorados pelo Git
└── README.md
```

## Tecnologias

- **Python 3.10+** — linguagem principal, com uso de `match/case`
- **json** (biblioteca padrão) — persistência de dados em arquivo
- **pytest** — framework de testes automatizados

## Decisões de design

- **Separação entre lógica e interface:** as funções de negócio (`criar_conta`, `depositar`, etc.) não contêm `input()`. Toda interação com o usuário acontece no bloco `if __name__ == '__main__'`. Isso permite testar as funções isoladamente.
- **Arquivo de dados parametrizado:** o nome do arquivo JSON vive em uma constante `ARQUIVO_DADOS` no topo do módulo, não espalhado pelo código. Os testes trocam essa constante por um arquivo próprio (`dados_test.json`) pra não poluir o banco real.
- **Códigos de retorno semânticos:** em vez de retornar `True`/`False`, as funções retornam strings como `'Conta_criada'`, `'Sem_saldo'` ou `'conta_pagadora_nao_cadastrada'`. Isso permite que o menu reaja de forma específica a cada caso.
- **Transferência atômica:** a transferência só retira da origem depois que confirma que o depósito no destino foi bem-sucedido.

## Limitações conhecidas

- **Depositar exige o nome do titular**, não só o número da conta. Em um sistema real, qualquer pessoa pode depositar na conta de outra pessoa sabendo só o número.
- **Não há autenticação por senha** para operações de saque e transferência. Em um sistema real, operações sensíveis exigiriam senha, não o nome do titular (que não é um segredo).
- **Numeração sequencial baseada em `len(dados) + 1`** quebra se contas forem removidas no futuro (ainda não há essa funcionalidade, mas é uma fragilidade).
- **Sem tratamento de arquivo inexistente:** se `dados.json` não existir, o programa quebra na primeira operação em vez de criar um banco vazio automaticamente.

## Próximas melhorias

- Adicionar camada de autenticação com senha para saques e transferências
- Tratar o caso de `dados.json` inexistente ou corrompido com `try/except`
- Permitir listar todas as contas e deletar contas
- Formatar valores monetários (R$ 1.234,56) nas mensagens
- Adicionar data/hora em cada transação no extrato

## O que aprendi construindo isto

- Aprofundei na utilização e no reaproveitamento de funções, usando um arquivo JSON como fonte de dados e funções para acessar e modificar o seu conteúdo.
- Cada função tem seu próprio escopo. Não dá pra criar uma única função que pega input do usuário, valida os dados e salva tudo junto — misturar essas responsabilidades deixa o código impossível de testar e difícil de reaproveitar.
- Loops podem passar silenciosamente mesmo quando têm bug: no meu caso, descobri que `>` e `>=` fazem diferença grande em comparações de saldo, e esse tipo de erro só aparece quando você testa o caso de limite exato.
- Tipos importam muito mais do que eu imaginava. Uma mesma informação pode ser `int` dentro do código e `string` depois de passar pelo JSON — e Python não avisa quando isso quebra uma comparação. Só vi o problema quando os testes automatizados falharam.