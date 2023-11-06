from posterygrafica import create_poster

if __name__ == '__main__':
    example_dict = {
        'television 32 pulgadas': {'name': 'SANSUI 32" HD TV SMX32T1H 2023 (32" Basic)', 'price': '$2,149.00',
                                   'image': 'https://m.media-amazon.com/images/I/71+TiKe7cHL._AC_UL320_.jpg',
                                   'store': 'amazon'},
        'television 55 pulgadas': {
            'name': 'Sony Pantalla 55 Pulgadas KD-55X77L: BRAVIA LED 4K UHD Smart Google TV - Modelo 2023',
            'price': '$10,713.00', 'image': 'https://m.media-amazon.com/images/I/6142QNI9HBL._AC_UL320_.jpg',
            'store': 'amazon'},
        'television 65 pulgadas': {'name': 'Hisense Televisión 65" 4K Ultra HD Panel Full Array', 'price': '$10,119.00',
                                   'image': 'https://m.media-amazon.com/images/I/71Lm17sZaDL._AC_UL320_.jpg',
                                   'store': 'amazon'},
        'television 75 pulgadas': {'name': 'TCL Smart TV Pantalla 55" 55Q750G Google TV QLED Compatible con Alexa',
                                   'price': '$10,999.00',
                                   'image': 'https://m.media-amazon.com/images/I/61ztvJYfgBL._AC_UL320_.jpg',
                                   'store': 'amazon'}}

    background_image_path = "fondo.png"  # Ruta de tu imagen de fondo

    create_poster(example_dict, 'television', background_image_path)
