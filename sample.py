# brain stomer
import streamlit as st
import os
# creating directories
SAVE_DIR = "notes"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_note(username, filename, content):
    with open(os.path.join(SAVE_DIR, f"{username}_{filename}.txt"), "w") as file:
        file.write(content)

def load_note(username, filename):
    with open(os.path.join(SAVE_DIR, f"{username}_{filename}.txt"), "r") as file:
        return file.read()

def get_user_files(username):
    return [f for f in os.listdir(SAVE_DIR) if f.startswith(f"{username}_")]

def main():
    if 'username' not in st.session_state:
        st.session_state.username = None

    if st.session_state.username is None:
        st.title("Brain Stromer")
        username = st.text_input("uername:")
        
        if st.button("Login"):
            if username:
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Username cannot be empty.")

    else:
        username = st.session_state.username
        st.sidebar.title(f"Welcome, {username}")
        
        if st.sidebar.button("Logout"):
            st.session_state.username = None
            st.experimental_rerun()

        operation = st.sidebar.selectbox("Select operation", ["New Note", "Edit Note"])

        if operation == "New Note":
            st.header("New Note")
            new_filename = st.text_input("Share your thought:")
            new_content = st.text_area("Brief down your thought:")

            if st.button("Save Note"):
                if new_filename and new_content:
                    save_note(username, new_filename, new_content)
                    st.success("Thought saved successfully!")
                else:
                    st.error("Filename and content cannot be empty.")

        elif operation == "Edit Note":
            st.header("Review Thought")
            user_files = get_user_files(username)
            if user_files:
                edit_filename = st.selectbox("Select a note to edit", user_files)
                if edit_filename:
                    edit_filename = edit_filename[len(username) + 1:-4] 
                    edit_content = load_note(username, edit_filename)
                    new_content = st.text_area("Edit Thought:", edit_content)

                    if st.button("Save Changes"):
                        save_note(username, edit_filename, new_content)
                        st.success("Thought updated successfully!")
            else:
                st.write("You have no saved notes.")

if __name__ == "__main__":
    main()
