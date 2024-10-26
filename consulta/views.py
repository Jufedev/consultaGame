from django.shortcuts import redirect, render
from obtencion_data.user import cpu, disk, gpu, ram
from obtencion_data.game import req_game
from obtencion_data import database
from .forms import SearchGame

requirements = []


def comparar_espacio_libre(espacio_libre, valor_comparacion):
    res = {}
    valor_comparacion_num = float(valor_comparacion.split()[0])
    for key, value in espacio_libre.items():
        espacio_libre = value["Libre"]
        espacio_libre_num = float(espacio_libre.split()[0])
        if espacio_libre_num > valor_comparacion_num:
            res[key] = True
        else:
            res[key] = False

    return res


def search(request):
    if request.method == "GET":
        return render(request, "index.html", {
            "form": SearchGame()
        })
    else:
        if request.POST["name"] != "":
            print("ACTIVAR NOMBRE")
            name_spaces = request.POST["name"]
            name = name_spaces.replace(" ", "+")
            url_game_name = f'https://store.steampowered.com/search/?term={name}'
            requirements.append(req_game.get_requirements_name(url_game_name))
            return redirect("game/")
        elif request.POST["url"] != "":
            print("ACTIVAR URL")
            url_game = request.POST["url"]
            requirements.append(req_game.get_requirements_url(url_game))
            return redirect("game/")
        else:
            print("ACTIVAR NADA")
            return render(request, "index.html", {
                "form": SearchGame(),
                "errorinfo": "Debes proporcionar información del nombre o url!"
            })


def game(request):
    if request.method == "GET":
        print(requirements)
        if len(requirements) == 0:
            return render(request, "error.html")
        data_game = req_game.obtain_data(requirements[-1])
        data_cpu = cpu.get_cpu()
        response_aux = database.get_data_game(data_game)
        if len(response_aux) >= 1:
            response = database.get_data_game(data_game)[0]
        else:
            response = database.get_data_game(data_game)
        if len(response) == 0:
            response = dict(response)
            response["frec"] = 3.0
            response["cores"] = 2

        if "error" in data_game:
            return render(request, "error.html")

        all_data = {
            "user_procesador": data_cpu["Nombre"],
            "user_cores": data_cpu["Cores"],
            "user_frec": data_cpu["Frec"],
            "user_ram": ram.get_ram()[next(iter(ram.get_ram()))],
            "user_disco": disk.get_disk(),
            "user_grafica": list(gpu.get_gpu().keys())[0],
            "game_procesador": data_game["Processor"],
            "game_ram": data_game["Memory"],
            "game_disco": data_game["Storage"],
            "game_grafica": data_game["Graphics"],
            "game_nombre": requirements[-1]["title"],
            "game_url": requirements[-1]["url"],
            "game_img": requirements[-1]["image"]
        }
        user_data = {
            "procesador": all_data["user_procesador"],
            "ram": all_data["user_ram"],
            "disco": all_data["user_disco"],
            "grafica": all_data["user_grafica"]
        }
        game_data = {
            "procesador": all_data["game_procesador"],
            "ram": all_data["game_ram"],
            "disco": all_data["game_disco"],
            "grafica": all_data["game_grafica"],
            "nombre": all_data["game_nombre"],
            "url": all_data["game_url"],
            "img": all_data["game_img"]
        }
        cumple_data = {
            "procesador": True if response["frec"] <= all_data["user_frec"] and response["cores"] <= all_data["user_cores"] else False,
            "ram": True if float(all_data["user_ram"][:-3]) >= float(all_data["game_ram"][:-3]) else False,
            "disco": comparar_espacio_libre(all_data["user_disco"], all_data["game_disco"]),
            "grafica": "Falta de información en el procesador, por favor comprobar compatibilidad"
        }

        return render(request, "game.html", {
            "user": user_data,
            "game": game_data,
            "cumple": cumple_data
        })
