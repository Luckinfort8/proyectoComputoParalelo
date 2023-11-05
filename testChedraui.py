from drivers.chedraui import chedraui_driver
from drivers.walmart import walmart_driver


def main():

    info_total = walmart_driver(('television', ['soporte'],
                                    [('32 pulgadas', '32'),
                                    ('55 pulgadas', '55'),
                                    ('65 pulgadas', '65'),
                                    ('75 pulgadas', '75'),
                                    ]))
    for query, info in info_total:
        print(query)
        for item in info:
            print(item)


if __name__ == '__main__':
    main()
