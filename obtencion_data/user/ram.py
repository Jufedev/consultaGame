import psutil
from obtencion_data.user.bytes_converter import bytes_to_readable


def get_ram():
    return {
        "Total": bytes_to_readable(psutil.virtual_memory().total)
    }
