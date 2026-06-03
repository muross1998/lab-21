import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="ЧПК Калькулятор", page_icon="🪵")

st.title("🪵 Калькулятор матеріалів для ЧПК")
st.write("Ця програма допомагає розрахувати витрати листового матеріалу (наприклад, фанери) та загальну вартість проєкту з візуалізацією залишків.")

st.sidebar.header("Параметри деталі")
part_width = st.sidebar.number_input("Ширина деталі (мм)", min_value=10, value=200)
part_length = st.sidebar.number_input("Довжина деталі (мм)", min_value=10, value=300)
quantity = st.sidebar.slider("Кількість деталей (шт)", min_value=1, max_value=100, value=10)

st.sidebar.header("Параметри матеріалу")
sheet_width = st.sidebar.number_input("Ширина листа (мм)", value=1525)
sheet_length = st.sidebar.number_input("Довжина листа (мм)", value=1525)
sheet_price = st.sidebar.number_input("Ціна за лист (грн)", min_value=100, value=850)
bit_diameter = st.sidebar.number_input("Діаметр фрези (мм)", value=3.2, step=0.1)

if st.button("Розрахувати витрати"):
  
    effective_width = part_width + bit_diameter
    effective_length = part_length + bit_diameter
   
    part_area_m2 = (effective_width * effective_length) / 1_000_000
    total_area_m2 = part_area_m2 * quantity
    sheet_area_m2 = (sheet_width * sheet_length) / 1_000_000
  
    sheets_needed = np.ceil(total_area_m2 / sheet_area_m2)
    total_cost = sheets_needed * sheet_price
    
    st.success("Розрахунок успішно завершено!")
    
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Загальна площа (м²)", f"{total_area_m2:.2f}")
    col2.metric("Потрібно листів", int(sheets_needed))
    col3.metric("Загальна вартість (грн)", f"{total_cost:.0f}")

  
    st.subheader("Співвідношення матеріалу: Корисна площа vs Залишки")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    used_area = total_area_m2
    wasted_area = (sheets_needed * sheet_area_m2) - used_area
    if wasted_area < 0: wasted_area = 0 
        
    categories = ['Корисна площа деталей', 'Залишки (відходи/обрізки)']
    ax.pie([used_area, wasted_area], labels=categories, autopct='%1.1f%%', 
           startangle=90, colors=['#4CAF50', '#FFC107'])
    ax.axis('equal') 
    

    st.pyplot(fig)
