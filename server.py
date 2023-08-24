from flask import Flask, request, jsonify, json
import os

app = Flask(__name__)
app.config['EMPLOYEES_JSON_FILE'] = '/home/employees.json'

def load_data_from_file():
    try:
        with open(app.config['EMPLOYEES_JSON_FILE'], 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data_to_file(data):
    with open(app.config['EMPLOYEES_JSON_FILE'], 'w') as file:
        json.dump(data, file)

def create_to_file(data, id):
    with open(id, 'w') as file:
        json.dump(data, file)

def get_from_file(id):
    try:
        with open(id, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!', 200

@app.route('/employee', methods=['POST'])
def create_employee():
    employee = request.get_json()
    employees = load_data_from_file()
    employee_id = str(len(employees) + 1)
    result = {"employeeId" : employee_id}
    employee.update(result)
    create_to_file(employee, employee_id)
    employees.append(employee_id)
    save_data_to_file(employees)
    return jsonify(result), 201

@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    employees = load_data_from_file()
    return jsonify(employees), 200

@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = get_from_file(id)
    if employee == {}:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404
    else:
        return jsonify(employee), 200

@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = get_from_file(id)
    if employee == {}:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404
    else:
        updated_employee = request.get_json()
        employee.update(updated_employee)
        create_to_file(employee)
        return jsonify(employee), 201        

@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = get_from_file(id)
    if employee == {}:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404
    else:
        os.remove(id)
        employees = load_data_from_file()
        employee = employees.remove(id)
        save_data_to_file(employees)
        return jsonify(employee), 200

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')