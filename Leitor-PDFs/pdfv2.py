import PyPDF2
import os
import re

inicioArquivo = "Termo de Equipamento -2025"

# Caminho pasta de arquivos
caminho_pasta = r"C:\Users\killy\Downloads\Termos Onboarding Automate"

# Função extrair texto
def extrair_texto(caminho_arquivo):
    with open(caminho_arquivo, "rb") as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in leitor_pdf.pages:
            texto += pagina.extract_text()
        return texto

# Função extrair nome e sobrenome. Desculpa, mas realmente não entendi nada sobre RegEx... O deepseek fez isso pra mim
def extrair_nome(texto):
    # Padrão para capturar a parte do e-mail antes do @
    padrao_nome = r"([a-zA-Z0-9_.+-]+)@c6bank\.com"
    match = re.search(padrao_nome, texto, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # Retorna apenas a parte antes do @
    return None


# Função para sanitizar o nome do arquivo
def sanitizar_nome(nome):
    # Remove caracteres inválidos para nomes de arquivos
    nome = re.sub(r'[\\/*?:"<>|\n]', '', nome)
    return nome.strip()

# Listar aquivos diretorio.
arquivos = os.listdir(caminho_pasta)

# Processar arquivos diretorio.
for arquivo in arquivos:
    if arquivo.startswith(inicioArquivo):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        try:
            texto = extrair_texto(caminho_arquivo)
            nome = extrair_nome(texto)
            
            if nome:
                 # Criar novo nome para o arquivo.
                novo_nome = f"{nome} Termo Onboarding 2025.pdf"
                # Define o novo caminho do arquivo.
                novo_caminho_arquivo = os.path.join(caminho_pasta, novo_nome)

                # Renomear arquivo
                os.rename(caminho_arquivo, novo_caminho_arquivo)

                # Mensagem de sucesso
                print(f'Arquivo renomeado com suceesso! {arquivo} >>> {novo_nome}')

            else:
                # Erro 1 caso não encontre o erro
                print(f'Nome não encontrado no arquivo: {arquivo}')

        except Exception as e:
            # Erro caso o try falhe na execução do codigo em algum momento
            print(f"Erro ao processar o arquivo {arquivo}: {e}")