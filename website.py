from flask import Flask, request, make_response
from processor import process_calendars

app = Flask(__name__)

@app.route('/process')
def process():
    response = make_response(process_calendars(request.args.getlist('courses')).decode('utf-8'))
    response.headers["Content-type"] = "text/plain; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(debug=True)
