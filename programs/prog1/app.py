from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import os, time, json, sys

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Program2', version='2.0.0')

success_counter = metrics.counter(
    'success_requests', 'Count of successful responses',
    labels={'status': lambda r: r.status_code}
)

# Parse JSON string passed via command-line argument
if len(sys.argv) < 3:
    print("Usage: python3 app.py '<json_string>' <port>")
    sys.exit(1)

json_string = sys.argv[1]
try:
    data_pers = json.loads(json_string)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    sys.exit(1)

@app.route('/')
@success_counter
def main():
    return "Program1"

@app.route('/health')
def health_check():
    return "Healthy", 200

@app.route('/ident', methods = ['POST'])
def ident_check():
    # Parse the incoming JSON data
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400
    else:
      # Extract and compare values
      name1 = data.get("password")
      password1 = data.get("password")
      name2 = data_pers.get("name")
      password2 = data_pers.get("password")
      if password1 == password2:
          pid = os.getpid()
          ident = data_pers.get("ident")
          start = data_pers.get("start_time")
          planning_duration = data_pers.get("rand_duration")
          uptime = time.clock_gettime(time.CLOCK_BOOTTIME)
          return jsonify({
              "name": name1,
              "pid": pid,
              "ident": ident,
              "start": start,
              "planning_duration": planning_duration,
              "uptime": uptime
          })
      else: 
          return jsonify({"error": "Invalid login or password"}), 400

if __name__ == '__main__':
    port = int(sys.argv[2])
    app.run(port=port)
