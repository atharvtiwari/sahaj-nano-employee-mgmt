from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_data_from_file(json_file : str):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def save_data_to_file(data, json_file : str):
    with open(json_file, 'w') as file:
        json.dump(data, file)

employees = load_data_from_file('employees.json')

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!', 200

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    employee = request.get_json()
    employee_id = str(len(employees) + 1)
    employee.update({"employeeId" : employee_id})
    employees.append(employee)
    save_data_to_file(employees, 'employees.json')
    return jsonify({"employeeId" : employee_id}), 201

# Get all Employee details
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return jsonify(employees), 200

# Get Employee details
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = next((item for item in employees if item["employeeId"] == id), None)
    if (employee):
        return jsonify(employee), 200
    else:
        return jsonify({ "message" : "Employee with " + id + " was not found" }), 404

# Update Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = next((item for item in employees if item["employeeId"] == id), None)
    if (employee):
        updated_employee = request.get_json()
        old_employee= employee
        employee.update(updated_employee)
        employees[employees.index(old_employee)] = employee
        save_data_to_file(employees, 'employees.json')
        return jsonify(employee), 201
    else:
        return jsonify({ "message" : "Employee with " + id + " was not found" }), 404   

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee =next((item for item in employees if item["employeeId"] == id), None)
    if (employee):
        employees.remove(employee)
        save_data_to_file(employees, 'employees.json')
        return jsonify(employee), 200
    else:
        return jsonify({ "message" : "Employee with " + id + " was not found" }), 404

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')