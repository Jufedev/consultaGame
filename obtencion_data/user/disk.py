import psutil
from obtencion_data.user.bytes_converter import bytes_to_readable


def get_disk():
    res = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        res[partition.device[0]] = {
            "Total": bytes_to_readable(partition_usage.total),
            "Libre": bytes_to_readable(partition_usage.free)
        }
    return res
