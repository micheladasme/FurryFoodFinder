from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = Flask(__name__)

def buscar_alimento(url, selectors):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        resultado = soup.select_one(selectors['container'])
        if resultado:
            nombre_elemento = resultado.select_one(selectors['nombre'])
            precio_elemento = resultado.select_one(selectors['precio'])
            stock_elemento = resultado.select_one(selectors['stock'])

            nombre = nombre_elemento.text.strip() if nombre_elemento else 'No disponible'
            precio = precio_elemento.text.strip() if precio_elemento else 'No disponible'
            stock = stock_elemento.text.strip() if stock_elemento else 'No disponible'

            if 'agotado' in stock.lower() or 'fuera de stock' in stock.lower():
                stock = "Agotado"
            else:
                stock = "Con Stock"
            
            return {"nombre": nombre, "precio": precio, "stock": stock}
    
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_puntomascotas = None
    resultado_braloy = None
    resultado_petslandia = None
    resultado_tusmascotas = None
    resultado_tusmascotas_full = None
    resultado_novapet = None
    resultado_mlandia = None
    nombre_alimento = None

    if request.method == 'POST':
        nombre_alimento = request.form['nombre_alimento']
        nombre_alimento_mas = nombre_alimento.replace(" ", "+")
        nombre_alimento_codificado = quote_plus(nombre_alimento_mas)

        # Configuración de selectores para cada sitio web
        selectors_puntomascotas = {
            'container': "div.product-container.product-style.pg-epd.pg-eal.pg-evl.pg-bnl",
            'nombre': "h5.product-name",
            'precio': "span.price.product-price",
            'stock': "div.product-availability"
        }
        selectors_braloy = {
            'container': "article.product-miniature-default",
            'nombre': "h3.product-title",
            'precio': "span.product-price",
            'stock': "div.product-availability"
        }
        selectors_petslandia = {
            'container': "div.product-wrapper",
            'nombre': "h3.wd-entities-title",
            'precio': "span.amount",
            'stock': "div.product-labels.labels-rectangular"
        }
        selectors_tusmascotas = {
            'container': "div.product-grid-item",
            'nombre': "h3.wd-entities-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock"
        }
        selectors_tusmascotas_full = {
            'container': "div.product-image-summary.col-lg-12.col-12.col-md-12",
            'nombre': "h1.product_title.entry-title.wd-entities-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock"
        }
        selectors_novapet = {
            'container': "div.bs-collection__product.border",
            'nombre': "h3.bs-collection__product-title",
            'precio': "strong.bs-collection__product-final-price",
            'stock': "button.btn.btn-primary"
        }
        selectors_mlandia = {
            'container': "div.product-grid-item.product",
            'nombre': "h3.product-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock"
        }

        # Realizar búsquedas en los sitios web
        resultado_puntomascotas = buscar_alimento(f"https://puntomascotas.cl/buscar?controller=search&s={nombre_alimento_mas}", selectors_puntomascotas)
        resultado_braloy = buscar_alimento(f"https://braloy.cl/busqueda?controller=search&s={nombre_alimento_mas}", selectors_braloy)
        resultado_petslandia = buscar_alimento(f"https://www.petslandia.cl/?s={nombre_alimento_mas}&post_type=product", selectors_petslandia)
        resultado_tusmascotas = buscar_alimento(f"https://www.tusmascotas.cl/?s={nombre_alimento_mas}&post_type=product", selectors_tusmascotas)
        resultado_tusmascotas_full = buscar_alimento(f"https://www.tusmascotas.cl/?s={nombre_alimento_mas}&post_type=product", selectors_tusmascotas_full)
        resultado_novapet = buscar_alimento(f"https://www.novapet.cl/search?search_text={nombre_alimento_codificado}&limit=24&order=relevance&way=DESC", selectors_novapet)
        resultado_mlandia = buscar_alimento(f"https://mlandia.cl/?s={nombre_alimento_mas}&post_type=product", selectors_mlandia)

    return render_template('index.html', nombre=nombre_alimento, resultado_puntomascotas=resultado_puntomascotas, resultado_braloy=resultado_braloy, resultado_petslandia=resultado_petslandia, resultado_tusmascotas=resultado_tusmascotas,
    resultado_tusmascotas_full=resultado_tusmascotas_full, resultado_novapet=resultado_novapet, resultado_mlandia=resultado_mlandia)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
