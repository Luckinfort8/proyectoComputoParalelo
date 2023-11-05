from drivers.chedraui import chedraui_driver


def main():
    info_total = chedraui_driver(('television', ['soporte'],
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
