from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, PythonAnywhere!"

if __name__ == '__main__':
    app.run(debug=True)
# from app import app
#
# if __name__ == '__main__':
#     app.run(debug=True)
