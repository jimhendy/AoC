def run(inputs):

    n = inputs
    n_len = len(n)

    loc_a = 0
    loc_b = 1
    scores = '37'
    
    while n not in scores[-n_len-2:]:
        score_a = int(scores[loc_a])
        score_b = int(scores[loc_b])
        new_score = score_a + score_b
        scores += str(new_score)
        score_len = len(scores)
        loc_a = ( loc_a + score_a + 1 ) % score_len
        loc_b = ( loc_b + score_b + 1 ) % score_len  

    return scores.index(n)