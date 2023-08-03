from flask import render_template, request, Blueprint
import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import quote_plus

main = Blueprint('main' , __name__)

def buscar_alimento(url, selectors):
    userAgent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=userAgent)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        resultado = soup.select_one(selectors['container'])
        if resultado:
            nombre_elemento = resultado.select_one(selectors['nombre'])
            precio_elemento = resultado.select_one(selectors['precio'])
            stock_elemento = resultado.select_one(selectors['stock']) if selectors['stock'] else ''
            url_elemento = resultado.select_one(selectors['url'])

            nombre = nombre_elemento.text.strip() if nombre_elemento else 'Sin Informacion'
            precio = precio_elemento.text.strip() if precio_elemento else 'Sin Informacion'
            stock = stock_elemento.text.strip() if stock_elemento else 'Sin Informacion'
            url_product = url_elemento['href'] if url_elemento else ''

            if 'agotado' in stock.lower() or 'fuera de stock' in stock.lower() or 'sin stock' in stock.lower():
                stock = "Agotado"
            else:
                stock = "Con Stock"
            
            return {"shop":selectors['shop'], "nombre": nombre, "precio": precio, "stock": stock, "url": url_product }
        
    return None

@main.route('/', methods=['GET', 'POST'])
def index():
    resultado_puntomascotas = None
    resultado_braloy = None
    resultado_petslandia = None
    resultado_tusmascotas = None
    resultado_tusmascotas_full = None
    resultado_novapet = None
    resultado_mlandia = None
    resultado_mlandia_full = None
    resultado_gpet = None
    resultado_dgppet = None
    resultado_stgopet = None
    resultado_lira = None
    resultado_lira_full = None
    resultado_faunimals = None
    resultado_manchasSofi = None
    nombre_alimento = None

    if request.method == 'POST':
        nombre_alimento = request.form['nombre_alimento']
        nombre_alimento_codificado = urllib.parse.quote(nombre_alimento)
        nombre_alimento_mas = nombre_alimento.replace(" ", "+")
        nombre_alimento_mas_codificado = quote_plus(nombre_alimento_mas)
        nombre_codificado_safe_plus = urllib.parse.quote(nombre_alimento_mas, safe='+')
        nombre_alimento_mas_cast_y = nombre_alimento_mas.replace("&", "y")
        # Configuración de selectores para cada sitio web
        selectors_puntomascotas = {
            'shop': "PuntoMascotas",
            'container': "article.product-miniature.js-product-miniature",
            'nombre': "h5.product-name",
            'precio': "span.price.product-price",
            'stock': "div.product-availability",
            'url': "a.btn.add-to-cart.details-link"
        }
        selectors_braloy = {
            'shop': "Braloy",
            'container': "article.product-miniature-default",
            'nombre': "h3.product-title",
            'precio': "span.product-price",
            'stock': "div.product-availability",
            'url': "a.btn.btn-product-list"
        }
        selectors_petslandia = {
            'shop': "Petslandia",
            'container': "div.product-wrapper",
            'nombre': "h3.wd-entities-title",
            'precio': "span.amount",
            'stock': "div.product-labels.labels-rectangular",
            'url': "a.product-image-link"
        }
        selectors_petslandia_full = {
            'shop': "Petslandia 2",
            'container': "div.container-fluid",
            'nombre': "h1.product_title.entry-title.wd-entities-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "p.stock.out-of-stock",
            'url': "x"
        }
        selectors_tusmascotas = {
            'shop': "TusMascotas",
            'container': "div.product-grid-item",
            'nombre': "h3.wd-entities-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock",
            'url': "a.product-image-link"
        }
        selectors_tusmascotas_full = {
            'shop': "TusMascotas 2",
            'container': "div.container-fluid",
            'nombre': "h1.product_title.entry-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock.product-label",
            'url': "x"
        }
        selectors_novapet = {
            'shop': "Novapet",
            'container': "div.bs-collection__product.border",
            'nombre': "h3.bs-collection__product-title",
            'precio': "strong.bs-collection__product-final-price",
            'stock': "button.btn.btn-primary",
            'url': "a.bs-collection__product-info"
        }
        selectors_mlandia = {
            'shop': "Mlandia",
            'container': "div.product-grid-item.product",
            'nombre': "h3.product-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock",
            'url': "a.product-image-link"
        }
        selectors_mlandia_full = {
            'shop': "Mlandia 2",
            'container': "div.row.product-image-summary-wrap",
            'nombre': "h1.product_title.entry-title",
            'precio': "ins",
            'stock': "p.stock.out-of-stock",
            'url': "x"
        }
        selectors_gpet = {
            'shop': "Gpet",
            'container': "td.oe_product",
            'nombre': "h6.o_wsale_products_item_title",
            'precio': "span.oe_currency_value",
            'stock': "span.out-of-stock",
            'url': "a.tp-link-dark"
        }
        selectors_dgppet = {
            'shop': "De Gatos y Perros",
            'container': "div.row.bs-collection",
            'nombre': "h3.bs-collection__product-title",
            'precio': "strong.bs-collection__product-final-price",
            'stock': "div.bs-collection__product-stock",
            'url': "a.bs-collection__product-info"
        }
        selectors_stgopet = {
            'shop': "Stgopet",
            'container': "div.row.products-category",
            'nombre': "h4",
            'precio': "p.price",
            'stock': "",
            'url': "a"
        }
        selectors_lira = {
            'shop': "Distribuidora Lira",
            'container': "div.shop-container",
            'nombre': "a.woocommerce-LoopProduct-link.woocommerce-loop-product__link",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "div.out-of-stock-label",
            'url': "a.woocommerce-LoopProduct-link"
        }
        selectors_lira_full = {
            'shop': "Distribuidora Lira 2",
            'container': "div.product-info.summary",
            'nombre': "h1.product-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "p.stock.out-of-stock",
            'url': "x"
        }
        selectors_faunimals = {
            'shop': "Faunimals",
            'container': "div.d-flex.col-sm-6.col-md-3.text-center",
            'nombre': "h6.text-truncate",
            'precio': "div.bs-product-final-price",
            'stock': "",
            'url': "a"
        }
        selectors_manchasSofi = {
            'shop': "Las Manchas de Sofi",
            'container': "div.products.elements-grid.wd-products-holder",
            'nombre': "h3.wd-entities-title",
            'precio': "span.woocommerce-Price-amount.amount",
            'stock': "span.out-of-stock.product-label",
            'url': "a.product-image-link"
        }

        # Realizar búsquedas en los sitios web
        
        resultado_puntomascotas = buscar_alimento(f"https://puntomascotas.cl/buscar?controller=search&s={nombre_codificado_safe_plus}", selectors_puntomascotas)
        resultado_braloy = buscar_alimento(f"https://www.braloy.cl/busqueda?controller=search&s={nombre_alimento_mas_cast_y}", selectors_braloy)
        resultado_petslandia = buscar_alimento(f"https://www.petslandia.cl/?s={nombre_alimento_mas}&post_type=product", selectors_petslandia)
        resultado_tusmascotas = buscar_alimento(f"https://www.tusmascotas.cl/?s={nombre_alimento_mas}&post_type=product", selectors_tusmascotas)
        resultado_tusmascotas_full = buscar_alimento(f"https://www.tusmascotas.cl/?s={nombre_alimento_mas}&post_type=product", selectors_tusmascotas_full)
        resultado_novapet = buscar_alimento(f"https://www.novapet.cl/search?search_text={nombre_alimento_mas_codificado}&limit=24&order=relevance&way=DESC", selectors_novapet)
        resultado_mlandia = buscar_alimento(f"https://mlandia.cl/?s={nombre_alimento_mas}&post_type=product", selectors_mlandia)
        resultado_mlandia_full = buscar_alimento(f"https://mlandia.cl/?s={nombre_alimento_mas}&post_type=product", selectors_mlandia_full)
        resultado_gpet = buscar_alimento(f"https://gpet.cl/shop?search={nombre_alimento_mas}", selectors_gpet)
        resultado_dgppet = buscar_alimento(f"https://www.dgppet.cl/search?search_text={nombre_alimento_mas_codificado}&limit=12&order=relevance&way=DESC", selectors_dgppet)
        resultado_stgopet = buscar_alimento(f"https://www.santiagopetstore.cl/tienda/index.php?route=product/search&search={nombre_alimento_codificado}", selectors_stgopet)
        resultado_lira = buscar_alimento(f"https://www.distribuidoralira.cl/?product_cat=&s={nombre_alimento_mas}&post_type=product", selectors_lira)
        resultado_lira_full = buscar_alimento(f"https://www.distribuidoralira.cl/?product_cat=&s={nombre_alimento_mas}&post_type=product", selectors_lira_full)
        resultado_faunimals = buscar_alimento(f"https://www.faunimals.com/search?search_text={nombre_alimento_mas_codificado}&limit=24&order=relevance&way=DESC&page=1", selectors_faunimals)
        resultado_manchasSofi = buscar_alimento(f"https://lasmanchasdesofi.cl/?s={nombre_alimento_mas}&post_type=product", selectors_manchasSofi)

    return render_template('index.html', nombre=nombre_alimento, resultado_puntomascotas=resultado_puntomascotas, resultado_braloy=resultado_braloy, resultado_petslandia=resultado_petslandia, resultado_tusmascotas=resultado_tusmascotas,
    resultado_tusmascotas_full=resultado_tusmascotas_full, resultado_novapet=resultado_novapet, resultado_mlandia=resultado_mlandia, resultado_mlandia_full=resultado_mlandia_full, resultado_gpet=resultado_gpet, resultado_dgppet=resultado_dgppet, resultado_stgopet=resultado_stgopet, 
    resultado_lira=resultado_lira, resultado_lira_full=resultado_lira_full, resultado_faunimals=resultado_faunimals, resultado_manchasSofi=resultado_manchasSofi)

