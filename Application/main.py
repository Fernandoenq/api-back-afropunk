from flask import Flask
from flask_cors import CORS
from Application.Controllers.PersonController import PersonController
from Application.Controllers.OrganizerController import OrganizerController
from Application.Controllers.ImageController import ImageController

app = Flask(__name__)
CORS(app, origins='*')

PersonController.setup_controller(app)
OrganizerController.setup_controller(app)
ImageController.setup_controller(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3335)
    app.run(debug=True)
