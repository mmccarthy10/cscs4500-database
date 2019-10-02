from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<a href='./login'>Click here to login</a>"

@app.route("/login")
def login():
    return "Thank you for logging in!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
