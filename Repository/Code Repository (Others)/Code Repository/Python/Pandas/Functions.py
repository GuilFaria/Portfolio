def rename_columns(df: pd.DataFrame, others_dict : dict | None = None) -> pd.DataFrame:
    '''Renomeia as colunas do DataFrame a partir de uma limpeza de dados:
    1- é retirado os underlines, colocando space no lugar;
    2- é colocado Title, para que, em cada espaço, seja colocado uma letra maiuscula;
    3- Caso haja (Parâmetro opcional), algum valor a ser tratado de outra maneira, deve ser colocado na 'ignore_dict'.
    
    Args:
        df (pd.DataFrame): O DataFrame a ser modificado.
        others_dict (dict or None): Dicionário opcional contendo os valores a serem modificados de forma distinta.

    Returns:
        df (pd.DataFrame):
        Dataframe contendo as colunas renomeadas.
    '''
    
    renamed_dict = {}
    
    if not others_dict is None:
        for col in df.columns:
            if col not in others_dict.keys():
                renamed_dict[col] = col.replace('_', ' ').title().strip()
            else:
                renamed_dict[col] = others_dict.get(col)
    else:
        for col in df.columns:
            renamed_dict[col] = col.replace('_', ' ').title().strip()

    df = df.rename(columns=renamed_dict)
    
    return df
    
    
def rename_columnns_with_name_conventions(df: pd.DataFrame, name_convention: str | None = None, others_dict : dict | None = None, sep: str | str = ' ') -> pd.DataFrame:
    '''Renomeia as colunas do DataFrame de acordo com uma convenção a partir de uma limpeza de dados:
    1- é retirado os underlines, colocando space no lugar;
    2- é colocado Title, para que, em cada espaço, seja colocado uma letra maiuscula;
    3- Caso haja (Parâmetro opcional), algum valor a ser tratado de outra maneira, deve ser colocado na 'others_dict'.
    
    Args:
        - df (pd.DataFrame): O DataFrame a ser modificado.
        - name_convention (str or None, optional, default - None): O nome da convenção de nomenclatura a ser utilizada, exemplo:
            - 'snake', referindo-se ao Snake Case, com a formatação 'nome_da_coluna'
            - 'camel', referi-se ao Camel Case, com a formatação 'nomeDaColuna'
            - 'pascal', referindo-se ao Pascal Case, com a formatação 'NomeDaColuna'
            - 'kebab', refere-se ao Kebab Case, com a formatação 'nome-da-coluna'
        - others_dict (dict or None, optional, default - None): Dicionário opcional contendo os valores a serem modificados de forma distinta.
        - sep (str, optional, default - str ' '): separador do valores das colunas.
        

    Returns:
        df (pd.DataFrame):
        Dataframe contendo as colunas renomeadas.
    '''
    
    renamed_dict = {}
    if not name_convention:
        ##Normal Case
        
        if others_dict:
            for col in df.columns:
                if col not in others_dict.keys():
                    renamed_dict[col] = col.strip().replace(sep, ' ').title()
                else:
                    renamed_dict[col] = others_dict.get(col)
        else:
            for col in df.columns:
                renamed_dict[col] = col.strip().replace(sep, ' ').title()

        df = df.rename(columns=renamed_dict)
        
        return df
    
    else:
        
        match name_convention:
            
            ##Snake Case
            case 'snake':
                if others_dict:
                    for col in df.columns:
                        if col not in others_dict.keys():
                            renamed_dict[col] = col.strip().replace(sep, '_').lower()
                        else:
                            renamed_dict[col] = others_dict.get(col)
                else:
                    for col in df.columns:
                        renamed_dict[col] = col.strip().replace(sep, '_').lower()
                df = df.rename(columns=renamed_dict)
                
                return df
        
        
            ##Snake Case
            case 'camel':
                if others_dict:
                    for col in df.columns:
                        if col not in others_dict.keys():
                            words = col.strip().split(sep)
                            first_word = words[0].lower()

                            words.pop(0)

                            words_to_join = list(str(w).title() for w in words)
                            words = ''.join(words_to_join)

                            renamed_dict[col] = first_word + words
                            
                        else:
                            renamed_dict[col] = others_dict.get(col)
                else:
                    for col in df.columns:
                            words = col.strip().split(sep)
                            first_word = words[0].lower()

                            words.pop(0)

                            words_to_join = list(str(w).title() for w in words)
                            words = ''.join(words_to_join)

                            renamed_dict[col] = first_word + words
                            

                df = df.rename(columns=renamed_dict)
                
                return df
            
    
            ##Pascal Case
            case 'pascal':
                if others_dict:
                    for col in df.columns:
                        if col not in others_dict.keys():
                            renamed_dict[col] = col.strip().title().replace(sep, '')
                        else:
                            renamed_dict[col] = others_dict.get(col)
                else:
                    for col in df.columns:
                        renamed_dict[col] = col.strip().title().replace(sep, '')


                df = df.rename(columns=renamed_dict)
                
                return df
            
            
            ##Kebab Case
            case 'kebab':
                if others_dict:
                    for col in df.columns:
                        if col not in others_dict.keys():
                            renamed_dict[col] = col.strip().lower().replace(sep, '-')
                        else:
                            renamed_dict[col] = others_dict.get(col)
                else:
                    for col in df.columns:
                        renamed_dict[col] = col.strip().lower().replace(sep, '-')


                df = df.rename(columns=renamed_dict)
                
                return df
            
            case _: #Caso nenhum (equivalente a else)
                raise ValueError(f"Convenção de Nomenclatura inválida: {name_convention}. Por favor, escolha entre: camel, pascal, snake ou kebab.\nEm caso de não utilizar uma nomenclatura, passe None.")


def lista_valores(df: pd.DataFrame, col_ordem: str) -> list:
    '''Função que cria uma lista dos valores de uma coluna de
    um DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a ser analisado os valores.
        col_ordem (str): Nome da coluna a ser analisada.
    Returns:
        lista (list): lista de valores da Coluna do DataFrame.
    '''
    
    lista = df[col_ordem].drop_duplicates().to_list()
    
    return lista
    


def group_holders(df: pd.DataFrame, tipo: str, col_cod_geral: str, col_agr: str) -> pd.DataFrame:
    '''Função que agrupa os valores de um DataFrame por titulares.
    
    Args:
        df (pd.DataFrame): DataFrame a ser analisado os valores.
        tipo (str): Nome da coluna que representa a titularidade.
        col_cod_geral (str): Nome da coluna que contem o código geral
        col_agr (str): Nome da coluna que contem os valores a serem agrupados.
        
    Returns:
        df (pd.DataDrame): lista de valores da Coluna do DataFrame.
        s
    '''
    st.dataframe(df)
    df['Ordem'] = df[tipo].apply(lambda x: lista_valores(df, tipo).index(x))
    
    df = df.sort_values([col_cod_geral]).drop(columns=['Ordem'])

    df['Vidas'] = df.groupby([col_agr], as_index=False)[col_agr].transform('count')
    
    dict_cols = {col: ('sum' if col == 'Valor' else 'first') for col in df.columns}
    df_grouped = df.groupby([col_agr], as_index= False).agg(dict_cols)
    
    return df_grouped
   

   
def extrai_mensalidade(file_pdf):
#     dominio_planos = ["A. PLATINUM ML ECLA"]
    
#     reader = PdfReader(file_pdf)
#     first_page = reader.pages[0].extract_text().replace(' ', '|')
    
#     pos_ini = first_page.find("Nº|Funcional|")
#     first_page = first_page[pos_ini:len(first_page)]
#     pos_ini = first_page.find("Data|de|nasc.") +len("Data|de|nasc.")
#     first_page = first_page[pos_ini:len(first_page)].strip()
    
#     #print(first_page)    
    
#     arr_page = first_page.split("\n")
#     cnt = 0
#     arr_saida=[]
#     while cnt < len(arr_page):
#         if str('Total|').upper() in arr_page[cnt].upper():
#             pass
#         else:
#             arr_saida.append(arr_page[cnt])
#         cnt=cnt+1
#     del arr_page
#     #first_page = '\n'.join(arr_saida)
#     #print(first_page)
    
#     cnt = 0
#     while cnt < len(arr_saida):
#         list_values = []
        
#         str_aux = arr_saida[cnt].strip()
#         pos = str_aux.rfind("|")+1        
#         list_values.append(str_aux[pos:len(str_aux)])
#         str_aux = str_aux[0:pos-1]
        
#         pos = str_aux.rfind("|")+1
#         list_values.append(str_aux[pos:len(str_aux)])        
#         str_aux = str_aux[0:pos-1]
        
#         pos = str_aux.rfind("|")+1
#         list_values.append(str_aux[pos:len(str_aux)])        
#         str_aux = str_aux[0:pos-1]  
        
#         pos = str_aux.rfind("|")+1
#         list_values.append(str_aux[pos:len(str_aux)])
#         str_aux = str_aux[0:pos-1]                 
        
#         for aux_plano in dominio_planos:
#             aux_plano = aux_plano.replace(" ", "|")
#             pos = str_aux.rfind(aux_plano)
            
#             if pos > 0:
#                 list_values.append(aux_plano.replace("|", ' '))
#                 str_aux= str_aux[0:pos-1] + "|" + str_aux[(pos + len(aux_plano))+1:len(str_aux)]
#                 break 
        
        
        
#         num_funcional = ''
#         arr_aux = str_aux.split("|")
#         str_aux=''
#         cnt_aux = 0
        
#         while cnt_aux < len(arr_aux):
#             if len(arr_aux[cnt_aux]) == 5:
#                 try:
#                     list_values.append(int(arr_aux[cnt_aux]))
#                 except:
#                     pass                
#             else:
#                 str_aux = str_aux + arr_aux[cnt_aux] + "|"
#             cnt_aux=cnt_aux+1
#         str_aux = str_aux.replace("||","")
        
    
#         cnt_aux = 0
#         pos1 = str_aux[-1]
#         if pos1 == "|":
#             str_aux = str_aux[:-1]
#         arr_aux = str_aux.split("|")    
        
#         CPF = None
#         parentesco = None
#         Nome = ''
        
#         for item in arr_aux:
#             if item.isnumeric():
#                 CPF = item
#             else:
#                 if item in list_parentesco and parentesco is None:
#                     parentesco = item
#                     print('passou')
#                 else:
#                     Nome += item + ' '
#         list_values.append(CPF)
#         list_values.append(parentesco)
#         list_values.append(Nome)
        
#         # print(data_nasc)
#         # print(codigo)       
#         # print(valor)
#         # print(adesao)
#         # print(plano)
#         # print(num_funcional)
#         # print(CPF)
#         # print(parentesco)
#         # print(Nome)
#         # print('')
#         print(list_values)
        
#         cnt=cnt+1
    
#     #st.write(first_page)
#     #print(first_page)
#     lista_colunas = ['Data Nascimento', 'Código', 'Valor', 'Adesão', 'Plano', 'Número Funcional', 'CPF', 'Parentesco', 'Nome']
    
#     match_codigo = re.findall(r'(3).')
    
#     return None

def columns_convert_data(df : pd.DataFrame) -> pd.DataFrame:

    '''
    Converte todas as colunas, do tipo string, para um tipo específico de data: dd/mm/YYYY (formato brasileiro).
    A função tenta, em cada coluna, aplicar o formato de data.
    Em caso de insucesso, acaba passando a coluna.
    '''

    for column in df.columns:
        try:
            df[column] = pd.to_datetime(df[column], format='%d/%m/%Y')
        except (ValueError, TypeError):
            pass
    
    for column in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[column] = df[column].dt.strftime('%d/%m/%Y')
    
    return df 