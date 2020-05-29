def pack2(n, endianness = 'little'):
    return n.to_bytes(2,endianness)

def pack4(n, endianness = 'little'):
    return n.to_bytes(4,endianness)

def pack(n, endianness = 'little'):
    return pack4(n, endianness)
