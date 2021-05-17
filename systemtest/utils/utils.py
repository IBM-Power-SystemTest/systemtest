def dict_counter(count_dict: dict, count_key: str) -> None:
    """
    A dictionary is passed to count the times a key is passed,
    create a count of that key, the count is inline over same dict

    Args:
        cout_dict:
            Dictionary to save keys with count
        count_key:
            Key to assign the count and count

    Returns:
        None but modify the dictionary
    """

    count_dict[count_key] = count_dict.get(count_key, 0) + 1
