from bs4 import BeautifulSoup
import requests
from obtencion_data.user import cpu


def fetch_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_game_requirements(soup, url):
    requirements_section = soup.find('div', class_='sysreq_contents')

    if requirements_section:
        first_game_section_title = soup.find('div', id='appHubAppName').string
        first_game_section_img = soup.find(
            'img', class_='game_header_image_full').get('src')

        try:
            requirements_section_minimum = requirements_section.find(
                'div', attrs={'data-os': 'win'})
            minimum_requirements = requirements_section_minimum.find(
                'div', class_='game_area_sys_req_leftCol')
        except:
            minimum_requirements = None

        return {
            'title': first_game_section_title,
            'url': url,
            'image': first_game_section_img,
            'Minimum Requirements': minimum_requirements
        }
    else:
        return None


def get_requirements_name(game_url):
    soup = fetch_soup(game_url)
    search_section = soup.find('div', id='search_resultsRows')

    if search_section:
        first_game_section_url = search_section.find('a').get('href')
        soup2 = fetch_soup(first_game_section_url)
        return get_game_requirements(soup2, first_game_section_url)
    else:
        return None


def get_requirements_url(game_url):
    try:
        soup = fetch_soup(game_url)
    except:
        return None
    return get_game_requirements(soup, game_url)


def get_processor_name(split_list_processor):

    try:
        intel_index = split_list_processor.index('Intel')
        intel_name = f"{split_list_processor[intel_index]} {split_list_processor[intel_index + 1]}"
    except ValueError:
        try:
            intel_index = split_list_processor.index('Core')
            intel_name = f"{split_list_processor[intel_index]} {split_list_processor[intel_index + 1]}"
        except:
            amd_name = None
    try:
        amd_index = split_list_processor.index('AMD')
        amd_name = f"{split_list_processor[amd_index]} {split_list_processor[amd_index + 1]}™ {split_list_processor[amd_index + 2]} {split_list_processor[amd_index + 3]}"
    except ValueError:
        amd_name = None

    return [intel_name, amd_name]


def obtain_data(requirements):
    data = {}
    if requirements:
        text_data = []

        for key, value in requirements.items():
            if key == "Minimum Requirements":
                for txt in value.stripped_strings:
                    text_data.append(txt)

        for index, text in enumerate(text_data):
            if text == "Processor:":
                aux = text_data[index+1].split(" ")
                if cpu.get_cpu()["Prefijo"].lower() == "amd":
                    data["Processor"] = get_processor_name(aux)[1]
                else:
                    data["Processor"] = get_processor_name(aux)[0]

            if text == "Memory:" or text == "Storage:":
                list_aux = text_data[index+1].split(" ")
                data[text_data[index][:-1]] = " ".join(list_aux[0:2])

            if text == "Graphics:":
                data[text_data[index][:-1]] = text_data[index+1]
    else:
        data["error"] = 'No se pudieron encontrar los requisitos del juego.'

    return data
