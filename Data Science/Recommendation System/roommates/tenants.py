# Libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

def generar_grafico_compatibilidad(compatibilidad):
    # Convert compatibility percentages to a scale from 0 to 1
    compatibilidad = compatibilidad / 100
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Create a bar plot using seaborn
    sns.barplot(x=compatibilidad.index, y=compatibilidad.values, ax=ax, color='lightblue')
    
    # Remove the top, right, left spines, and bottom spine from the plot
    sns.despine(top=True, right=True, left=True, bottom=False)
    
    # Set the x and y axis labels
    ax.set_xlabel('Identificador de Inquilino', fontsize=10)
    ax.set_ylabel('Similitud (%)', fontsize=10)
    
    # Rotate x-axis labels for better readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    # Format y-axis labels to show percentages
    ax.set_yticklabels(['{:.1f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=8)
    
    # Annotate each bar with its height (percentage)
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5),
                    textcoords='offset points', fontsize=8)
    
    return fig

def generar_tabla_compatibilidad(resultado):
    # Reset index and rename the index column to 'ATRIBUTO'
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'ATRIBUTO'}, inplace=True)
    
    # Create a table using Plotly
    fig_table = go.Figure(data=[go.Table(
        columnwidth=[20] + [10] * (len(resultado_0_with_index.columns) - 1),
        header=dict(values=list(resultado_0_with_index.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                   fill_color='lavender', align='left'))
    ])
    
    # Update layout of the table
    fig_table.update_layout(width=700, height=320, margin=dict(l=0, r=0, t=0, b=0))
    
    return fig_table

def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn):
    id_inquilinos = []
    # Iterate over the tenant inputs
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        try:
            if inquilino:
                id_inquilinos.append(int(inquilino))
        except ValueError:
            # Display an error if the tenant identifier is not a valid number
            st.error(f"El identificador del inquilino '{inquilino}' no es un número válido.")
            id_inquilinos = []
            break
        
    return id_inquilinos