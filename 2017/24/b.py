import os

import a_star
from bridge import Bridge
from component import Component


def run(inputs):

    comps = [Component(i) for i in inputs.split(os.linesep)]
    status = a_star.augmented_a_star(
        initial_state=Bridge([], comps),
        return_status=True
    )

    return status['bridge_data'][
        max(status['bridge_data'].keys())
    ]