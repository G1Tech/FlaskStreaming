from flask import *
import things
import time

app = Flask(__name__)
pi_things = things.PiThings()

@app.route("/")
def hello():
      button = pi_things.read_button()
      return render_template('index.html', button=button)

@app.route("/led/<int:state>", methods=['POST'])
def led(state):
    if state == 0:
        pi_things.set_led(False)
    elif state == 1:
        pi_things.set_led(True)
    else:
        return ('Unknown LED state', 400)
    return ('', 204)

@app.route("/switch")
def switch():
    def read_button():
        while True:
            button = pi_things.read_button()
            yield 'data: {0}\n\n'.format(button)
            time.sleep(1.0)
    return Response(read_button(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80, threaded=True)
