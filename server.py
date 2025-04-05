from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
