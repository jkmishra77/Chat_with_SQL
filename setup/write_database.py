import sqlite3
import os

def create_database_with_sample_data():
    """Create database and insert sample student data with confirmation"""
    
    db_path = "student.db"
    
    # Check if database already exists
    if os.path.exists(db_path):
        print("⚠️  Database 'student.db' already exists!")
        response = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if response != 'y':
            print("❌ Operation cancelled.")
            return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS STUDENT(
                NAME VARCHAR(25),
                CLASS VARCHAR(25),
                SECTION VARCHAR(25),
                MARKS INTEGER
            )
        ''')
        print("✅ STUDENT table created")
        
        # Clear existing data if any
        cursor.execute("DELETE FROM STUDENT")
        print("✅ Cleared existing data (if any)")
        
        # Insert sample data
        sample_data = [
            ('Alice', 'Data Science', 'A', 92),
            ('Bob', 'Data Science', 'B', 88),
            ('Charlie', 'AI', 'A', 95),
            ('David', 'AI', 'B', 78),
            ('Eva', 'DEVOPS', 'A', 85),
            ('Frank', 'DEVOPS', 'B', 74),
            ('Grace', 'Web Development', 'A', 90),
            ('Hank', 'Web Development', 'B', 81),
            ('Ivy', 'Cybersecurity', 'A', 89),
            ('Jack', 'Cybersecurity', 'B', 76)
        ]
        
        cursor.executemany('INSERT INTO STUDENT VALUES(?,?,?,?)', sample_data)
        conn.commit()
        
        # Verify data insertion
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ {count} sample records inserted successfully!")
        print("📊 Database 'student.db' is ready to use!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def show_sample_data():
    """Display sample data from database"""
    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT")
        rows = cursor.fetchall()
        conn.close()
        
        print("\n📋 Sample Data in STUDENT table:")
        print("-" * 50)
        for row in rows:
            print(f"Name: {row[0]:<10} | Class: {row[1]:<15} | Section: {row[2]:<3} | Marks: {row[3]}")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error reading data: {e}")

if __name__ == "__main__":
    print("🚀 Student Database Setup")
    print("=" * 50)
    
    if create_database_with_sample_data():
        # Ask if user wants to see the data
        response = input("\nDo you want to view the sample data? (y/n): ").lower().strip()
        if response == 'y':
            show_sample_data()
    
    print("\n🎉 Setup completed!")