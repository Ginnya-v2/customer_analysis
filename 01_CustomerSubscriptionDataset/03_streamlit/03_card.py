import streamlit as st
import matplotlib.pyplot as plt

# 汎用的なカード作成関数
def create_card(title, value, width=4, height=1, color='#0017C1'):
    fig = plt.figure(figsize=(width, height))
    fig.patch.set_facecolor(color)
    plt.axis('off')
    plt.text(0.5, 0.7, title, ha='center', fontsize=14, color='white')
    plt.text(0.5, 0.4, f"{value:,}", ha='center', fontsize=24, color='white')
    return fig


col_left, col_right = st.columns([1, 2])

with col_left:
    st.pyplot(create_card("A店舗", 12000, height=1.5))
    st.pyplot(create_card("B店舗", 11000, height=1.5))

with col_right:
    st.pyplot(create_card("売上推移", 99999, width=6, height=3))

