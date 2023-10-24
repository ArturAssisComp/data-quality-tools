
def get_int_or_float(input:int|str):
    if isinstance(input, int):
        return input, True
    return float(input[:-1]), False


def parse_samples(sample_arg:str)->list[str | int]:
    if not sample_arg:
        return []
    result = []
    raw_numbers = sample_arg.split(',')
    if raw_numbers[-1] == '':
        raw_numbers.pop()
    for raw_num in raw_numbers:
        num = _parse_int(raw_num)
        if num and num > 0:
            result.append(num)
        elif is_percent(raw_num):
            result.append(raw_num.replace(' ', ''))
        else:
            raise ValueError
    return result

def _parse_int(input:str)->int|None:
    try:
        num = int(input)
        return num
    except:
        return None

def is_percent(input:str)->bool:
    ''' 
    Returns True if input is a str in the form `<number>%` in which 0 < <number> <= 100.
    And False otherwise.
    '''
    input = input.strip()
    if not input or input[-1] != '%':
        return False
    try:
        percent_number = float(input[:-1])
        if 0 < percent_number and percent_number <= 100:
            return True
        return False
    except:
        return False

