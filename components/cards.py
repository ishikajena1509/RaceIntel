import streamlit as st


def metric_card(title, value, icon="📊", subtitle="", color="#E10600"):

    st.markdown(
        f"""
<div style="
background:#181C24;
border-left:5px solid {color};
border-radius:14px;
padding:18px;
height:125px;
box-shadow:0px 6px 16px rgba(0,0,0,0.35);
display:flex;
flex-direction:column;
justify-content:space-between;
">

<div style="
font-size:20px;
font-weight:600;
color:#B0B3B8;">
{icon} {title}
</div>

<div style="
font-size:24px;
font-weight:700;
color:white;
white-space:nowrap;
overflow:hidden;
text-overflow:ellipsis;">
{value}
</div>

<div style="
font-size:14px;
color:#9AA0A6;">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )