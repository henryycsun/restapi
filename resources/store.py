from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store {} not found!'.format(name)}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store {} already exists!'.format(name)}, 400

        store = StoreModel(name)

        try:
            store.upsert_to_db()
        except:
            return {'message':'An error occurs when adding the store!'}, 500

        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message':"Store {} deleted!".format(name)}

class Stores(Resource):
    def get(self):
        return {'Stores':[store.json() for store in StoreModel.query.all()]}
