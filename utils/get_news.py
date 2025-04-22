import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import dotenv
import os

def limpiar_contenido(texto: str) -> str:
    """
    Clean the extracted content by removing unwanted elements and formatting.
    """
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'via Getty Images.*$', '', texto)
    texto = re.sub(r'^[Bb]y\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*', '', texto)
    texto = re.sub(r'\n.{1,10}\n', '\n', texto)
    return texto.strip()


def extraer_contenido_html(html: str) -> str:
    """
    Extract the main content from the HTML of a news article. Not so clean but works for most cases.
    """
    soup = BeautifulSoup(html, 'html.parser')

    possible_selectors = [
        'article',
        'div[itemprop="articleBody"]',
        'div[class*="article"]',
        'section[class*="content"]',
        'div[class*="story"]',
        'main',
        'div[role="main"]',
        'div[class*="text"]',
    ]

    containers = soup.select(','.join(possible_selectors))
    container = max(containers, key=lambda c: len(c.find_all('p')), default=None)

    def limpiar_parrafos(parrafos):
        vistos = set()
        limpios = []
        for p in parrafos:
            texto = p.get_text().strip()
            if len(texto) >= 40 and texto not in vistos:
                limpios.append(texto)
                vistos.add(texto)
        return limpios

    if container:
        parrafos = limpiar_parrafos(container.find_all('p'))
    else:
        parrafos = limpiar_parrafos(soup.find_all('p'))

    return '\n'.join(parrafos)


def obtener_articulos(query: str, api_key: str, page_size: int, from_date: str, max_articulos: int = 10) -> list:
    """
    Fetch articles from the News API based on the query and date range.
    """
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&from={from_date}&pageSize={page_size}"
        f"&sortBy=publishedAt&apiKey={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return []

    articles = data.get("articles", [])
    resultados = []

    for article in articles:
        try:
            raw_html = requests.get(article["url"]).text
            contenido = extraer_contenido_html(raw_html)
            if contenido:
                contenido_limpio = limpiar_contenido(contenido) #[:1250]
                resultados.append({
                    "title": article.get("title"),
                    "content": contenido_limpio,
                    "source": article.get("source", {}).get("name", "Desconocido"),
                    "url": article.get("url"),
                })
                if len(resultados) >= max_articulos:
                    break
        except Exception as e:
            print(f"No se pudo procesar {article['url']}: {e}")

    print(f"Se encontraron {len(resultados)} artículos relevantes para '{query}'.")
    return resultados


def get_news(queries: list[str], page_size: int = 20, from_days: int = 7) -> list[dict]:
    """
    Fetch news articles based on the provided queries and date range.
    """

    dotenv.load_dotenv('.env')
    api_key = os.getenv("API_KEY_NEWSAPI")

    from_date = (datetime.now() - timedelta(days=from_days)).strftime("%Y-%m-%d")

    todas_las_noticias = []
    for query in queries:
        print(f"\nBuscando noticias para: '{query}' desde {from_date}...")
        noticias = obtener_articulos(query, api_key, page_size, from_date)
        todas_las_noticias.extend(noticias)

    return todas_las_noticias
