from flask import Flask, send_from_directory, render_template


app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def serve_index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
