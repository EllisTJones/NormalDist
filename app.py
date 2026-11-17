from flask import Flask, jsonify, request, send_from_directory

from calc import compute

app = Flask(__name__, static_folder="static")


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/calc")
def api_calc():
    try:
        return jsonify(compute(request.args))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    # debug=True reloads the server automatically whenever you save a .py file
    app.run(debug=True)