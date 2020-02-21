def password_is_valid(password, input_range):
    start, end = list(map(
        lambda x: int(x),
        input_range.split('-')
        ))

    if not len(str(password)) == 6:
        return False
        
    if any([min(start, password) != start, max(end, password) != end]):
        return False

    last_num = -1
    last_repeat_count = 1
    has_adjacent_repeat = False
    is_increasing = True
    for i, current in enumerate(str(password)):
        current = int(current)
        # print(i, last_num, current, last_repeat_count)
        if current == last_num:
            last_repeat_count += 1
            
            if last_repeat_count == 2 and i == len(str(password)) - 1:  # handle final digit
                has_adjacent_repeat = True
        else:
            # i != last_num and 
            if last_repeat_count == 2:
                has_adjacent_repeat = True
            last_repeat_count = 1

        if current < last_num:
            is_increasing = False
        last_num = current


    if not has_adjacent_repeat or not is_increasing:
        # print(has_adjacent_repeat, is_increasing)
        return False

    return True
    
def do():
    input = '109165-576723'
    current, end = list(map(
        lambda x: int(x),
        input.split('-')
        ))
        
    valid = []
    while current < end:
        if password_is_valid(current, input):
            valid.append(current)
        
        current += 1
        
    print(valid, len(valid))

do()

