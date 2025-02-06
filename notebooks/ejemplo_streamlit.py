import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Mi primera aplicación con Streamlit 🚀")

# Agregar un texto
st.write("¡Bienvenido a tu primera aplicación interactiva en Python!")

# Entrada de texto para el usuario
nombre = st.text_input("¿Cómo te llamas?")

# Botón para saludar
if st.button("Saludar"):
    st.write(f"Hola, {nombre}! 🎉 Bienvenido a Streamlit.")

# Agregar un gráfico simple

# Crear datos aleatorios
datos = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

# Mostrar tabla con datos
st.write("📊 Aquí tienes algunos datos aleatorios:")
st.dataframe(datos)

# Mostrar gráfico
st.write("📈 Gráfico de los datos:")
fig, ax = plt.subplots()
ax.plot(datos)
st.pyplot(fig)
