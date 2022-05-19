from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    return render_template('index.html', data = todoItems)

@app.route("/create/todo", methods=["POST"])
def addTodo():
    if(request.method == 'POST'):
        description = request.form.get('description')
        new_todo = Todo(description = description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    return 'request method not allowed'
