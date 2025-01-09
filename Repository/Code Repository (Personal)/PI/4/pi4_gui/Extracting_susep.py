import requests
import pandas as pd
import os
import io

from bs4 import BeautifulSoup

def fetch_page(url):
    geted = requests.get(url, verify=False)

    return geted.text


def parse_page(html):
    soap = BeautifulSoup(html, 'html.parser')
    
    downloads_links = soap.find_all('a', class_="external-link")
    hrefs = [link['href'] for link in downloads_links]


    return hrefs

def filter_only_S(lista):

    Seguros_S = list()
    for i in lista:
        print(i[-16])
        if i[-16] == 's':
            Seguros_S.append(i)
            

    return Seguros_S

def cria_repository():

    os.makedirs('downloads_susep', exist_ok=True)

def downloads(hrefs, dir):
    for link in hrefs:
        try:
            print(f'Baixando: {link}')

            response = requests.get(link, stream=True)
            response = os.path.join(dir, os.path.basename())
        except Exception as e:
            return print(f'erro: {e}')

if __name__ == '__main__':
    url = "https://www.gov.br/susep/pt-br/central-de-conteudos/dados-estatisticos/bases-anonimizadas/bases_auto"
    request = fetch_page(url)
    print(request)
    links = parse_page(request)
    filtrados = filter_only_S(links)
    # print(filtrados)