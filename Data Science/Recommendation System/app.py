# Libraries
import streamlit as st
from domain.logic import inquilinos_compatibles
from assistants.attendants import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

def main():
    # Configure the page to use a wider layout
    st.set_page_config(layout="wide")
    resultado = None

    # Display an image at the top of the page
    st.image('Your Path/portada.png', use_column_width=True)
    st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

    # Configure the sidebar with input fields and a button
    with st.sidebar:
        st.header("¿Quién está viviendo ya en el piso?")  # "Who is already living in the apartment?"
        inquilino1 = st.text_input("Inquilino 1")
        inquilino2 = st.text_input("Inquilino 2")
        inquilino3 = st.text_input("Inquilino 3")
        num_compañeros = st.text_input("¿Cuántos nuevos compañeros quieres buscar?")  # "How many new roommates do you want to search for?"

        if st.button('BUSCAR NUEVOS COMPAÑEROS'):  # "SEARCH NEW ROOMMATES"
            try:
                topn = int(num_compañeros)  # Convert the number of roommates to an integer
            except ValueError:
                st.error("Por favor, ingresa un número válido para el número de compañeros.")  # "Please enter a valid number for the number of roommates."
                topn = None

            # Obtain the tenant IDs using the provided function
            id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)
            if id_inquilinos and topn is not None:
                # Call the function to get compatible roommates
                resultado = inquilinos_compatibles(id_inquilinos, topn)

    # Display errors if there are any
    if isinstance(resultado, str):
        st.error(resultado)
    elif resultado is not None:
        # Create two columns for the output
        cols = st.columns((1, 2))

        # In the first column, display the compatibility graph
        with cols[0]:
            st.write("Nivel de compatibilidad de cada nuevo compañero:")  # "Compatibility level of each new roommate:"
            fig_grafico = generar_grafico_compatibilidad(resultado[1])
            st.pyplot(fig_grafico)

        # In the second column, display the comparison table
        with cols[1]:
            st.write("Comparativa entre compañeros:")  # "Comparison between roommates:"
            fig_tabla = generar_tabla_compatibilidad(resultado)
            st.plotly_chart(fig_tabla, use_container_width=True)

if __name__ == "__main__":
    main()