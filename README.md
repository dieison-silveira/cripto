# Cifra de Substituição Homófona

Este projeto implementa um algoritmo de criptografia por substituição homófona, utilizando derivação de chave com PBKDF2. O script permite criptografar e descriptografar arquivos de texto.

## O Algoritmo 

Foi implementada uma cifra de substituição homófona, onde:
- Os caracteres do texto original são substituídos por um código numérico.
- Cada caractere tem múltiplos códigos possíveis (homófonos), escolhidos aleatoriamente na cifragem.
- Na decifragem, os códigos são revertidos para o caractere original com base em um dicionário salvo.

A chave de substituição é gerada a partir da senha do usuário com o algoritmo PBKDF2-HMAC-SHA256 e um salt aleatório.

### Requisitos do sistema

- Sistema operacional Windows ou Linux
- Python 3 instalado
- Instalar a biblioteca `cryptography`:
```bash
pip install cryptography
```

## Como executar

Você pode usar o comando `python` ou `py`, dependendo da configuração do seu ambiente.

### Execução do script (Windows ou Linux)

```bash
python main.py <arquivo.txt> <senha> <criptografar|decriptografar>
```

Ou, no Windows, caso `python` esteja apontando para outra versão, use:

```bash
py main.py <arquivo.txt> <senha> <criptografar|decriptografar>
```

### Exemplos:

**Para criptografar:**

```bash
python main.py teste.txt minha_senha criptografar
```

Isso gera os arquivos:
- `teste_cifrado.txt`
- `teste_dicionario.json` (contém salt e dicionário para decifragem)

**Para descriptografar:**

```bash
python main.py teste_cifrado.txt minha_senha decriptografar
```

Isso gera:
- `teste_decifrado.txt`

## Estrutura dos arquivos

- `main.py`: script principal com toda a lógica de cifragem/decifragem
- `arquivo_cifrado.txt`: texto criptografado
- `arquivo_dicionario.json`: contém o dicionário e o salt necessário para decifrar
- `arquivo_decifrado.txt`: resultado final após decifragem

## Observações

- A senha e o salt são usados para garantir que o mesmo texto e senha sempre gerem o mesmo dicionário.
- É essencial não apagar o arquivo `.json` gerado durante a cifragem, pois ele é necessário para decifrar.
- O script aceita qualquer caractere UTF-8, inclusive acentos e símbolos.

## Estudante

- Aluna: Ana Paula Ferreira Pelluzo  
- Instituição: Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Sul 
- Disciplina: Segurança da Informação  
- Professor: Dieison Silveira
