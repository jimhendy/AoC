from bits_message import BitsMessage


def run(inputs):

    bm = BitsMessage(hex_message=inputs)
    bm.extract_leading_packet()

    return bm.version_total
