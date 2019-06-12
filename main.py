from flask import Flask, request, jsonify, abort
from google.appengine.ext import ndb
from marshmallow import Schema, fields
import werkzeug
import logging
#simple flask app
app = Flask(__name__)
app.debug = True


class customer(ndb.Model):
    firstname = ndb.StringProperty()
    account_number = ndb.StringProperty()
    lastname = ndb.StringProperty()
    # set value on create only
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    # update value every time the entity is updated
    updated_at = ndb.DateTimeProperty(auto_now=True)

# JSON serialization
class PostSerializer(Schema):
    #This produces a result like agVoZWxsb3IPCxIHQWNjb3VudBiZiwIM 
    #Returns a websafe-base64-encoded serialized version of the key.
    #which can later be used to reconstruct the key and retrieve the original entity:
    
    id = fields.Function(lambda obj: obj.key.urlsafe())
    class Meta:
        fields = (
            "id", "firstname","lastname", "account_number",
              "created_at", "updated_at"
        )

post_schema = PostSerializer()
posts_schema = PostSerializer(many=True)

@app.route('/')
def index():
    return "Welcome Datastore API"

@app.route('/createCustomer', methods = ['POST'])
def create():
    # check if json input
    if not request.is_json:
        abort(400, "only json please")

    record = customer(
        firstname=request.json['firstname'],
        lastname=request.json['lastname'],
        account_number=request.json['account_number'])

    # push to datastore
    record.put()

    # return as json
    return jsonify(post_schema.dump(record).data)

@app.route('/getCustomers')
def fetch():
    #fetch
    posts = customer.query().fetch()

    # return as json
    return jsonify({ 'customer_record': posts_schema.dump(posts).data })

@app.route('/getCustomerId')
def get():
    #fetch by id
    post_id = request.args.get('id')
    if post_id == None:
        return abort(400, "please provide a record id")

    # get record by id
    try:
        key = ndb.Key(urlsafe=post_id)
        record = key.get()

        if record == None:
            return not_found("record was not found")

        # return as json
        return jsonify(post_schema.dump(record).data)
    except Exception, e:
        return abort(400, e)


@app.route('/deleteCustomer', methods = ['POST'])
def delete():
    """ delete a record """
    try:
        key = ndb.Key(urlsafe=request.json['id'])
        key.delete()
        return jsonify({'status': 'ok'}), 200
    except Exception, e:
        return abort(400, e)

@app.route('/updateCustomer', methods = ['POST'])
def update():
    """ update a record """
    # allow only json
    if not request.is_json:
        abort(400, "json only please")

    try:
        key = ndb.Key(urlsafe=request.json['id'])
        record = key.get()
        # if no entity with given id exists
        # return a 404 not found
        if record == None:
            return not_found("record was not found")

        json = request.json or {}

        if 'firstname' in json:
            record.firstname = json['firstname']
        if 'account_number' in json:
            record.account_number  = json['account_number']
        if 'lastname' in json:
            record.lastname = json['lastname']
        record.put()

        return jsonify(post_schema.dump(record).data)
    except Exception, e:
        return abort(400, e)

def not_found(message='resource was not found'):
    return jsonify({
        'http_status': 404,
        'code': 'not_found',
        'message': message
    }), 404

@app.errorhandler(werkzeug.exceptions.BadRequest)
def bad_request(e):
    return jsonify({
        'http_status': 400,
        'code': 'bad_request',
        'message': '{}'.format(e)
    }), 400
