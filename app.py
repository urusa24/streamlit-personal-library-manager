import streamlit as st
import json

# Load and Save Library Data
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Streamlit App
st.title("Personal Library Manager")
menu = st.sidebar.radio("Select an option", ["View Library", "Add Book", "Remove Book", "Search Books", "Save & Exit"])

# View Library
if menu == "View Library":
    st.sidebar.title("Your Library")
    
    if library:
        st.table(library)
    else:
        st.write("Your library is empty. Add some books!")

# Add Book
elif menu == "Add Book":
    st.sidebar.title("Add a new book")
    name = st.text_input("Book Name")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=2022, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")
    rating = st.slider("Rating", min_value=0, max_value=5, step=1)

    if st.button("Add Book"):
        if name:
            library.append({
                "name": name,
                "author": author,
                "year": year,
                "genre": genre,
                "read_status": read_status,
                "rating": rating
            })
            save_library()
            st.success("Book added successfully!")
            st.rerun()
        else:
            st.error("Book Name cannot be empty!")

# Remove Book
elif menu == "Remove Book":
    st.subheader("Remove a book")

    book_names = [book.get("name", "") for book in library]

    if book_names:
        selected_book = st.selectbox("Select a book to remove", book_names)

        if st.button("Remove Book"):
            library = [book for book in library if book.get("name", "") != selected_book]
            save_library()
            st.success(f"Book '{selected_book}' removed successfully!")
            st.rerun()
    else:
        st.warning("No books in your library yet! Add some books first.")

# Search Books
elif menu == "Search Books":
    st.sidebar.title("Search for a book")
    search_term = st.text_input("Enter a book name, author, or genre")

    if st.button("Search"):
        results = [book for book in library if
                   search_term.lower() in book.get("name", "").lower() or
                   search_term.lower() in book.get("author", "").lower() or
                   search_term.lower() in book.get("genre", "").lower()]
        if results:
            st.table(results)
        else:
            st.warning("No books found matching your search.")

# Save & Exit
elif menu == "Save & Exit":
    save_library()
    st.success("Library saved successfully!")
    st.stop()
