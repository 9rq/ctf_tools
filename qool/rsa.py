from tqdm import tqdm


def ex_euclid(x, y):
    '''
    get d from e and phi
    '''
    c0, c1 = x, y
    a0, a1 = 1, 0
    b0, b1 = 0, 1

    while c1 != 0:
        m = c0 % c1
        q = c0 // c1

        c0, c1 = c1, m
        a0, a1 = a1, (a0 - q * a1)
        b0, b1 = b1, (b0 - q * b1)

    if a0 < 0:
        a0 += y
    return a0

def small_key_attack(n, till= 10**7):
    for i in tqdm(range(3,till,2)):
        if n % i == 0:
            return (i, n//i)
    else:
        print('small key attack failed')
        return None

def similar_key_attack(n,till = 10**7):
    m = int(n**0.5)
    m -= m%2+1

    for i in tqdm(range(m, m + till, 2)):
        if n % i == 0:
            return (i, n //i)
    else:
        print('similar key attack failed')
        return None

def int_to_str(pt):
    return bytes.fromhex(hex(pt)[2:]).decode('utf-8')


class RSA():
    '''
    RSA enc/dec solver
    '''
    def __init__(self, e , p=0, q=0, n=0, phi=0):

        if phi == 0:
            if p == n == 0 or q == n == 0:
                raise ValueError('No information for keys.')
            elif n == 0:
                n = p * q
                self.n = n
            elif p == q == 0:
                p, q = self.key_attack(n)
            elif p == 0:
                assert n%q ==0
                p = n // q
            elif q == 0:
                assert n%p == 0
                q = n // p

            assert phi == 0
            phi = (p - 1) * (q - 1)

        self.p = p
        self.q = q
        self.n = n
        self.e = e
        self.phi = phi

        d = ex_euclid(e, phi)
        assert d > 0
        self.d = d

    def key_attack(self, n):
        p = q = 0
        # check if p or q is small prime
        if p == q == 0:
            pq = small_key_attack(n)
            if pq is not None:
                p, q = pq

        # check if p or q is almost same value
        if p == q == 0:
            pq = similar_key_attack(n)
            if pq is not None:
                p, q = pq

        if p == q == 0:
            raise ValueError('Failed to specific keys')

        return p, q

    def enc(self, pt):
        ct = pow(pt, self.e, self.n)
        return ct

    def dec(self, ct):
        pt = pow(ct, self.d, self.n)
        assert self.enc(pt) == ct
        return pt

    def show(self):
        print('-'* 50)
        print('p={}'.format(self.p))
        print('q={}'.format(self.q))
        print('e={}'.format(self.e))
        print('d={}'.format(self.d))
        print('phi={}'.format(self.phi))
        print('-'* 50)


def main():
    p = 11616319110658188732363367285578075415582166350901955095819403328983515795673123283602587072841405166117210828382822280472716981376567192209223029993520687
    q = 9995623664398093950285806095825074830515486875873306891928893633322396259698043756295306959220611822631989759221775083696914195202522879012979025752766139
    n = p*q
    ct = 88516966939738101781614614217858346225269523737213529195370817409185227690925053773305931450341832298964405870356511204440566349620771126612146640623723791860220025737297100212744016843594624562613209552923301844687215754202211867608884775000642105079727858827824203562624203890981078763929147069944312378787
    e = 65537
    rsa = RSA(e, n=n,p=p)
    pt = rsa.dec(ct)
    print(pt)
    rsa.show()
    print(int_to_str(pt))


if __name__ == '__main__':
    main()
