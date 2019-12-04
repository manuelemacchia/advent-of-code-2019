from itertools import groupby

lower_bound = 130254
upper_bound = 678275
count = 0

for password in range(lower_bound, upper_bound+1):
    flags = {
        # True if at least one pair of adjacent digits is the same
        'adjacents': False,

        # True if the digits never decrease
        'increasing': True,

        # True if there is at least one group of more than two equal digits
        'matching_groups': False,
    }

    digit_prev = None
    for digit in map(int, str(password)):
        if digit_prev != None:
            if digit_prev > digit:
                flags['increasing'] = False
        
        digit_prev = digit

    groups = [''.join(g) for k, g in groupby(str(password))]

    group_prev = None
    for group in groups:
        if len(group) > 2:
            flags['matching_groups'] = True
        if len(group) == 2:
            flags['adjacents'] = True
        
        group_prev = group
        
    if (flags['adjacents'] == False or flags['increasing'] == False) or (flags['matching_groups'] == True and flags['adjacents'] == False):
        continue
    
    count += 1

print(f"Number of valid passwords: {count}")