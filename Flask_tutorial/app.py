# imports
from flask import Flask, render_template, request, redirect, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# MyApp
app = Flask(__name__)
# Scss(app)

# DB Connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# DB Models (Schema)
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Task {self.id}'

# Routes to webpages
@app.route("/", methods=["GET","POST"])     # homepage
def index():
    # Add tasks
    if request.method == "POST":
        # collect content from Form
        new_task_content = request.form['content']
        new_task = MyTask(content=new_task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f'Error while adding task: {e}'
            
    # See all current tasks
    tasks = MyTask.query.order_by(MyTask.created.desc()).all()
    return render_template("index.html", tasks = tasks)

# Delete a Task
@app.route("/delete/<int:id>")
def delete(id:int):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f'Error while deleting Task: {e}'

# Edit a Task    
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task_to_edit = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f'Error while editing Task: {e}'
        
    return render_template('edit.html', task=task_to_edit)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)