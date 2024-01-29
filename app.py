from flask import Flask, redirect, url_for, render_template, request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.secret_key = "hello" # this secret key is for session store
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Role(db.Model):
     __tablename__ = 'Roles'
     unique_id = db.Column(db.Integer,primary_key=True)
     role_name =db.Column(db.String(100))
     role_code =db.Column(db.String(100))
     role_description =db.Column(db.String(180))
     def __repr__(self):
        return '<Role %r>' % self.role_name

@app.route("/")
def home():
	return 'Hello World'

@app.route("/roles")
def roles():
    roles = Role.query.order_by(Role.role_name).all()
    return render_template("roles.html",roles=roles)

@app.route("/add-role", methods=["GET","POST"])
def addRole():
    if request.method == 'POST':
          #  return jsonify(request.form)  #this will return all the request in json format 
         role_name = request.form['role_name']
         role_code = request.form['role_code']
         role_description = request.form['role_description']
         role = Role(role_name=role_name,role_code=role_code,role_description=role_description)
         db.session.add(role)
         db.session.commit()
         flash('Role Added Successfully','success')
         return redirect('/roles')
    else:
        
        return render_template("addRole.html")
    
@app.route("/update-role/<id>", methods=["GET","POST"])
def updatRole(id):
    if request.method == 'POST':
         role = Role.query.filter_by(unique_id=id).first()
         role.role_name = request.form['role_name']
         role.role_code = request.form['role_code']
         role.role_description = request.form['role_description']
         db.session.add(role)
         db.session.commit()
         flash('Role Updated Successfully','success')
         return redirect('/roles')
    else:
        role = Role.query.filter_by(unique_id=id).first()
        return render_template("updateRole.html",role=role)
    
@app.route("/delete-role/<id>", methods=["GET","POST"])
def deleteRole(id):
        role = Role.query.filter_by(unique_id=id).first()
        db.session.delete(role)
        db.session.commit()
        flash('Role Deleted Successfully','warning')
        return redirect('/roles')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)