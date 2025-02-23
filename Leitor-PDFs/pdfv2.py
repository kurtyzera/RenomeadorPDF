import PyPDF2
import os
import re

# Váriavel que define o começo do nome do documento neymar
inicioArquivo = "Termo de Equipamento -2025"

# Caminho pasta de arquivos, literalmente é o que define qual o caminho de tudo
caminho_pasta = r"C:\Users\killy\Downloads\Termos Onboarding Automate"

# Função extrair texto
def extrair_texto(caminho_arquivo):
    with open(caminho_arquivo, "rb") as arquivo:
        # Estou atribuindo o nome de leitor_pdf para essa função que le o arquivo pdf
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        # Defino o texto para vazio, para em seguida adicionar nele o texto do pdf. Faço isso apenas para criar o texto
        texto = ""
        # Aqui estou validando a questão das paginas. Ele vai pegar listar todas as paginas do PDF com o .pages, e depois e repetir para cada pagina por causa do loop "for"
        for pagina in leitor_pdf.pages:
            texto += pagina.extract_text()
        return texto

# Função extrair nome e sobrenome. Desculpa, mas realmente não entendi nada sobre RegEx... O deepseek fez isso pra mim (e nos meus testes, so consegui fazer com que funcionasse em dois arquivos, mas não em cinco. Parece que cada pdf tem um padrão diferente)
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

# Listar aquivos diretorio, usando a função listdir (como o nome diz, lista o diretorio). Por fim passo o parametro de qual diretorio quero listar, que no caso é o caminho_pasta
arquivos = os.listdir(caminho_pasta)

# Processar arquivos diretorio. O for vai percorrer todos os itens da lista de arquivos, que nos obtivemos no item anterior atravez do os.listdir
for arquivo in arquivos:
    # Aqui defino o "if" para iniciar quando o começo do nome do arquivo tiver a palavra ou frase que foi definida no inicio do código
    if arquivo.startswith(inicioArquivo):
        # Usamos a função os.path.join para que não tenhamos que digitar /, ja que ela pode variar dependendo do sistema operacional. ela vai juntar o caminho_pasta com o arquivo, algo como C:/CaminhoArquivo/arquivo.pdf. isso vai definir para o python o caminho de cada arquivo dentro daquela pasta, desde que todos iniciem com o nome "Zezin".
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        # O try não é necessario, mas foi adicionado para que possa nos retornar mensagens de erro ou sucesso no console. Sem eles, qualquer erro iria interromper a execução do codigo, garantindo que se algo de errado, o codigo não vá para pqp. No fim, usamos ele junto do except para que o except possa capturar erros, assim caso tenhamos algum erro, seremos redirecionados para parte do except, aonde nos apresentara um erro
        try:
            # Puxar o texto extraido. Definimos o parametro caminho_arquivo na função, para que ele puxe o caminho de cada arquivo, coisa que foi atribuida nas linhas de codigo anteriores
            texto = extrair_texto(caminho_arquivo)
            # Puxar o nome extraido. Primeiro definimos q o nome é o resultado da função que extrai apenas o nome do texto completo. Em seguida adicionamos "texto" de parametro na função, pq queremos q a função puxe o nome nos textos de cada arquivo.
            nome = extrair_nome(texto)
                
            # Se tiver nome no arquivo
            if nome:
                # Criar novo nome para o arquivo. O novo nome sera igual ao nome extraido e a frase final de "Termo Bla bla bla.pdf"
                novo_nome = f"{nome} Termo Onboarding 2025.pdf"
                # Define o novo caminho do arquivo. Vamos usar a mesma regra de antes (os.path.join para evitar incompatibilidade com diferentes OS, ja que ele une os dois atributos automaticamente e adiciona a / ou \ dependendo do OS). Após isso, definiremos o caminho, que sera o caminho_pasta + nome novo do arquivo, nos retornando algo como C:/CaminhoArquivo/aquivoNOVO.pdf. Esse passo é importante para dizer para o sistema operacional aonde ele deve salvar o nosso arquivo quando ele for renomeado.É OBRIGATORIO conter o nome novo do arquivo apos o caminho_pasta
                novo_caminho_arquivo = os.path.join(caminho_pasta, novo_nome)

                # Renomear arquivo. Simplesmente uma função que renomeia arquivo. Essa função precisa que o caminho completo dos arquivos de origem e destino. O primeiro nome sendo o caminho/nome antigo, e o segundo o caminho/nome novo
                os.rename(caminho_arquivo, novo_caminho_arquivo)

                # Mensagem de sucesso
                print(f'Arquivo renomeado com suceesso! {arquivo} >>> {novo_nome}')

            else:
                # Erro 1 caso não encontre o erro. Ele esta fora do except por esse erro não ocorrer dentro do try. Se esse erro ocorrer, foi por conta da função extrair_texto ou extrair_nome
                print(f'Nome não encontrado no arquivo: {arquivo}')

        except Exception as e:
            # Erro caso o try falhe na execução do codigo em algum momento
            print(f"Erro ao processar o arquivo {arquivo}: {e}")