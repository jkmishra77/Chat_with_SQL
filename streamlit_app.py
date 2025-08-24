import streamlit as st
import sqlite3
from backend import process_question

# Streamlit UI
st.set_page_config(page_title="SQL CrewAI Assistant", layout="centered")
st.title("🧠 SQL CrewAI Assistant")

# Function to show all data
def show_all_data():
    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT")
        rows = cursor.fetchall()
        conn.close()
        
        # Display all data
        st.subheader("📊 All Students Data")
        for row in rows:
            st.write(f"**Name:** {row[0]}, **Class:** {row[1]}, **Section:** {row[2]}, **Marks:** {row[3]}")
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

# Show all data when app starts
if 'data_loaded' not in st.session_state:
    if show_all_data():
        st.session_state.data_loaded = True
    st.divider()

# Initialize session state for question
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

# Question input section
st.subheader("💬 Ask a Question")
question = st.text_input(
    "Enter your question about student data:", 
    placeholder="e.g., Show students with marks greater than 90...",
    key="question_input",
    value=st.session_state.current_question
)

# Example questions
st.write("**💡 Example Questions:**")
examples = [
    "Show all students in Data Science class",
    "Who has the highest marks?",
    "List students with marks greater than 90",
    "Count students in each class",
    "Show average marks by section"
]

cols = st.columns(2)
for i, example in enumerate(examples):
    with cols[i % 2]:
        if st.button(example, key=f"ex_{i}"):
            st.session_state.current_question = example
            st.rerun()

# Process question
if st.button("🚀 Generate & Execute SQL", type="primary") or question:
    if question:
        with st.spinner("🧠 Generating SQL query and executing..."):
            result = process_question(question)
        
        st.divider()
        st.subheader("🔍 Generated SQL:")
        st.code(result['sql_query'], language='sql')
        
        st.subheader("📊 Results:")
        if 'error' in result and result['error']:
            st.error(f"❌ {result['error']}")
        else:
            st.write(result['results'])
    else:
        st.warning("⚠️ Please enter a question first!")

# Refresh button to show all data again
st.divider()
if st.button("🔄 Refresh All Data"):
    show_all_data()
