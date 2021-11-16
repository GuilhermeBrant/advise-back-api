from flask import Flask 
from flask_restx  import Api
from flask_cors import CORS

class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app, 
            version='1.0',
            title='advise API',
            description='advise API will help you in the destination of your emigration.',
            doc='/docs'
        )

    def run(self, ):
        self.app.run(
            debug=True
        )

server = Server()