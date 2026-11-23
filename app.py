import streamlit as st
import pandas as pd
import os

ARCHIVO = "ventas.csv"
COLUMNAS = ["Producto", "Cantidad", "Precio", "Total"]


def cargar_datos():
    if os.path.exists(ARCHIVO):
        return pd.read_csv(ARCHIVO)
    return pd.DataFrame(columns=COLUMNAS)


def guardar_datos(df):
    df.to_csv(ARCHIVO, index=False)


st.title("Registro de Ventas del Día")

df = cargar_datos()

# ---------- CREAR ----------
st.header("1. Registrar una venta")
producto = st.text_input("Producto")
cantidad = st.number_input("Cantidad", min_value=1, step=1)
precio = st.number_input("Precio unitario", min_value=0.0, step=100.0)

if st.button("Guardar venta"):
    if producto.strip() == "":
        st.warning("Escribe el nombre del producto.")
    else:
        nueva = pd.DataFrame([{
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio": precio,
            "Total": cantidad * precio,
        }])
        df = pd.concat([df, nueva], ignore_index=True)
        guardar_datos(df)
        st.success("Venta guardada.")

# ---------- LEER ----------
st.header("2. Ventas del día")
if len(df) == 0:
    st.info("Todavía no hay ventas registradas.")
else:
    st.dataframe(df)
    st.metric("Total vendido en el día", f"${df['Total'].sum():,.0f}")

# ---------- ACTUALIZAR ----------
if len(df) > 0:
    st.header("3. Corregir una venta")
    fila = st.selectbox("Elige el número de la venta a corregir", df.index)
    nuevo_producto = st.text_input(
        "Producto", value=df.loc[fila, "Producto"], key=f"prod_{fila}"
    )
    nueva_cantidad = st.number_input(
        "Cantidad", min_value=1, step=1,
        value=int(df.loc[fila, "Cantidad"]), key=f"cant_{fila}"
    )
    nuevo_precio = st.number_input(
        "Precio unitario", min_value=0.0, step=100.0,
        value=float(df.loc[fila, "Precio"]), key=f"prec_{fila}"
    )

    if st.button("Actualizar venta"):
        df.loc[fila, "Producto"] = nuevo_producto
        df.loc[fila, "Cantidad"] = nueva_cantidad
        df.loc[fila, "Precio"] = nuevo_precio
        df.loc[fila, "Total"] = nueva_cantidad * nuevo_precio
        guardar_datos(df)
        st.rerun()

    # ---------- ELIMINAR ----------
    st.header("4. Eliminar una venta")
    fila_borrar = st.selectbox(
        "Elige el número de la venta a eliminar", df.index, key="borrar"
    )
    if st.button("Eliminar venta"):
        df = df.drop(fila_borrar).reset_index(drop=True)
        guardar_datos(df)
        st.rerun()