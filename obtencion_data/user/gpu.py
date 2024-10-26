import wmi
import pythoncom
from obtencion_data.user.bytes_converter import bytes_to_readable_gpu


def get_gpu():
    res = {}
    pythoncom.CoInitialize()
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        a_ram = - int(gpu.AdapterRAM)
        res[gpu.Caption] = {
            "VRAM": bytes_to_readable_gpu(a_ram)
        }
    pythoncom.CoUninitialize()
    return res
