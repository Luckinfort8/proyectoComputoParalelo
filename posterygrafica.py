import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import requests
from io import BytesIO
from PIL import Image


def create_poster(data, product_name, background_image_path):
    # Crear un DataFrame con los datos
    df = pd.DataFrame(data).T

    # Encontrar el producto con el precio más bajo
    # Crear un archivo PDF para guardar las figuras y el póster
    pdf_pages = PdfPages(f'posters/{product_name}_result_poster.pdf')

    # Crear el póster
    for key, item in data.items():
        poster = plt.figure(figsize=(8.5, 11), facecolor='black')  # Establecer el fondo en negro
        # Obtener las dimensiones de la imagen de fondo
        background_image = plt.imread(background_image_path)
        img_width, img_height = background_image.shape[1], background_image.shape[0]

        # Calcular las coordenadas para centrar la imagen de fondo en el póster
        x_center = int((8.5 * 72 - img_width) / 2)
        y_center = int((11 * 72 - img_height) / 2)

        # Agregar la imagen de fondo al póster
        poster.figimage(background_image, x_center, y_center, alpha=0.9)

        # Añadir la imagen, mensaje de oferta, precio y tienda al póster del producto más barato
        response = requests.get(item['image'])
        img = Image.open(BytesIO(response.content))

        # Calcular las coordenadas para colocar la imagen del producto
        x_img = 180  # Puedes ajustar esta posición
        y_img = 450  # Puedes ajustar esta posición

        # Añadir la imagen del producto al póster
        poster.figimage(img, x_img, y_img, alpha=1)
        plt.axis('off')
        plt.title(f'Oferta en {item["store"]}\nTipo{key}\nPrecio: {item["price"]}\n{item["name"]}', color='white',
                  fontsize=18)  # Cambiar el color del título a blanco
        pdf_pages.savefig(poster)  # Guardar la página del póster en el PDF

    # 1. Gráfica de caja por tamaño/presentación del producto
    plt.figure(figsize=(8.5, 11))
    df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    df.boxplot(column='price', by='store', vert=False)
    plt.title(f'Precios de {product_name} por tienda')
    plt.ylabel('Precio')
    plt.xlabel('Tienda')
    plt.tight_layout()
    pdf_pages.savefig()

    # 2. Gráfica de dispersión por tamaño/presentación
    df.sort_values(by='price', inplace=True)
    plt.figure(figsize=(8.5, 11))
    plt.scatter(df['store'], df['price'], c=range(len(df)), cmap='viridis', marker='o')
    plt.xticks(rotation=45)
    plt.title(f'Dispersión de precios de {product_name}')
    plt.xlabel('Tienda')
    plt.ylabel('Precio')
    plt.tight_layout()
    pdf_pages.savefig()

    # Guardar el PDF
    pdf_pages.close()
