from PyPDF2 import PdfReader



def extract_text_boleto(file_path):
    """
    Extrai informações específicas de um boleto bancário de um arquivo PDF e retorna como uma tupla.
    
    Esta função processa a segunda página do PDF, procurando por padrões específicos de texto.
    
    :param file_path: Caminho do arquivo PDF a ser processado
    :return: Tupla contendo o texto da apólice e a vigência do boleto
    """
    
    reader = PdfReader(file_path)  # Cria um leitor do PDF
    
    try:
        page = reader.pages[2]  # Obtém a segunda página do PDF
        page_text = page.extract_text()  # Extrae o texto da página
        
        # Remove espaços em branco para facilitar a busca de padrões
        page_text = page_text.replace('\n', ' ')
        
        # Busca pelo texto da apólice
        match_apolice = re.search(r"(?<=CONTRATO:)(.*?)(?=PERÍODO)", page_text.replace(' ', ''))

        if match_apolice:
            apolice_text = match_apolice.group(1)  # Obtém o grupo correspondente ao padrão da apólice
        else:
            print("No match found")  # Mensagem de erro se não encontrar um match
        
        # Busca pelo texto da vigência
        match_vigencia = re.search(r"(?<=COMPETÊNCIA:)(.*?)(?=NOMEDOESTIPULANTE)", page_text.replace(' ', ''))

        if match_vigencia:
            vigencia_text = match_vigencia.group(1).replace('De', '').replace('até', ' - ')  # Modifica o formato do texto da vigência
        else:
            print("No match found")  # Mensagem de erro se não encontrar um match

    except IndexError:
        print("The specified page does not exist.")  # Trata o caso de uma página inválida

    return apolice_text, vigencia_text  # Retorna os textos extraídos como tupla
 
def extract_text_tables(file_path):
    """
    Extrai texto de tabelas de um arquivo PDF e retorna como uma string concatenada.
    
    Esta função processa todas as páginas do PDF, procurando por uma frase específica ("Anexo da Fatura")
    e capturando o texto subsequente até "RETROA TIVO (R$)".
    
    :param file_path: Caminho do arquivo PDF a ser processado
    :return: String concatenada contendo o texto extraído das tabelas
    """
    reader = PdfReader(file_path)  # Cria um leitor do PDF
    
    text_file = ''  # Variável para armazenar o texto extraído

    # Itera sobre cada página do PDF
    for p in range(len(reader.pages)):
        try:
            page = reader.pages[p]  # Obtém a página atual
            page_text = page.extract_text()  # Extrae o texto da página
            
            if page_text:  # Verifica se algum texto foi extraído
                if 'Anexo da Fatura' in page_text:  # Procura pela frase específica
                    captured_text = page_text.split('RETROA TIVO (R$)')[1]  # Divide o texto e captura o segmento após a frase específica
                    # Aqui estava um comentário removido que parecia estar tentando extrair informações específicas do texto
                    text_file += '\n' + captured_text  # Adiciona o texto capturado ao resultado final
        
        except IndexError:
            print("The specified page does not exist.")  # Trata o caso de uma página inválida

    return text_file  # Retorna o texto extraído como string concatenada
