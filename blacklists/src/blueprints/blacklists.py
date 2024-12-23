from flask import Blueprint, request, jsonify
from ..commands.create_blacklist import CreateBlacklist
from ..commands.getList import getBlacklist
from ..commands.authenticate import Authenticate
from ..errors.errors import MissingToken

blacklists_blueprint = Blueprint('blacklists', __name__)

@blacklists_blueprint.route('/blacklists', methods=['POST'])
def create():
    auth = Authenticate(auth_token()).verify()
    
    if auth == True:
        client_ip = request.remote_addr
        black = CreateBlacklist(request.get_json(), client_ip).execute()
        return black, 201

@blacklists_blueprint.route('/blacklists/ping', methods=['GET'])
def ping():
    return jsonify('pong'), 200
    

@blacklists_blueprint.route('/blacklists/<email>', methods=['GET'])
def ValidarEmail(email):
    auth = Authenticate(auth_token()).verify()

    if auth == True:
        black = getBlacklist(email).validar_email()

        return jsonify(black), 200
    
def auth_token():
    try:
        if 'Authorization' in request.headers:
            authorization = request.headers['Authorization']            
        else:
            raise MissingToken()
        return authorization
    except Exception as e:
        raise MissingToken()
   
