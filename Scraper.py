import requests
from bs4 import BeautifulSoup


class RecipeScraper():

    def __init__(self):
        self.url = 'https://www.recetasgratis.net'
        self.data = []

    def __download_html(self, url):
        response = requests.get(url)
        html = response.content
        return html

    def __get_subcat_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        sc_links = []
        for link in soup.find_all('ul', attrs={'class': 'sub-categorias'}):
            subcat = link.find_all('a')
            l = []
            for sc in subcat:
                l.append(sc.get('href'))
            sc_links.append(l)

        return sc_links


    def __get_next_link(self, url):
        resp = requests.get(url)
        bs_recipes = BeautifulSoup(resp.content, 'html.parser')
        next_page = bs_recipes.find_all('a', attrs={'class': 'next ga', 'data-event': 'Paginador'})
        if len(next_page) > 0:
            next_page_link = next_page[0].get('href')
        else:
            next_page_link = []

        return next_page_link

    def __get_recipe_links(self, url):
        r_links = []
        response = requests.get(url)
        bs_recipes = BeautifulSoup(response.content, 'html.parser')
        anchors = bs_recipes.find_all('a', attrs={'class': 'titulo titulo--resultado'})
        for a in anchors:
            r_links.append(a['href'])

        return r_links


    def scrape(self):
        # Descarga html
        html = self.__download_html(self.url)
        bs = BeautifulSoup(html, 'html.parser')

        # Links de las subcategorias (canapes, empanadas,...)
        cat_links = self.__get_subcat_links(html)

        # para cada subcat se recogen los links de todas las recetas para cada página de la subcat
        recipe_links = []
        for cat in cat_links:
            for sc in cat:
                aux = sc
                while len(self.__get_next_link(aux)) > 0:
                    recipe_links.append(self.__get_recipe_links(aux))
                    aux = self.__get_next_link(aux)
                    print(aux)
        return recipe_links

    #def write_csv(self):

