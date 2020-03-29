import os
import re
from abc import ABC
from collections import defaultdict

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChipReceiver(ABC):
    def __init__(self):
        self.chips = []

    def get(self, chip_value):
        self.chips.append(chip_value)
        self.give_if_possible()

    def give_if_possible(self):
        pass


class Bot(ChipReceiver):
    def __init__(self):
        super().__init__()
        self.give_to_high = None
        self.give_to_low = None
        self.chips_compared = []

    def set_give_instruction(self, low_high, to):
        setattr(self, f'give_to_{low_high}', to)
        self.give_if_possible()
        
    def give_if_possible(self):
        if not len(self.chips) == 2:
            return
        if self.give_to_high is None or self.give_to_low is None:
            return
        chips = sorted(self.chips)
        logger.info(f'Giving value {chips[0]} to {self.give_to_low.__class__}')
        logger.info(f'Giving value {chips[1]} to {self.give_to_high.__class__}')
        self.chips_compared.append((chips[0],chips[1])) 
        self.give_to_low.get(chips[0])
        self.give_to_high.get(chips[1])
        self.chips = []
        self.give_to_low = None
        self.give_to_high = None


class Output(ChipReceiver):
    pass


BOTS = defaultdict(Bot)
OUTPUTS = defaultdict(Output)


def give(from_bot, low_high, dest_bot_output, dest_id):
    logger.info(f'Bot {from_bot} giving {low_high} to {dest_bot_output} {dest_id}')
    if dest_bot_output == 'bot':
        dest_dict = BOTS
    else:
        dest_dict = OUTPUTS
    BOTS[from_bot].set_give_instruction( low_high, dest_dict[dest_id])


def get(bot_id, value):
    logger.info(f'Bot {bot_id} getting value {value}')
    BOTS[bot_id].get(value)


GIVE_REG = re.compile(
    '^bot (\d+) gives (low|high) to (bot|output) (\d+) and (low|high) to (bot|output) (\d+)$')
GET_REG = re.compile('^value (\d+) goes to bot (\d+)$')


def run(inputs):

    values = defaultdict(list)
    
    for ins in inputs.split(os.linesep):

        matches = GIVE_REG.findall(ins)

        if len(matches):
            assert len(matches) == 1
            matches = matches[0]
            from_bot = int(matches[0])
            give(from_bot, matches[1], matches[2], int(matches[3]))
            give(from_bot, matches[4], matches[5], int(matches[6]))

        else:
        
            matches = GET_REG.findall(ins)
            assert len(matches) == 1
            matches = matches[0]
            get(int(matches[1]), int(matches[0]))
            values[int(matches[1])].append(int(matches[0]))

    answer_bots = [ bot_id for (bot_id, bot) in BOTS.items() if (17,61) in bot.chips_compared ]
    assert len(answer_bots) == 1

    return answer_bots[0]
