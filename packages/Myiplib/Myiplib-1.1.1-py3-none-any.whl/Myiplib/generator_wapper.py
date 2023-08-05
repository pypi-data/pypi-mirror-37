def generator_warp(generator_to_warp, buffer_length):
    """
    Warp generator in a quere
    :rtype: generator
    """
    buffer = []

    while True:
        buffer = [next(generator_to_warp) for i in range(buffer_length)]
        yield buffer