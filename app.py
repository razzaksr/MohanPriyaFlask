from flask import Flask,make_response,render_template,jsonify,request,session
from flask_mongoengine import MongoEngine
from flask_cors import CORS

app=Flask(__name__)

# database configuration
app.config['MONGODB_HOST']="mongodb+srv://razak:mohamed@cluster0.ptmlylq.mongodb.net/forenoon?retryWrites=true&w=majority"

# Object Document Mapping config
mydb=MongoEngine()
mydb.init_app(app)
CORS(app)

class Bike(mydb.Document):
    regno=mydb.StringField()
    model=mydb.StringField()
    brand=mydb.StringField()
    year=mydb.IntField()
    cc=mydb.FloatField()
    price=mydb.IntField()
    
    # def __init__(self,reg="",mod="",bnd="",yr=0,cc=0,price=0):
    #     super().__init__(self)
    #     self.regno=reg
    #     self.model=mod
    #     self.brand=bnd
    #     self.year=yr
    #     self.cc=cc
    #     self.price=price
    
@app.route("/erase/<reg>",methods=['DELETE'])
def deleting(reg):
    check=Bike.objects(regno=reg).first()
    check.delete()
    return jsonify(reg+" vehicle has deleted")

@app.route("/brand/<bnd>")
def getByBrand(bnd):
    return jsonify(Bike.objects(brand=bnd))

@app.route("/budget/<int:cost>")
def getByPrice(cost):
    return jsonify(Bike.objects(price__lte=cost))

@app.route("/year/<int:yr>")
def getByYear(yr):
    return jsonify(Bike.objects(year__gte=yr))
    
@app.route("/<reg>",methods=['GET','PUT'])
def getByRegno(reg):
    if request.method=="GET":
        one=Bike.objects(regno=reg).first()
        return jsonify(one)
    else:
        hai=request.json
        Bike.objects(regno=reg).update_one(set__brand=hai['brand'],set__model=hai['model'],set__cc=hai['cc'],set__price=hai['price'],set__year=hai['year'])
        return jsonify(Bike.objects(regno=reg))

@app.route("/create",methods=['POST'])
def addNew():
    hai=request.json
    bike = Bike()
    bike.brand=hai['brand']
    bike.model=hai['model']
    bike.regno=hai['regno']
    bike.year=hai['year']
    bike.cc=hai['cc']
    bike.price=hai['price']
    
    bike.save()    
    return jsonify(bike)
  
@app.route("/", methods=['GET'])
def showAll():
    return jsonify(Bike.objects.all())
    

# @app.route("/dummy")
# def adding():
#     bike=Bike()
#     bike.regno="TN54M0635"
#     bike.model="Apache 200"
#     bike.brand="TVS"
#     bike.year=2016
#     bike.cc=200
#     bike.price=112300
    
#     bike.save()
    
#     return jsonify(bike)



@app.route("/hi")
def hello():
    return make_response("<h1>Happy to welcome you to the world of  Flask Framework</h1>")

@app.route("/mypage")
def some():
    return render_template('sap.html')

@app.route("/passing",methods=['GET'])
def wind():
    return render_template('myparams.html',manoj="Java FSD Trainer")

@app.route("/mine/<int:dt>")
def say(dt):
    access=dt*4
    return render_template('myparams.html',manoj=access)

if __name__=="__main__":
    app.run(debug=True,port=1122)