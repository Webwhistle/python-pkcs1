import math

import emsa_pss
import primitives

def sign(private_key, message,
        emsa_pss_encode=emsa_pss.encode):
    mod_bits = int(math.ceil(math.log(private_key.n, 2)))
    embits = mod_bits - 1
    em = emsa_pss_encode(message, embits)
    m = primitives.os2ip(em)
    s = private_key.rsasp1(m)
    return primitives.i2osp(s, private_key.k)

def verify(public_key, message, signature,
        emsa_pss_verify=emsa_pss.verify):
    mod_bits = int(math.ceil(math.log(public_key.n, 2)))
    s = primitives.os2ip(signature)
    m = public_key.rsavp1(s)
    embits = mod_bits - 1
    em_len = primitives.integer_ceil(embits, 8)
    em = primitives.i2osp(m, em_len)
    return emsa_pss_verify(message, em, embits)
