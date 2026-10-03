def process(frame):
    '''Get the average color from the edges of the screen.'''

    height, width = frame.shape[:2]

    edge_height = int(height * 0.10)
    edge_width = int(width * 0.10)

    top = frame[:edge_height, :]
    bottom = frame[height - edge_height:, :]
    left = frame[edge_height:height - edge_height, :edge_width]
    right = frame[edge_height:height - edge_height, width - edge_width:]

    top_color = top.mean(axis=(0, 1))
    bottom_color = bottom.mean(axis=(0, 1))
    left_color = left.mean(axis=(0, 1))
    right_color = right.mean(axis=(0, 1))

    average_color = (
        top_color +
        bottom_color +
        left_color +
        right_color
    ) / 4

    return average_color.astype(int)