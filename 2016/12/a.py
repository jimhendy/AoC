from assembunny import Assembunny

def run(inputs):
    
    a = Assembunny(inputs)
    a()

    return a.registers['a']