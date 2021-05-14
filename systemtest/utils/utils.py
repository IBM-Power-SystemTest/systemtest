def dict_counter(count_dict: dict, count_key: str) -> None:
    count_dict[count_key] = count_dict.get(count_key, 0) + 1
