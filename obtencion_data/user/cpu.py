import psutil
import platform
import cpuinfo


def get_cpu():
    nom_core = platform.processor()
    num_core = psutil.cpu_count(logical=False)
    freq_core = int(psutil.cpu_freq().current) / 1000

    return {
        'Nombre': cpuinfo.get_cpu_info()['brand_raw'],
        "Prefijo": nom_core.split(" ")[0][:-2],
        'Cores': num_core,
        'Frec': freq_core,
    }
