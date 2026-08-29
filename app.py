import streamlit as st


st.set_page_config(
    page_title="Ana Fast-Lane",
    page_icon="🛡️",
    layout="centered",
)


def main():
    st.title("Ana Fast-Lane")
    st.subheader("From Report to Temporary Preservation")

    st.warning(
        "SIMULATED PROTOTYPE — This application uses synthetic data only "
        "and is not connected to Banco de México, SPEI, any bank, police, "
        "or any real recipient account."
    )

    st.markdown(
        """
        **Vacuum:** Restitution  
        **Lens:** Operator

        **Core question:**  
        How fast can a verified fraud report become operational action?
        """
    )

    st.divider()

    st.info(
        "Phase 1 project skeleton is active. "
        "Transaction reporting and preservation logic have not been implemented yet."
    )

    st.markdown("### Locked prototype boundaries")

    st.markdown(
        """
        This prototype will eventually evaluate whether one specific reported
        transaction can qualify for a temporary simulated preservation action.

        It will **not**:

        - freeze real funds;
        - freeze an entire account;
        - reimburse the reporting user;
        - determine recipient guilt;
        - prove a complete fraud case;
        - connect to real banking or SPEI systems;
        - store real personal or banking data;
        - allow AI to authorize a hold.
        """
    )

    st.divider()

    st.caption(
        "Synthetic prototype only · No persistent personal-data storage · "
        "No database · No authentication"
    )


if __name__ == "__main__":
    main()
