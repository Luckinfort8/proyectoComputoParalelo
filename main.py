from multiprocessing import Process, Manager
import pickle
import subprocess 

from drivers.amazon import amazon_driver
from drivers.chedraui import chedraui_driver
from drivers.mercado_libre import ml_driver


class BestItem:
    def __init__(self, nombre, dict):
        self.nombre = nombre
        self.items = dict

    def add_item(self, total_info):
        for query, info in total_info.items():
            if query not in self.items:
                self.items[query] = info
            else:
                if self.items[query]['price'] > info['price']:
                    self.items[query] = info


def main():
    list_prodcuts = [
        ('television', ['soporte'],
         [('32 pulgadas', '32'),
          ('55 pulgadas', '55'),
          ('65 pulgadas', '65'),
          ('75 pulgadas', '75'),
          ]),
        ('laptop', ['mouse', 'audifonos'],
         [('lenovo', 'lenovo'),
          ('hp', 'hp'),
          ('dell', 'dell'),
          ('macbook', 'macbook'),
          ]),
        ('celular', ['cargador', 'audifonos'],
         [('samsung', 'samsung'),
          ('iphone', 'iphone'),
          ('motorola', 'motorola'),
          ('nokia', 'nokia'),
          ]),
        ('refrigerador', ['licuadora'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('samsung', 'samsung'),
          ('frigidaire', 'frigidaire'),
          ]),
        ('lavadora', ['secadora'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('daewoo', 'daewoo'),
          ('frigidaire', 'frigidaire'),
          ]),
        ('estufa', ['microondas'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('samsung', 'samsung'),
          ('frigidaire', 'frigidaire'),
          ]),
        ('aspiradora', ['escoba'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('daewoo', 'daewoo'),
          ('frigidaire', 'frigidaire'),
          ]),
        ('licuadora', ['cafetera'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('samsung', 'samsung'),
          ('frigidaire', 'frigidaire'),
          ]),
        ('cafetera', ['licuadora'],
         [('lg', 'lg'),
          ('mabe', 'mabe'),
          ('daewoo', 'daewoo'),
          ('frigidaire', 'frigidaire'),
          ]),
    ]

    drivers = [chedraui_driver, amazon_driver, ml_driver]
    processes = []

    with Manager() as manager:
        best_items = [BestItem(item[0], manager.dict()) for item in list_prodcuts]
        for item, best_item in zip(list_prodcuts, best_items):
            for driver in drivers:
                p = Process(target=driver, args=(item, best_item))
                processes.append(p)
                p.start()
        for p in processes:
            p.join()
        for best_item in best_items:
            print(best_item.nombre)
            print(best_item.items)

    # Guardar los diccionarios en archivos
    for best_item in best_items:
        product_name = best_item.nombre
        data_to_save = best_item.items
        with open(f'{product_name}_data.pkl', 'wb') as file:
            pickle.dump(data_to_save, file)

    # Después de guardar los diccionarios, ejecuta posterygrafica.py
    #subprocess.run(["python", "posterygrafica.py"])

if __name__ == '__main__':
    main()
