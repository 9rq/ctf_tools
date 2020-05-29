def pack1(n, endianness = 'little'):
    '''
    return 8 bit
    '''
    return n.to_bytes(1,endianness)

def pack2(n, endianness = 'little'):
    '''
    return 16 bit
    '''
    return n.to_bytes(2,endianness)

def pack4(n, endianness = 'little'):
    '''
    return 32 bit
    '''
    return n.to_bytes(4,endianness)

def pack8(n, endianness = 'little'):
    '''
    return 64 bit
    '''
    return n.to_bytes(8,endianness)

def pack(n, endianness = 'little'):
    return pack4(n, endianness)
