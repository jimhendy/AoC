class State:

    def __init__(self):
        self.loc_a = 0
        self.loc_b = 1
        self.scores = [3, 7]

    def generate(self):
        score_a = self.scores[self.loc_a]
        score_b = self.scores[self.loc_b]
        new_score = score_a + score_b
        if new_score < 10:
            self.scores.append(new_score)
        else:
            [ self.scores.append(int(i)) for i in list(str(new_score)) ]  
        self.loc_a = ( self.loc_a + score_a + 1 ) % len(self.scores)  
        self.loc_b = ( self.loc_b + score_b + 1 ) % len(self.scores)  

    def __repr__(self):
        out = []
        for i,n in enumerate(self.scores):
            if i == self.loc_a:
                out.append(f'({n})')
            elif i == self.loc_b:
                out.append(f'[{n}]')
            else:
                out.append(str(n))
        return ' '.join(out)

def run(inputs):
    n = int(inputs)
    state = State()
    
    while len(state.scores) < (n+10):
        state.generate()
    

    return ''.join(map(str, state.scores[-10:]))