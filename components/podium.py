import streamlit as st


def podium_card(position, driver, team, color):

    st.markdown(
        f"""
<div style="
background:#181C24;
border-top:6px solid {color};
border-radius:18px;
padding:18px;
height:180px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
box-shadow:0px 6px 18px rgba(0,0,0,0.35);
">

<h1 style="margin:0;">
{position}
</h1>

<h3 style="margin-top:12px;color:white;">
{driver}
</h3>

<p style="color:#B5B5B5;font-size:16px;">
{team}
</p>

</div>
""",
        unsafe_allow_html=True,
    )