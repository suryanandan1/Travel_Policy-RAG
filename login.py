import streamlit as st
from auth import create_user_table, signup, login


def login_page():

    create_user_table()

    st.title("Travel Policy Assistant")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Signup"]
    )

    # ---------------- SIGNUP ---------------- #

    if menu == "Signup":

        st.subheader("Create Account")

        emp_id = st.text_input("Employee ID")
        name = st.text_input("Name")

        password = st.text_input(
            "Password",
            type="password"
        )

        band = st.selectbox(
            "Band",
            [
                "9/10",
                "7/8",
                "5/6",
                "1/2/3/4"
            ]
        )

        if st.button("Signup"):

            success = signup(
                emp_id,
                name,
                password,
                band
            )

            if success:
                st.success("Account Created Successfully")
            else:
                st.error("Employee already exists")

    # ---------------- LOGIN ---------------- #

    if menu == "Login":

        st.subheader("Login")

        emp_id = st.text_input("Employee ID")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login(
                emp_id,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.user = {
                    "employee_id": user[1],
                    "name": user[2],
                    "band": user[4]
                }

                st.rerun()

            else:
                st.error("Invalid Credentials")