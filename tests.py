from drivers.chedraui import chedraui_driver
from drivers.amazon import amazon_driver
from drivers.soriana import soriana_driver


def main():
    info_total = dict()
    amazon_driver(('television', ['soporte'],
                                    [('32 pulgadas', '32'),
                                    ('55 pulgadas', '55'),
                                    ('65 pulgadas', '65'),
                                    ('75 pulgadas', '75'),
                                    ]), info_total)
    print(info_total)


if __name__ == '__main__':
    main()
