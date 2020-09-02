from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from voice_forge.configs import set_up_db, get_config
from voice_forge.handlers import *

app = Flask('Loult Panopticon API')
# allowing Cross origin requests
CORS(app)

# retrieving the right config, using the FLASK_CONFIG env variable.
config = get_config()
app.config.from_object(config)
set_up_db(config)

# Wrapping the app with the Smorest Api Object
api = Api(app)

# registering the RESTful API blueprints
api.register_blueprint(recordings_blp)

if __name__ == '__main__':
    app.run()