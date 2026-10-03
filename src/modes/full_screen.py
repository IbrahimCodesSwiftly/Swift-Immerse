def process(frame):
    '''Get the average color of the whole frame.'''

    average_color = frame.mean(axis=(0, 1)).astype(int)

    return average_color