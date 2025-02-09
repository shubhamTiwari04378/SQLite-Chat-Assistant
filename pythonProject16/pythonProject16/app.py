import sqlite3
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK tokenizer
nltk.download('punkt')


# Helper function to query the database
def query_database(query: str, params: tuple = ()):
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result


# NLP-based query processing using NLTK
def process_query(user_query: str):
    tokens = word_tokenize(user_query.lower())

    if "employees" in tokens and "in" in tokens:
        dept_index = tokens.index("in") + 1
        department = tokens[dept_index].capitalize()
        result = query_database("SELECT Name FROM Employees WHERE Department = ?", (department,))
        response = ", ".join([row[0] for row in result]) if result else "No employees found in that department."

    elif "manager" in tokens and "of" in tokens:
        dept_index = tokens.index("of") + 1
        department = tokens[dept_index].capitalize()
        result = query_database("SELECT Manager FROM Departments WHERE Name = ?", (department,))
        response = result[0][0] if result else "No manager found for that department."

    elif "hired" in tokens and "after" in tokens:
        date_index = tokens.index("after") + 1
        date = tokens[date_index]
        result = query_database("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        response = ", ".join([row[0] for row in result]) if result else "No employees hired after that date."

    elif "total" in tokens and "salary" in tokens and "for" in tokens:
        dept_index = tokens.index("for") + 1
        department = tokens[dept_index].capitalize()
        result = query_database("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
        response = f"Total salary expense: {result[0][0]:.2f}" if result and result[0][
            0] else "No data for that department."

    else:
        response = "I'm sorry, I couldn't understand your query. Please rephrase."

    return response


# Streamlit UI
st.title("NLP-Powered SQLite Chat Assistant")
st.write("Ask me queries about employees and departments!")

user_input = st.text_input("Enter your query:")
if st.button("Submit"):
    if user_input.strip():
        result = process_query(user_input)
        st.success(f"Response: {result}")
    else:
        st.warning("Please enter a valid query.")
