from flask import Flask, request, render_template_string
import subprocess
import sys
from io import StringIO

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Python Test Page</title>
</head>
<body>
  <h2>Run Command on Server</h2>
  <form action="/run" method="post">
    <input type="text" name="command" required>
    <button type="submit">Run Command</button>
  </form>

  <h2>Run Python Code</h2>
  <form action="/execute_python" method="post">
    <textarea name="python_code" rows="5" cols="50" required></textarea><br>
    <button type="submit">Run Python Code</button>
  </form>

  {% if result %}
    <h3>Output:</h3>
    <pre>{{ result }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/run', methods=['POST'])
def run_command():
    command = request.form['command']
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
    except subprocess.CalledProcessError as e:
        output = f"An error occurred: {e}"
    return render_template_string(HTML, result=output)

@app.route('/execute_python', methods=['POST'])
def execute_python():
    python_code = request.form['python_code']
    output = ""
    try:
        stdout = sys.stdout
        sys.stdout = StringIO()
        exec(python_code)
        output = sys.stdout.getvalue()
        sys.stdout = stdout
    except Exception as e:
        output = f"An error occurred: {e}"
    return render_template_string(HTML, result=output)

if __name__ == '__main__':
    app.run(debug=True)

