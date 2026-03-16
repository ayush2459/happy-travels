def calculate_amount(
    start: str,
    destination: str,
    mode: str,
    option: str,
) -> int:
    distance = get_distance(start, destination)
    if distance == 0:
        return 0

    base = BASE_RATE.get(mode.lower())
    multiplier = CLASS_MULTIPLIER.get(option)

    if not base or not multiplier:
        return 0

    amount = distance * base * multiplier
    return int(amount)