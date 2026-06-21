
import os
import sys
import json
import random
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Gera uma chave criptográfica derivada da senha e salt usando PBKDF2
def gerar_chave_pbkdf2(senha, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Tamanho da chave (32 bytes)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return chave.decode()

# Gera um dicionário de substituição homófona baseado na chave derivada
def gerar_dicionario_com_chave(caracteres_unicos, chave_derivada, opcoes=3):
    caracteres = sorted(set(caracteres_unicos))
    dicionario = {}
    codigo = 1000  # Ponto de partida para os códigos
    seed = int(hashlib.sha256(chave_derivada.encode()).hexdigest(), 16)  # Semente determinística
    rng = random.Random(seed)  # Gera números aleatórios baseados na semente

    for c in caracteres:
        codigos = [str(codigo + i) for i in range(opcoes)]  # Cria N códigos para cada caractere
        rng.shuffle(codigos)  # Embaralha para não manter ordem previsível
        dicionario[c] = codigos
        codigo += opcoes
    return dicionario

# Cifra o texto, escolhendo aleatoriamente um dos códigos possíveis para cada caractere
def cifrar(texto, dicionario):
    return ' '.join(random.choice(dicionario[c]) if c in dicionario else c for c in texto)

# Inverte o dicionário para descriptografar (código → caractere original)
def inverter_dicionario(dicionario):
    invertido = {}
    for letra, codigos in dicionario.items():
        for cod in codigos:
            invertido[cod] = letra
    return invertido

# Decifra o texto cifrado, revertendo os códigos para os caracteres originais
def decifrar(texto, dicionario):
    invertido = inverter_dicionario(dicionario)
    codigos = texto.strip().split()  # Divide os códigos cifrados por espaço
    return ''.join(invertido.get(cod, '?') for cod in codigos)  # Usa '?' caso código não exista

# Função principal: trata leitura de arquivos, argumentos e controla o fluxo de operação
def main():
    if len(sys.argv) != 4:
        print("Uso correto: python main.py <arquivo.txt> <senha> <criptografar|decriptografar>")
        return

    nome_arquivo, senha, modo = sys.argv[1], sys.argv[2], sys.argv[3]

    if not os.path.isfile(nome_arquivo):
        print(f"Erro: arquivo '{nome_arquivo}' não encontrado.")
        return

    # Modo de criptografia
    if modo == "criptografar":
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            texto = f.read()

        salt = os.urandom(16)  # Gera salt aleatório
        chave = gerar_chave_pbkdf2(senha, salt)  # Deriva chave
        caracteres_unicos = ''.join(sorted(set(texto)))  # Extrai os caracteres únicos do texto
        dicionario = gerar_dicionario_com_chave(caracteres_unicos, chave)  # Gera dicionário de cifragem
        texto_cifrado = cifrar(texto, dicionario)  # Cifra o texto

        nome_saida = nome_arquivo.replace(".txt", "_cifrado.txt")
        with open(nome_saida, "w", encoding="utf-8") as f:
            f.write(texto_cifrado)

        # Salva o dicionário e salt para futura decifragem
        dados_dicionario = {
            "dicionario": dicionario,
            "caracteres_unicos": caracteres_unicos,
            "salt": base64.b64encode(salt).decode()
        }

        with open(nome_arquivo.replace(".txt", "_dicionario.json"), "w", encoding="utf-8") as f:
            json.dump(dados_dicionario, f, ensure_ascii=False, indent=2)

        print(f"Arquivo cifrado salvo como: {nome_saida}")

    # Modo de decriptografia
    elif modo == "decriptografar":
        if "_cifrado.txt" not in nome_arquivo:
            print("Erro: nome do arquivo para decifrar deve terminar com '_cifrado.txt'")
            return

        nome_base = nome_arquivo.replace("_cifrado.txt", "")
        dict_file = f"{nome_base}_dicionario.json"

        if not os.path.isfile(dict_file):
            print(f"Erro: dicionário '{dict_file}' não encontrado.")
            return

        with open(nome_arquivo, "r", encoding="utf-8") as f:
            texto_cifrado = f.read()

        with open(dict_file, "r", encoding="utf-8") as f:
            dados = json.load(f)

        dicionario_salvo = dados["dicionario"]
        caracteres_unicos = dados["caracteres_unicos"]
        salt = base64.b64decode(dados["salt"])

        chave = gerar_chave_pbkdf2(senha, salt)  # Recria chave
        dicionario_reconstruido = gerar_dicionario_com_chave(caracteres_unicos, chave)

        # Verifica se a senha é correta comparando os dicionários
        if json.dumps(dicionario_reconstruido, sort_keys=True) != json.dumps(dicionario_salvo, sort_keys=True):
            print("Erro: senha incorreta. Não foi possível decifrar.")
            return

        texto_decifrado = decifrar(texto_cifrado, dicionario_salvo)  # Decifra o texto
        nome_saida = nome_arquivo.replace("_cifrado.txt", "_decifrado.txt")
        with open(nome_saida, "w", encoding="utf-8") as f:
            f.write(texto_decifrado)

        print(f"Arquivo decifrado salvo como: {nome_saida}")

    else:
        print("Erro: modo deve ser 'criptografar' ou 'decriptografar'")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
