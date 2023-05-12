
import cv2
import base64
import numpy as np
from PIL import Image
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from image_process import process

app = Flask(__name__)
app.secret_key = 'ptSecret'
app.config['SECRET_KEY'] = 'ptSecret'
socketio = SocketIO(app)


# ---- Endpoints ----
@app.route('/')
def home():
    return render_template('index.html')


# ---- Web sockets contra el frontend ----
@socketio.on("traducir")
def traducir(base64_string):
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (1664,137), Image.LANCZOS)
    #cv2.imwrite("static/images/braille_image.jpg", image)
    #image_loc= "static/images/braille_image.jpg"
    #image= cv2.imread(image_loc)
    braille_text= process(image)
    emit('traducido', braille_text)

  
if __name__ == "__main__":
    # Certificados SSL:
    # https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    app.run(debug=True, host="0.0.0.0", port=5020, ssl_context='adhoc')
