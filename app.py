import streamlit as st
import json
import pandas as pd

# Cargar datos de relations.json
with open('relations.json', 'r') as file:
    relations = json.load(file)

# Cargar datos de descriptions.json
with open('descriptions.json', 'r') as file:
    descriptions = json.load(file)

# Convertir descriptions a un diccionario para un acceso más fácil
descriptions_dict = {list(item.keys())[0]: list(item.values())[0] for item in descriptions}

# Obtener lista de criterios
criterios = []
for item in relations:
    for objetivo, data in item.items():
        criterios.extend(data['criterios'])

# Eliminar duplicados y ordenar criterios
criterios = sorted(set(criterios), key=lambda x: (int(x[2]), int(x[4:])))

# Interfaz de usuario
st.title("Selección de Criterios de Avaliación e Obxectivos Relacionados")

# Generar lista de criterios con descripciones
criterios_con_descripcion = [f"{criterio.upper()} - {descriptions_dict.get(criterio.upper(), 'DESCRICIÓN NON DISPOÑIBLE')}" for criterio in criterios]

# Selección de criterios de evaluación
selected_criterios = st.multiselect("Selecciona os criterios de avaliación da túa unidade", criterios_con_descripcion)

# Filtrar criterios seleccionados
selected_criterios_codes = [item.split(" - ")[0].lower() for item in selected_criterios]

# Relacionar criterios con descriptores y objetivos
criterios_dict = {}
objetivos_relacionados = set()
for item in relations:
    for objetivo, data in item.items():
        for criterio in data['criterios']:
            if criterio in selected_criterios_codes:
                criterios_dict.setdefault(criterio, {'descriptores': [], 'objetivos': []})
                criterios_dict[criterio]['descriptores'].extend(data['descriptores'])
                criterios_dict[criterio]['objetivos'].append(objetivo.upper())
                objetivos_relacionados.add(objetivo.upper())

# Presentar la estructura de datos en una tabla
if selected_criterios:
    st.write("### Estrutura de datos")
    data = []
    for criterio, info in criterios_dict.items():
        descriptores = ", ".join(set(info['descriptores'])).upper()
        descripcion = descriptions_dict.get(criterio.upper(), "DESCRICIÓN NON DISPOÑIBLE")
        data.append([criterio.upper(), descripcion, descriptores])

    df = pd.DataFrame(data, columns=["Criterio", "Descrición", "Descritores"])
    st.dataframe(df)

    # Imprimir objetivos relacionados
    st.write("### Obxectivos relacionados")
    st.write(", ".join(sorted(objetivos_relacionados)))