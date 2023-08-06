import os
from aiohttp import web
import jwt
import motor.motor_asyncio
from bson import ObjectId
from flatten_dict import flatten

SECRET = os.getenv("SECRET")
DB_URL = os.getenv("DB_URL")
DB = os.getenv("DB")
client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL, 27017)
db = client[DB] # test

def point_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return k1 + "." + k2

def set_cors_headers (request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

async def cors_factory (app, handler):
    async def cors_handler (request):
        # preflight requests
        print(request)
        if request.method == 'OPTIONS':
            return set_cors_headers(request, web.Response())
        else:
            response = await handler(request)
            return set_cors_headers(request, response)
    return cors_handler


def jwt_auth(f):
    async def helper(request):
        try:
            payload = jwt.decode(request.headers['Authorization'], SECRET, algorithms=['HS256'])
            return await f(request, payload)
        except Exception as e:
            return web.json_response({'error': str(e)})
    return helper

def validate(validator, update=False):
    def decorator(f):
        async def helper(request, payload):
            document = await request.json()             
            if validator.validate(document, update=update):
                return await f(document, request, payload)
            else:
                return web.json_response({'error': 'not valid document'})                 
        return helper
    return decorator

def validate_push(validator):
    def decorator(f):
        async def helper(request, payload):
            attr = request.match_info.get('push')
            document = await request.json()             
            if validator.validate(document):
                return await f(document, request, payload)
            else:
                return web.json_response({'error': 'not valid document'}) 
        return helper
    return decorator

def has_role(role):
    def decorator(f):
        async def helper(request, payload):
            if role in payload['roles']:
                return await f(request, payload)
            else:
                return {'error': 'not authorized'}
        return helper
    return decorator

def is_owner(col):
    def decorator(f):
        async def helper(request, payload):
            _id = request.match_info.get('_id')
            old_doc = await db[col].find_one({'_id': ObjectId(_id)})
            if payload['user'] == old_doc["__owner"]:
                return await f(request, payload)
            else:
                return {'error': 'not authorized'}
        return helper
    return decorator

def get(col):
    def decorator(f):
        async def helper(request, payload):
            _id = request.match_info.get('_id')
            document = await db[col].find_one({'_id': ObjectId(_id)})
            document = await f(document)
            document['_id'] = str(document['_id'])
            return web.json_response(document)
        return helper
    return decorator

def get_many(col):
    def decorator(f):
        async def helper(request, payload):
            query, skip, limit = await f(request.query)
            cursor = db[col].find(query).skip(skip).limit(limit)
            documents = await cursor.to_list(length=100)
            ret = []
            for d in documents:
                d['_id'] = str(d['_id'])
                ret.append(d)
            return web.json_response(ret)
        return helper
    return decorator

def insert(col):
    def decorator(f):
        async def helper(document, request, payload):
            document = await f(document, request, payload)
            document['__owner'] = payload['user']   
            result = await db[col].insert_one(document)
            document['_id'] = str(result.inserted_id)
            return web.json_response(document) 
        return helper
    return decorator

def update(col):
    def decorator(f):
        async def helper(document, request, payload):
            document = await f(document, request, payload)
            document = flatten(document, reducer=point_reducer)
            _id = request.match_info.get('_id')
            await db[col].update_one({'_id': ObjectId(_id)}, {'$set': document})        
            document['_id'] = _id
            return web.json_response(document)
        return helper
    return decorator

def push(col):
    def decorator(f):
        async def helper(document, request, payload):
            document = await f(document, request, payload)
            _id = request.match_info.get('_id')
            attr = request.match_info.get('push')
            document['_id'] = ObjectId()
            await db[col].update_one({'_id': ObjectId(_id)}, {'$push': {attr: document}})        
            document['_id'] = str(document['_id'])
            return web.json_response(document)
        return helper
    return decorator

def pull(col):
    def decorator(f):
        async def helper(request, payload):
            await f({}, request, payload)
            _id = request.match_info.get('_id')
            attr = request.match_info.get('pull')
            sub_id = request.match_info.get('sub_id')
            document = {'_id': ObjectId(sub_id)}
            await db[col].update_one({'_id': ObjectId(_id)}, {'$pull': {attr: document}})        
            return web.json_response({})
        return helper
    return decorator

def json_response(f):
    async def helper(request):
        document = await f(request)
        return web.json_response(document)
    return helper

def delete(col):
    def decorator(f):
        async def helper(request, payload):
            _id = request.match_info.get('_id')
            document = await db[col].delete_one({'_id': ObjectId(_id)})
            return web.json_response({})
        return helper
    return decorator