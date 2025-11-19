from flask import Flask, request, jsonify
app = Flask(__name__)
current_direction = 'stop'
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
@app.route('/controls', methods=['OPTIONS'])
def handle_options():
    return '', 200
@app.route('/controls', methods=['POST'])
def set_direction():
    global current_direction
    try:
        data = request.get_json()
        direction = data.get('direction')
        valid_directions = ['forward', 'backward', 'left', 'right', 'stop']
        
        if direction in valid_directions:
            current_direction = direction
            print(f"Server updated state: {current_direction}")
            return jsonify({"status": "success", "direction": current_direction}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid direction"}), 400
    except Exception as e:
        print(f"Error processing POST request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/status', methods=['GET'])
def get_direction():
    return jsonify({"direction": current_direction}), 200
if __name__ == '__main__':
    print("Starting Flask server on http://0.0.0.0:5000. No sudo required.")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
