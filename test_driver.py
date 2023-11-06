from drivers.amazon import amazon_driver
from posterygrafica import create_poster


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
    empty_dict = dict()
    test_data = ('television', ['soporte'],
         [('32 pulgadas', '32'),
          ('55 pulgadas', '55'),
          ('65 pulgadas', '65'),
          ('75 pulgadas', '75'),
          ])
    amazon_driver(test_data, BestItem('television', empty_dict))
    create_poster(empty_dict, 'television', 'fondo.png')


if __name__ == '__main__':
    main()

