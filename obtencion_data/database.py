import os
from dotenv import load_dotenv
from supabase import create_client
from obtencion_data.user import cpu

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


def get_data_game(data_param):
    if "error" in data_param:
        return []
    product = data_param["Processor"] + "%"
    if cpu.get_cpu()["Prefijo"] == "AMD":
        response = supabase.table('amd').select(
            "*").ilike('name', product).order('cores').limit(1).execute()
        if len(response.data) == 0:
            product_aux = product[:-5] + "%"
            response = supabase.table('amd').select(
                "*").ilike('name', product_aux).order('cores').limit(1).execute()
    else:
        response = supabase.table('intel').select(
            "*").ilike('name', product).order('cores').limit(1).execute()
        if len(response.data) == 0:
            product_aux = product[:-5] + "%"
            response = supabase.table('intel').select(
                "*").ilike('name', product_aux).order('cores').limit(1).execute()
    return response.data
