def decidir_compra(estado):
    oro = estado["oro"]
    tienda = estado["tienda"]
    decisiones = []

    for heroe in tienda:
        if oro >= 2:
            decisiones.append(f"Comprar {heroe}")
            oro -= 2  # cada héroe cuesta 2 de oro en este ejemplo

    return decisiones