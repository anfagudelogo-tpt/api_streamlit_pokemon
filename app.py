import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import re


def validate_pokemon_name(pokemon_name):
    return bool(re.match(r"^[a-zA-Z]+$", pokemon_name))


def get_pokemon_evolution(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Ups... parece que '{pokemon_name}' se ha escondido en la hierba alta. ¿Seguro que escribiste bien el nombre? 🧐"

    species_data = response.json()
    evolution_chain_url = species_data["evolution_chain"]["url"]

    response = requests.get(evolution_chain_url)
    if response.status_code != 200:
        return "Error al obtener la cadena de evolución."

    evolution_data = response.json()

    evolution_chain = []
    current_evolution = evolution_data["chain"]

    while current_evolution:
        species_name = current_evolution["species"]["name"]
        sprite_url = f"https://pokeapi.co/api/v2/pokemon/{species_name}/"
        sprite_response = requests.get(sprite_url)

        if sprite_response.status_code == 200:
            sprite_data = sprite_response.json()
            sprite = sprite_data["sprites"]["front_default"]
        else:
            sprite = None

        evolution_chain.append((species_name, sprite))

        if "evolves_to" in current_evolution and current_evolution["evolves_to"]:
            current_evolution = current_evolution["evolves_to"][0]
        else:
            break

    return evolution_chain


st.title("Evoluciones pokemón")

pokemon_name = st.text_input("Ingrese el nombre de un Pokémon:")

if pokemon_name:
    if not validate_pokemon_name(pokemon_name):
        st.error(
            "El nombre del Pokémon debe contener solo letras y no puede incluir caracteres especiales ni números."
        )
    else:
        evolutions = get_pokemon_evolution(pokemon_name)

        if isinstance(evolutions, str):
            st.error(evolutions)
        else:
            cols = st.columns(
                len(evolutions)
            )  # Crear columnas dinámicamente según el número de evoluciones
            for col, (name, img_url) in zip(cols, evolutions):
                with col:
                    st.subheader(name.capitalize())
                    if img_url:
                        response = requests.get(img_url)
                        img = Image.open(BytesIO(response.content))
                        img = img.resize(
                            (128, 128)
                        )  # Reducción de tamaño fija para mejor visualización
                        st.image(img, caption=name.capitalize())
