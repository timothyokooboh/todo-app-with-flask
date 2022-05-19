from flask import Flask, render_template, request, url_for, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5432/todoapp"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)

    def __repr__ (self):
        return f'<Todo id={self.id} description={self.description}>'

@app.route("/")
def index():
    todoItems = Todo.query.all()
    return render_template("index.html", data = todoItems)

@app.route("/todos/get", methods=['GET'])
def getTodos():
    todoItems = Todo.query.all()
    
    return {'data:': jsonify(todoItems)}

@app.route("/todo/create", methods=["POST"])
def addTodo():
    data = {}
    error = False

    try:
        description = request.get_json()['description']
        new_todo = Todo(descriptionx = description)
        db.session.add(new_todo)
        db.session.commit()
        data = { 'description': new_todo.description }
    except: 
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return data
    

