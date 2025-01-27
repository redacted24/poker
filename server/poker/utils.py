def get_unique_name(name, player_names):
    if name in player_names:
        original_name = name
        i = 1
        while name in player_names:
            name = f'{original_name} ({i})'
            i += 1

    return name
