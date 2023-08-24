from flask import Flask, request, jsonify, json

app = Flask(__name__)
app.config['EMPLOYEES_JSON_FILE'] = '/home/employees.json'

def load_data_from_file():
    try:
        with open(app.config['EMPLOYEES_JSON_FILE'], 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data_to_file(data):
    with open(app.config['EMPLOYEES_JSON_FILE'], 'w') as file:
        json.dump(data, file)

employees = load_data_from_file()

# Greeting 
@app.route("/greeting", methods=['GET'])
def greeting():
    return 'Hello world!', 200

@app.route('/employee', methods=['POST'])
def create_employee():
    employee = request.get_json()
    employee_id = str(len(employees) + 1)
    employee.update({"employeeId" : employee_id})
    employees[employee_id] = employee
    save_data_to_file(employees)
    return jsonify({"employeeId" : employee_id}), 201

@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return jsonify(list(employees.values())), 200

@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = employees.get(id)
    if employee:
        return jsonify(employee), 200
    else:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404

@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = employees.get(id)
    if employee:
        updated_employee = request.get_json()
        employee.update(updated_employee)
        save_data_to_file(employees)
        return jsonify(employee), 201
    else:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404   

@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = employees.pop(id, None)
    if employee:
        save_data_to_file(employees)
        return jsonify(employee), 200
    else:
        return jsonify({ "message" : f"Employee with {id} was not found" }), 404

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')