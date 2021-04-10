import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time
import random
import numpy as np

start_time = time.time()

# Run code from console (example): python scraper.py --category Tortillas --stopAfter None
parser = argparse.ArgumentParser()
parser.add_argument('--category', help='Dish category to fetch the data', nargs='+')
parser.add_argument('--stopAfter', help='Maximum number of queries to process')
args = parser.parse_args()
category = ' '.join(args.category)


# Function to pull html code from website and convert it to BeautifulSoup object
def fetch_web(url):

    """
    Fetch the html code from url and convert it to BeautifulSoup object.

    :return: BeautifulSoup object
    """

    source = requests.get(url).content
    return BeautifulSoup(source, 'html.parser')

# Function to get the next page from the different pages of recipes
def get_next_page(url):

    """
    Take a url's page  and fetch next url's page.

    :return:  next url
    """

    resp = requests.get(url)
    bs_recipes = BeautifulSoup(resp.content, 'html.parser')
    next_page = bs_recipes.find_all('a', attrs={'class': 'next ga', 'data-event': 'Paginador'})
    if len(next_page) > 0:
        next_page_link = next_page[0].get('href')
    else:
        next_page_link = []
    return next_page_link


# Url get-go
soup = fetch_web('https://www.recetasgratis.net/')

# List to store all food categories and their url directions
names_webs = []

# Find all sub-categories (food categories) also containing their respective url
for frame in soup.find_all('ul', class_='sub-categorias'):
    sc_frame = frame.find_all('a')
    for sc in sc_frame:
        names_webs.append(
            sc.text.split('\n') + sc.get('href').split()
        )

# Convert names_webs list into pandas df
df_links = pd.DataFrame(names_webs, columns=['Item', 'Link'])

# Fetch category argument from agruments passed on the command line, and make it lower case letter
search_for = category

# Try to extract the category the user is searching for and store its link in variable extracting_page

if category != "All":
    try:
        # df_links = df_links.loc[df_links['Item'] == search_for, 'Link']
        match = df_links.loc[:, 'Item'] == search_for
        df_links = df_links.loc[match]
        print('Category {}, found! Fetching recipes...'.format(search_for))

    # If exception is risen inform the user and break the program
    except:
        print(
            'Oops! The type of dish you\'re searching for doesn\'t seems to be'
            'in our database. \nPlease also make sure the element you\'re searching for'
            'is correctly tiped in')

# Fetch stopAfter argument from agruments passed on the command line, and make it integer
if args.stopAfter == "None":
    stop_at = args.stopAfter
else:
    stop_at = int(args.stopAfter)

recipe_links = []

for page in df_links['Link']:
    # recipe_links.append(page)
    aux = page
    soup = fetch_web(aux)
    for a in soup.find_all('a', attrs={'class': 'titulo titulo--resultado'}):
        recipe_links.append(a['href'])
        while len(get_next_page(aux)) > 0:
            aux = get_next_page(aux)
            soup2 = fetch_web(aux)
            for anchor in soup2.find_all('a', attrs={'class': 'titulo titulo--resultado'}):
                recipe_links.append(anchor['href'])

if stop_at != "None":
    recipe_links = random.sample(recipe_links, stop_at)

count = 0
data = []
n = len(recipe_links)
for l in recipe_links:
    print(l)
    if l != "":
        count = count + 1
        print("Recipe {} of {}.".format(count, n))
        soup_2 = fetch_web(l)
        # Recipe's url
        recepe_site = l
        # Recipe's directions
        recipe_instructions = ''
        # Recipe's ingredients
        recipe_ingredients = ''

        # Recipe author's name (taken from recipe's url)
        try:
            recipe_author = soup_2.find('div', attrs={'class': 'nombre_autor'}).a.text
        except:
            recipe_author = None

        recipe_aux = []
        for ul in soup_2.find_all('ul', attrs={'class': 'breadcrumb mobile'}):
            for li in ul.find_all('li'):
                recipe_aux.append(li.text)
            # Recipe's category
            recipe_category = recipe_aux[1]
            # Recipe's sub-category
            recipe_subcategory = recipe_aux[2]
            # Recipe's name
            recipe_title = recipe_aux[3]

        ## Find all recipe's ingredients and add them to recipe_ingredients's string
        try:
            for ing in soup_2.find_all('li', class_='ingrediente'):
                ingredients = ing.text.split('\n')
                ingredients = [i for i in ingredients if i != '']
                recipe_ingredients = recipe_ingredients + ingredients[0]  # + ' \n '
        except:
            recipe_links = None

        # Find all recipe's directions and add them to recipe_instructions's string
        for recipe in soup_2.find_all('div', class_='apartado'):

            # Split instruction test by line space (different steps)
            content = recipe.text.split('\n')
            # Join the different steps dismissing empty lines
            directions = '- '.join([i for i in content if i != ''])
            # All recipe steps starts with a number, or else we know it is not an step therefore ditch

            if directions.startswith(
                    tuple(str(i) for i in range(50))
            ):
                # Combine all instruction into one string (already created --> recipe_instructions)
                recipe_instructions = recipe_instructions + directions  # + ' \n '
        # Create future df rows by adding extracted variables to list (later transform into df)
        row = [
            recipe_title, recipe_author, recipe_category, recipe_subcategory, recipe_ingredients,
            recipe_instructions, recepe_site
        ]
        # Append variables to our previously created list [[row_1],[row_2]...]
        data.append(row)
    else:
        continue

print('Creating csv with the recipes extracted, a total of {} recipes were found!'.format(len(data)))

# Transform our data list into dataframe

dataBase_out = pd.DataFrame(
    data, columns=[
        'Dish_Title', 'Recipe_author', 'Recipe_category', 'Recipe_subcategory', 'Recipe_ingredients',
        'Recipe', 'Source'
    ]
)

print(dataBase_out)
# Export dataframe into a csv file (recipes.csv) and save
# np.savetxt('recipes.txt', dataBase_out)

dataBase_out.to_csv('recipes.csv',  index=False, encoding='utf-8', sep=";")

print('CSV file successfully created and saved!')
print("--- %s seconds ---" % (time.time() - start_time))
