def competition(items, score_function):
    if len(items) == 0:
        raise Exception("Cannot have competition with no items")
    else:
        winner = items[0]
        winning_score = score_function(winner)
        for item in items[1:]:
            score = score_function(item)
            if score > winning_score:
                winner = item
                winning_score = score
        return winner

def multiwinner_competition(items, score_function, number_of_winners=1):
     copy = items.copy()
     copy.sort(key=score_function)
     return copy[:number_of_winners]
