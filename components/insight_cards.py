import streamlit as st


def insight_card(title, value, subtitle="", color="#E10600", icon="📊"):

    st.markdown(
        f"""
<div style="
background:#181C24;
border-left:5px solid {color};
border-radius:14px;
padding:18px;
height:120px;
display:flex;
flex-direction:column;
justify-content:space-between;
box-shadow:0 6px 16px rgba(0,0,0,.35);
">

<div style="
font-size:17px;
font-weight:600;
color:#AEB6BF;
">
{icon} {title}
</div>

<div style="
font-size:24px;
font-weight:700;
color:white;
">
{value}
</div>

<div style="
font-size:14px;
color:#B5B5B5;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )