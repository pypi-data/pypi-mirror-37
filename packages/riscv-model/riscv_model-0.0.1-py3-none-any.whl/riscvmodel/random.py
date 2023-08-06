import random

from .variant import Variant, VariantRV32I
from .insn import Instruction

def random_instruction(variant: Variant, pool = None):
    if pool is None:
        pool = get_insns(Instruction)

    while True:
        c = random.choice(pool)
        i = c()
        i.randomize(variant)
        yield i

def random_asm(n, pool=None):
    v = VariantRV32I()
    for i in range(10):
        yield next(random_instruction(v, pool=pool))


