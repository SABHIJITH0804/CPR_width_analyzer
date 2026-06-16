import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="CPR Range Visualizer",
    layout="wide"
)

st.title("CPR Range Visualizer")

# ---------------------------
# INPUTS
# ---------------------------

left_col, right_col = st.columns([1, 2])

with left_col:

    st.subheader("Inputs")

    tc = st.number_input(
        "TC",
        value=0.00,
        format="%.2f"
    )

    pivot = st.number_input(
        "Pivot",
        value=0.00,
        format="%.2f"
    )

    bc = st.number_input(
        "BC",
        value=0.00,
        format="%.2f"
    )

    calculate = st.button("Calculate")


# ---------------------------
# CALCULATE
# ---------------------------

if calculate:

    if pivot == 0:
        st.error("Pivot cannot be zero")
        st.stop()

    cpr_percent = ((tc - bc) / pivot) * 100

    # Keep chart between 0 and 1
    plot_value = max(0, min(cpr_percent, 1))

    # Histogram from 0.50 to CPR value

    if plot_value >= 0.50:
        bottom = 0.50
        height = plot_value - 0.50
    else:
        bottom = plot_value
        height = 0.50 - plot_value

    fig = go.Figure()

    for i in range(10):
        fig.add_bar(
            x=[i],
            y=[height],
            base=bottom,
            showlegend=False
        )

    fig.update_layout(
        title="CPR Histogram",
        height=500,
        bargap=0.10,
        xaxis=dict(
            showticklabels=False,
            title=""
        ),
        yaxis=dict(
            range=[0, 1],
            tickvals=[0, 0.25, 0.50, 0.75, 1.00],
            ticktext=["0.00", "0.25", "0.50", "0.75", "1.00"]
        )
    )

    with right_col:

        st.subheader("Visualization")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("CPR Values")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("TC", f"{tc:.2f}")
            st.metric("Pivot", f"{pivot:.2f}")

        with c2:
            st.metric("BC", f"{bc:.2f}")
            st.metric("CPR %", f"{cpr_percent:.4f}")

        st.divider()

        # CPR Interpretation

        if cpr_percent < 0.25:

            st.warning("Narrow CPR")

            st.info(
                """
                Market conditions are consistent with the type of CPR
                that is often associated with trend day sessions.
                Traders typically monitor for sustained directional
                movement once price establishes itself around key levels.
                """
            )

        elif cpr_percent > 0.75:

            st.success("Wide CPR")

            st.info(
                """
                Market conditions are consistent with the type of CPR
                that is often associated with trading range or sideways day sessions.
                Two-sided movement and range-based behaviour are
                commonly observed in these conditions.
                """
            )

        else:

            st.info("Normal CPR")

            st.info(
                """
                CPR width is within a typical range. Market structure
                can evolve in either direction depending on opening
                context, participation and price action.
                """
            )