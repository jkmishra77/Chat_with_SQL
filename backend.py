import sqlite3
from llm.llm import setup_llm

def process_question(question):
    try:
        # Use direct LLM call
        llm = setup_llm()
        
        # Create prompt for SQL generation
        prompt = f"""Convert this English question to a SQLite SELECT query.
        Database: STUDENT with columns: NAME, CLASS, SECTION, MARKS.
        Return ONLY the SQL query without any explanations or formatting.
        
        Question: {question}"""
        
        # Get SQL query from LLM
        response = llm.invoke(prompt)
        sql_query = response.content.strip()
        
        # Clean up the SQL query
        if sql_query.startswith('```sql'):
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        
        # Execute the SQL query and get actual results
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names for better formatting
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        conn.close()
        
        # Format results - handle any type of query safely
        if not results:
            results_str = "No results found."
        else:
            formatted_results = []
            for row in results:
                try:
                    if column_names and len(row) == len(column_names):
                        # For queries with column names (aggregate functions)
                        row_str = " | ".join([f"{col}: {val}" for col, val in zip(column_names, row)])
                        formatted_results.append(row_str)
                    elif len(row) >= 4:
                        # For individual student records
                        formatted_results.append(f"Name: {row[0]}, Class: {row[1]}, Section: {row[2]}, Marks: {row[3]}")
                    else:
                        # Fallback for any other format
                        formatted_results.append(str(row))
                except IndexError:
                    # If row doesn't have enough elements, just convert to string
                    formatted_results.append(str(row))
            
            results_str = "\n".join(formatted_results)
        
        return {
            'question': question,
            'sql_query': sql_query,
            'results': results_str
        }
        
    except Exception as e:
        return {
            'question': question,
            'sql_query': 'SELECT * FROM STUDENT',
            'results': f'Error: {str(e)}'
        }
