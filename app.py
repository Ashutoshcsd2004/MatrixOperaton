from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def parse_matrix(data):
    """Convert a 2D list of strings to a NumPy array"""
    try:
        return np.array([[float(cell) for cell in row] for row in data])
    except:
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    matrix1 = parse_matrix(data.get("matrix1"))
    matrix2 = parse_matrix(data.get("matrix2")) if data.get("matrix2") else None
    operation = data.get("operation")
    
    if matrix1 is None or (data.get("matrix2") and matrix2 is None):
        return jsonify({"error": "Invalid matrix input."})
    
    try:
        if operation == "add":
            result = matrix1 + matrix2
        elif operation == "subtract":
            result = matrix1 - matrix2
        elif operation == "multiply":
            result = np.dot(matrix1, matrix2)
        elif operation == "transpose1":
            result = matrix1.T
        elif operation == "transpose2":
            result = matrix2.T
        elif operation == "determinant1":
            result = np.linalg.det(matrix1)
        elif operation == "determinant2":
            result = np.linalg.det(matrix2)
        else:
            result = "Unknown operation"
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"result": result.tolist() if isinstance(result, np.ndarray) else result})

if __name__ == "__main__":
    app.run(debug=True)
