from flask_restful import Resource
from flask import request, jsonify, render_template, app, make_response

from caci.model.models import Profile, db, ProfileSchema
from caci.info.info import load
from pymongo import  MongoClient
from flask_paginate import Pagination, get_page_parameter, get_page_args
from bson.json_util import dumps, loads
import os

# Database configuration

# myclient = MongoClient("mongodb://localhost:27017/")
myclient = MongoClient(os.environ['DB_PORT_2707_TCP_ADDR'],27017, connect=True)
# myclient = MongoClient(os.environ['DB_PORT_2707_TCP_ADDR'], 27017)
mydb = myclient["restdb"]
mycol = mydb["people"]


profile_schema = ProfileSchema(many=True)
profile_s = ProfileSchema()
data = load()



def information_db():
    for item in data:
        mycol.insert_one(item)
# information_db()

class ProfilesList(Resource):

    def get(self):

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        cursor = mycol
        urls = cursor.find({}).skip(offset).limit(per_page)
        total = cursor.count()
        pagination = Pagination(page=page,
                                per_page=per_page,
                                total=1000,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                css_framework='foundation')
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', urls=urls, response=data, pagination = pagination),200)


    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input provided'}, 400

        data = profile_s.load(json_data)
        profiles = Profile(
                    job=json_data['job'],
                    company=json_data['company'],
                    ssn=json_data['ssn'],
                    residence=json_data['residence'],
                    blood_group=json_data['blood_group'],
                    username=json_data['username'],
                    name=json_data['name'],
                    sex=json_data['sex'],
                    address=json_data['address'],
                    mail=json_data['mail'],
                    birthdate=json_data['birthdate']
        )
        db.session.add(profiles)
        db.session.commit()
        result = profile_s.dump(profiles).data
        return {'status': 'success', 'data' : result}, 201

class ProfileJson(Resource):
    def get(self,p):
        if p != 1:
            count = int(p) * 10
            profile = []
            print(count)
            for row in mycol.find().skip(count).limit(10):
                row.pop('_id')
                profile.append(row)
            return {'status': 'success', 'data': profile}, 200
        else:
            profile = []
            for row in mycol.find().limit(10):
                row.pop('_id')
                profile.append(row)
        return {'status': 'success', 'data': profile}, 200


class ProfileIn(Resource):

    def get(self,username):
        profiles = []
        for pro in mycol.find({'username': username}):
            pro.pop('_id')
            profiles.append(pro)

        for p in profiles:
            if p['username'] == username:
                return {'status': 'success', 'data': p}, 200
        return {'message':'Username {} not found'.format(username)}


class ProfileDelete(Resource):

    def delete(self, username):
        search = False
        for pro in mycol.find({'username': username}):
            search = True
            mycol.remove(pro)
        if search:
            return {'success': 'Deleted'}
        else:
            return {'message': 'Username {} not found'.format(username)}

