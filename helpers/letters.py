def update_freq(letters_dict, item):
    for key in list(item):
        if key in letters_dict:
            letters_dict[key] = letters_dict[key] + 1
        else:
            letters_dict[key] = 1
            
def get_letters_stats(strings):
    letters_freq = dict()
    for item in strings:
        update_freq(letters_freq, item)
    return letters_freq
