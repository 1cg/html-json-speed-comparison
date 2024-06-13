from flask import (
    Flask, request, render_template, g as app_ctx
)
import time
from contacts import Contact

# ========================================================
# Flask App
# ========================================================

app = Flask(__name__)

# don't cache responses
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = b'html/json speed comparison'

Contact.load_db()


@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint
    print('%s ms %s %s %s' % (time_in_ms, request.method, request.path, dict(request.args)))
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/full-html")
def full_html():
    return render_template("full-html.html", contacts=Contact.all())


@app.route("/partial-html")
def parital_html():
    return render_template("rows.html", contacts=Contact.all())


@app.route("/json")
def json_response():
    return Contact.all()


if __name__ == "__main__":
    app.run()
