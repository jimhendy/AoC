from bits_message import BitsMessage


def run(inputs):

    bm = BitsMessage(hex_message=inputs)
    p = bm.extract_leading_packet()

    return p.value()
