from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    
    try:
        if language == 'python':
            output = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT)
        elif language == 'javascript':
            output = subprocess.check_output(['node', '-e', code], stderr=subprocess.STDOUT)
        elif language == 'cpp':
            with open('temp.cpp', 'w') as f:
                f.write(code)
            subprocess.check_output(['g++', 'temp.cpp', '-o', 'temp'])
            output = subprocess.check_output(['./temp'], stderr=subprocess.STDOUT)
        elif language == 'java':
            with open('Temp.java', 'w') as f:
                f.write(code)
            subprocess.check_output(['javac', 'Temp.java'])
            output = subprocess.check_output(['java', 'Temp'], stderr=subprocess.STDOUT)
        else:
            output = b'Unsupported language.'
        
        return jsonify({'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output.decode('utf-8')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
