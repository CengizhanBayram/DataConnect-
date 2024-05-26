from flask import Flask, render_template, request, redirect, url_for
from DataConnect import DataConnect

app = Flask(__name__)
data_connect = DataConnect("x4sqlite1.db")

@app.route('/')
def index():
    tables = data_connect.get_all_tables()
    return render_template('index.html', tables=tables)

@app.route('/select_table', methods=['POST'])
def select_table():
    table_name = request.form['table_name']
    message = data_connect.select_table(table_name)
    return redirect(url_for('table_operations'))

@app.route('/table_operations')
def table_operations():
    table_contents = data_connect.show_selected_table()
    return render_template('table_operations.html', table_contents=table_contents)

@app.route('/create_table', methods=['POST'])
def create_table():
    table_name = request.form['table_name']
    columns = request.form['columns']

    if not table_name or not columns:
        return "Table name and columns are required"

    columns_dict = {col.split()[0]: col.split()[1] for col in columns.split(', ')}
    message = data_connect.create_table(table_name, **columns_dict)
    return message

@app.route('/add_data', methods=['POST'])
def add_data():
    field_values = {}
    for key in request.form:
        field_values[key] = request.form[key]
    message = data_connect.add_data(**field_values)
    return message

@app.route('/update_data', methods=['POST'])
def update_data():
    id = request.form['id']
    field_values = {}
    for key in request.form:
        if key != 'id':
            field_values[key] = request.form[key]
    message = data_connect.update_data(id, **field_values)
    return message

@app.route('/delete_data/<int:id>')
def delete_data(id):
    message = data_connect.delete_data(id)
    return message

@app.route('/delete_table', methods=['POST'])
def delete_table():
    table_name = request.form['table_name']
    message = data_connect.delete_table(table_name)
    return message

if __name__ == '__main__':
    app.run(debug=True)