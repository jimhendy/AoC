import common


def run(inputs, aim=19690720):

    in_copy = common.in_to_array(inputs)

    done = False

    for noun in range(99):
        for verb in range(99):
            trial = in_copy.copy()
            trial[1] = noun
            trial[2] = verb
            output = common.intcode(trial)
            if output[0] == aim:
                print(f"Found working combination: Noue: {noun}, Verb: {verb}")
                return noun * 100 + verb

    raise Exception("Failure to find working combination")
