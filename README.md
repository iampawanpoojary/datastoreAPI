## Datastore App Engine (standard) API

You can see the output and make API calls in the python notebook below:
https://colab.research.google.com/github/iampawanpoojary/datastoreAPI/blob/master/datastoreAPI.ipynb

Sample record:
```
  {
      "account_number": "103", 
      "created_at": "2019-06-11T08:05:43.442680+00:00", 
      "firstname": "george", 
      "id": "agpzfnppbWFibHVlchULEghjdXN0b21lchiAgIDAl6SACgw", 
      "lastname": "harrison", 
      "updated_at": "2019-06-11T08:05:43.442686+00:00"
    }
```
id - Key (auto generated, urlsafe() Returns a websafe-base64-encoded serialized version of the key.)
created_at and updated_at are generated automatically.

## Functions

### /getCustomers
```
https://zimablue.appspot.com/getCustomers
```
This displays all records in the datastore

### /getCustomerId
```
https://zimablue.appspot.com/getCustomerId?id={"agpzfnppbWFibHVlchULEghjdXN0b21lchiAgIDAl6SACgw"}
```
Fetches the records matching id={"my-id"}

### /createCustomer
```
curl -X POST -H 'Content-Type: application/json' -d \
'{
  "firstname": "john",
  "lastname": "lenon",
  "account_number": "101",
}' https://zimablue.appspot.com/createCustomer
```
Creates a new record

### /updateCustomer
```
curl -X POST -H 'Content-Type: application/json' -d \
'{
  "firstname": "john",
  "lastname": "Ono",
  "account_number": "103",
  "id": "agpzfnppbWFibHVlchULEghjdXN0b21lchiAgICgpJWCCgw"
}' https://zimablue.appspot.com/updateCustomer
```
Updates the record based on Id


### /deleteCustomer
```
curl -X POST -H 'Content-Type: application/json' -d \
'{
  "id": "agpzfnppbWFibHVlchULEghjdXN0b21lchiAgICA3oyQCgw"
}' https://zimablue.appspot.com/deleteCustomer
```
Deletes the record based on Id

