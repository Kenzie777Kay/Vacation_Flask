from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Vacation, vacation_schema, vacations_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{'yee':'haw'}

@api.route('/vacations', methods = ['POST'])
@token_required
def create_vacation(current_user_token):
    destination = request.json['destination']
    flight = request.json['flight']
    food = request.json['food']
    lodging = request.json['lodging']
    souvenirs = request.json['souvenirs']
    activities = request.json['activities']
    total = request.json['total']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    vacation = Vacation(destination, flight, food, lodging, souvenirs, activities,total, user_token=user_token )

    db.session.add(vacation)
    db.session.commit()

    response = vacation_schema.dump(vacation)
    return jsonify(response)

@api.route('/vacations', methods = ['GET'])
@token_required
def get_canning(current_user_token):
    a_user = current_user_token.token
    vacations = Vacation.query.filter_by(user_token = a_user).all()
    response = vacations_schema.dump(vacations)
    return jsonify(response)

@api.route('/vacations/<id>', methods = ['POST','PUT'])
@token_required
def update_vacation(current_user_token,id):
    vacation = Vacation.query.get(id) 
    vacation.destination = request.json['destination']
    vacation.flight = request.json['flight']
    vacation.food = request.json['food']
    vacation.lodging = request.json['lodging']
    vacation.souvenirs = request.json['souvenirs']
    vacation.activities = request.json['activities']
    vacation.total = request.json['total']
    vacation.user_token = current_user_token.token

    db.session.commit()
    response = vacation_schema.dump(vacation)
    return jsonify(response)

@api.route('/vacations/<id>', methods = ['DELETE'])
@token_required
def delete_vacation(current_user_token, id):
    vacation = Vacation.query.get(id)
    db.session.delete(vacation)
    db.session.commit()
    response = vacation_schema.dump(vacation)
    return jsonify(response)