def validate_price_filter(min_price, max_price):
    """Function that checks whether a valid price filtered has been applied on Pararius.com"""
    valid_prices = {200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200,
                    1300, 1400, 1500, 1750, 2000, 2250, 2500, 3000, 4000, 6000}
    
    # Check that both prices are in the list of valid options, if provided
    if min_price is not None and min_price not in valid_prices:
        raise ValueError(f"Invalid minimum price '{min_price}'. Allowed values are: {sorted(valid_prices)}")
    if max_price is not None and max_price not in valid_prices:
        raise ValueError(f"Invalid maximum price '{max_price}'. Allowed values are: {sorted(valid_prices)}")
    
    # Check that min_price is less than max_price
    if min_price is not None and max_price is not None and min_price >= max_price:
        raise ValueError("Minimum price should be less than maximum price.")

    return min_price, max_price
    