
from drivers.mercado_libre import ml_driver
from main import BestItem


def main():
    info_total = dict()
    ml_driver(('television', ['soporte'],
                                    [('32 pulgadas', '32'),
                                    ('55 pulgadas', '55'),
                                    ('65 pulgadas', '65'),
                                    ('75 pulgadas', '75'),
                                    ]), BestItem('television', info_total))
    print(info_total)


if __name__ == '__main__':
    main()
