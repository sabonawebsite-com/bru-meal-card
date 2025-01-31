from flask import Flask, render_template, request, jsonify  
import sqlite3  

app = Flask(__name__)  

# Database setup  
def init_db():  
    with sqlite3.connect('checkboxes2.db') as conn:  
        cursor = conn.cursor()  
        cursor.execute('''CREATE TABLE IF NOT EXISTS checkboxes (id INTEGER PRIMARY KEY, checked INTEGER)''')  
        conn.commit()  

@app.route('/')  
def index():  
    return render_template('index1.html')  

@app.route('/load_checkboxes', methods=['GET'])  
def load_checkboxes():  
    with sqlite3.connect('checkboxes2.db') as conn:  
        cursor = conn.cursor()  
        cursor.execute("SELECT checked FROM checkboxes ORDER BY id")  
        checkboxes = [row[0] for row in cursor.fetchall()]  
    return jsonify(checkboxes)  

@app.route('/save_checkboxes', methods=['POST'])  
def save_checkboxes():  
    data = request.json  
    with sqlite3.connect('checkboxes2.db') as conn:  
        cursor = conn.cursor()  
        cursor.execute("DELETE FROM checkboxes")  # Clear existing data  
        for index, checked in enumerate(data):  
            cursor.execute("INSERT INTO checkboxes (id, checked) VALUES (?, ?)", (index, checked))  
        conn.commit()  
    return jsonify({"message": "Checkbox states saved successfully."})  

if __name__ == '__main__':  
    init_db()  
    app.run(debug=True)