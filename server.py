from flask import Flask, request, jsonify
app = Flask(__name__)

employees = []
deleted_employees = []

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
    return jsonify({"employeeId" : employee_id}), 201

# Get all Employee details
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return jsonify(employees), 200

# Get Employee details
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = employees[int(id) - 1]
    if (employee):
        return jsonify(employee), 200
    else:
        return jsonify({ "message" : "Employee with " + id + " was not found" }), 404

# Update Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = employees[int(id) - 1]
    if (employee):
        updated_employee = request.get_json()
        employee.update(updated_employee)
        employees[int(id) - 1] = employee
        return jsonify(employee), 201
    else:
        return jsonify({ "message" : "Employee with " + id + " was not found" }), 404   

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    return {}


if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')