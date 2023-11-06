from drivers.mercado_libre import ml_driver
from main import BestItem


def main():
    example_dict = {
        'television 32 pulgadas': {'name': 'Pantalla Aiwa 32 Pulgadas Smart TV HD Roku AW-32HM2PRC',
                                   'price': '$3,090.00',
                                   'image': 'https://chedrauimx.vtexassets.com/arquivos/ids/21286109-500-auto?v=638341531945800000&width=500&height=auto&aspect=true',
                                   'store': 'chedraui'},
        'television 55 pulgadas': {'name': 'Pantalla LG 55 Pulgadas Smart TV UHD 4K AI ThinQ 55UQ8000PSB',
                                   'price': '$11,195.00',
                                   'image': 'https://chedrauimx.vtexassets.com/arquivos/ids/21201548-500-auto?v=638340157294900000&width=500&height=auto&aspect=true',
                                   'store': 'chedraui'},
        'television 65 pulgadas': {'name': 'Pantalla Sansui 65 Pulgadas 4K Google TV SMX65VAUG',
                                   'price': '$11,995.00',
                                   'image': 'https://chedrauimx.vtexassets.com/arquivos/ids/20770744-500-auto?v=638334283224500000&width=500&height=auto&aspect=true',
                                   'store': 'chedraui'}
    }

    create_poster(example_dict, 'television')


if __name__ == '__main__':
    main()
