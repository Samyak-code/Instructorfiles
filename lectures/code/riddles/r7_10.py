def floors(drops: int, balls: int) -> int:
    """
    Calculates the highest building we can evaluate with the given parameters.

    Args:
        drops: The number of trials we are allowed to perform>
        balls: The number of balls we have>

    Returns:
        The maximum number of between which we can distinguish.
    """
    if drops == 0 or balls == 0:
        return 0

    return floors(drops - 1, balls - 1) + floors(drops - 1, balls) + 1


for b in range(1, 6):
    for d in range(1, 9):
        print(floors(d, b))
    print("\n")
