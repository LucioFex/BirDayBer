import sys


def calculate_percentage(screen_width, screen_height, measures):
    """
    Caculation of a simple rule of three to get a percentage for the imgs:
        Example: 'python index.py 1600 900 12x59'
    """
    SIZES = (screen_width, screen_height)
    measures = measures.split('x')

    for index in range(2):
        measures[index] = int(measures[index]) / int(SIZES[index])

    return f"Width = {round(measures[0], 3)}, Height = {round(measures[1], 3)}"


print(calculate_percentage(sys.argv[1], sys.argv[2], sys.argv[3]))
