def get_status_string(status_code: int):
    start_digit: str = str(status_code)[0]
    status_string_dict = {
        "1": "info",
        "2": "success",
        "3": "redirect",
        "4": "client_error",
        "5": "server_error",
    }
    try:
        return status_string_dict[start_digit]
    except:
        return "unknown_error"
