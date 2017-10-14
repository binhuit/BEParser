def get_state(pending, features=list, score=float('-inf'), prev_action=None):
    return {
        'pending': pending,
        'features': features,
        'score': score,
        'prev_action': prev_action
    }
