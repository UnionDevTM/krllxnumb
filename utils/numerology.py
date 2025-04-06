def calculate_digital_root(user_id: int) -> int:
    """Вычисляет цифровой корень ID"""
    num = user_id
    while num >= 10:
        num = sum(int(digit) for digit in str(num))
    return num