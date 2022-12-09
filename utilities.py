
def detect_repetition(l):
    val_to_check = l[-1]
    all_matches = [i for i in reversed(range(len(l))) if l[i] == val_to_check]
    try:
        return all_matches[0]-all_matches[1]
    except IndexError:
        return None