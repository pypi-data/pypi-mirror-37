# API Decorators

```python
from api import jwt_auth, is_owner, get, insert, is_owner, has_role, update, push, pull, \
                validate, validate_push
from cerberus import Validator

schema = {
    'author': {'type': 'string'},
    'title': {'type': 'string'}
}

validator = Validator(schema)

schema_comments = {
    'author': {'type': 'string'},
    'message': {'type': 'string'}
}

validator_comments = Validator(schema_comments)

def set_routes_book(routes):

    @routes.get('/api/book')
    @jwt_auth
    #@is_owner('book')
    @get_many('book')
    async def get_many_book(query):  
        author = query["author"]
        return {"author": author}, 0, 10 # mongo query, skip and limit

    @routes.get('/api/book/{_id}')
    @jwt_auth
    #@is_owner('book')
    @get('book')
    async def get_book(document):      
        return document

    @routes.put('/api/book/{_id}/push/{push}')
    @jwt_auth
    #@is_owner('book')
    @validate_push(validator=validator_comments)
    @push('book')
    async def handle_push(document, request, payload):      
        return document

    @routes.put('/api/book/{_id}/pull/{pull}/{sub_id}')
    @jwt_auth
    #@is_owner('book')
    @pull('book')
    async def handle_pull(document, request, payload):      
        pass

    @routes.post('/api/book')
    @jwt_auth
    @validate(validator=validator)
    @insert('book')
    async def handle_post(document, request, payload):
        return document       
    
    @routes.put('/api/book/{_id}')
    @jwt_auth
    #@is_owner('book')
    @validate(update=True, validator=validator)
    @update('book')
    async def handle_put(document, request, payload):      
        return document    
```
