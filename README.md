# Recipe Scraper

Recipe Dataset taken from https://www.recetasgratis.net/.

## Description and usage:

In order to run the code, write on to the console the following instructions:

python Scraper.py --category <food category|All> --stopAfter <number of recipes>
  
**--food category**  
You can either enter one of the following categories or 'All' for all categories:

|                         |                       |                               |
|-------------------------|-----------------------|-------------------------------|
| Canapés                 | Ensaladas saludables  | Espaguetis                    |
| Empanadas               | Ensaladas con frutas  | Pizza                         |
| Bocadillos y sándwiches | Ensaladas con pescado | Macarrones                    |
| Cremas para untar       | Ensaladas de pasta    | Lasaña                        |
| Risottos                | Guiso                 | Salmón                        |
| Paellas                 | Potajes               | Merluza                       |
| Arroces sueltos         | Cocido                | Atún                          |
| Arroces con carne       | Migas                 | Bacalao                       |
| Pollo                   | Tortillas             | Tartas                        |
| Pavo                    | Tortitas              | Postres con frutas            |
| Conejo                  | Queso                 | Flan                          |
| Pato                    | Huevos revueltos      | Helado                        |
| Cerdo                   | Garbanzos             | Salsas para carnes y verduras |
| Ternera                 | Lentejas              | Salsas rojas                  |
| Vaca                    | Alubias               | Salsas blancas                |
| Lomo                    | Frijoles              | Mayonesa                      |
| Batidos                 | Camarones             | Sopas                         |
| Cócteles                | Calamares             | Cremas                        |
| Jugos y zumos           | Langostinos           | Caldos                        |
| Ponche                  | Pulpo                 | Gazpachos                     |
| Trucos y técnicas       | Bizcochos             | Patata                        |
| Nutrición y salud       | Galletas              | Berenjena                     |
| Ideas para condimentar  | Pan                   | Otras verduras                |
| Consejos de compra      | Cupcakes              | Espinacas                     |


**--stopAfter**  
The number of queries you want to execute (~1 per recepie) or, alternatively, "None" to set no limits (will continue executing until there're no more elements to extract)

Example of use:

- *python Scraper.py --category Tortillas --stopAfter 10*
- *python Scraper.py --category All --stopAfter 10*
- *python Scraper.py --category All --stopAfter None* (This configuration is the one that extracts the entire recipes.csv dataset, it will take a long time to execute) 
