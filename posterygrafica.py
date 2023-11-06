import pickle
import matplotlib.pyplot as plt
from niceposter import Poster

# Cargar los diccionarios desde los archivos
best_items = []
product_names = ['television', 'laptop']  # Asegúrate de tener los nombres correctos aquí

for product_name in product_names:
    with open(f'{product_name}_data.pkl', 'rb') as file:
        data = pickle.load(file)
        best_items.append((product_name, data))

# Gráficas y pósters para cada producto
for product_name, data in best_items:
    # 1. Gráfica de caja por tamaño/presentación del producto
    plt.figure(figsize=(8, 6))
    plt.boxplot([float(item['price']) for item in data.values()])
    plt.xticks(range(1, len(data) + 1), data.keys(), rotation=45)
    plt.title(f'Precios de {product_name} por tamaño/presentación')
    plt.ylabel('Precio')
    plt.xlabel('Tamaño/Presentación')
    plt.tight_layout()
    plt.savefig(f'{product_name}_boxplot.png')
    plt.show()

    # 2. Gráfica de dispersión por tamaño/presentación
    prices = [float(item['price']) for item in data.values()]
    sizes = list(data.keys())

    plt.figure(figsize=(10, 6))
    plt.scatter(sizes, prices, c=range(len(sizes)), cmap='viridis', marker='o')
    plt.xticks(rotation=45)
    plt.title(f'Dispersión de precios de {product_name}')
    plt.xlabel('Tamaño/Presentación')
    plt.ylabel('Precio')
    plt.tight_layout()
    plt.savefig(f'{product_name}_scatter.png')
    plt.show()

    # Crear un póster para cada producto
    poster = Poster()
    poster.add_image(f'{product_name}_boxplot.png', 'Gráfica de caja')
    poster.add_image(f'{product_name}_scatter.png', 'Gráfica de dispersión')
    poster.create(f'{product_name}_result_poster.png', f'Resultados para {product_name}')
