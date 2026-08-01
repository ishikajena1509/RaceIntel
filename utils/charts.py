import plotly.graph_objects as go
def position_change_chart(results):
    results = results.sort_values("Position")
    fig = go.Figure()
    for _, row in results.iterrows():

        driver = row["Abbreviation"]

        start = int(row["GridPosition"])
        finish = int(row["Position"])

        change = start - finish

        if change > 0:
            color = "#00D26A"      # Green
        elif change < 0:
            color = "#FF4D4D"      # Red
        else:
            color = "#BDBDBD"      # Grey

        fig.add_trace(

            go.Scatter(

                x=[start, finish],
                y=[driver, driver],

                mode="lines+markers",

                line=dict(
                    color=color,
                    width=6,
                ),

                marker=dict(
                    size=11,
                    color=color,
                ),

                hovertemplate=
                f"<b>{row['FullName']}</b><br><br>"
                f"Grid Position : P{start}<br>"
                f"Finish Position : P{finish}<br>"
                f"Position Change : {change:+d}"
                "<extra></extra>",

                showlegend=False

            )
        )

    fig.update_layout(

        title=dict(
            text="📈 Position Gain / Loss",
            x=0,
            font=dict(size=24)
        ),

        template="plotly_dark",

        height=720,

        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",

        xaxis=dict(
            title="Race Position",
            autorange="reversed",
            dtick=1,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            tickfont=dict(size=13),
            title_font=dict(size=15)
        ),

        yaxis=dict(
            title="Drivers",
            tickfont=dict(size=13),
            categoryorder="array",
            categoryarray=results["Abbreviation"]
        ),

        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),

        hoverlabel=dict(
            bgcolor="#20242D",
            font_size=14
        )

    )

    return fig