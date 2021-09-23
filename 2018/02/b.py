import os


def run(inputs):

    ids = [list(i) for i in inputs.split(os.linesep)]

    for i, id_i in enumerate(ids):
        for id_j in ids[i:]:
            if not len(id_i) == len(id_j):
                continue

            n_diffs = 0
            failed = False
            diff_character_i = -1

            for char_i, id_i_char in enumerate(id_i):
                if id_i_char != id_j[char_i]:
                    diff_character_i = char_i
                    n_diffs += 1
                    if n_diffs > 1:
                        failed = True
                        break
            if failed:
                continue
            if n_diffs != 1:
                continue
            return "".join(id_i[:diff_character_i] + id_i[diff_character_i + 1 :])
