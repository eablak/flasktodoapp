from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

#Temel modulleri indirdikten sonra yine temel fonksiyonları yazıyoruz.
#Aşağıdaki üç fonksiyon Flask_sqlalchemy sitesinden.
#2. satırın sonuna kendi todo.db adresimizi ekliyoruz (en sona todo.db biz yazdık) ve slash işaretlerini ters olarak ekliyoruz.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ESRA  ABLAK/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app) 

@app.route("/")
def index():
    todos =  Todo.query.all() 
#Bu satır ile Todo'ya yazdığımız bilgileri alıyoruz ve bunları index.html'de oluşturduğumuz tabloya eklemek için kullanıyoruz
    return render_template("index.html",todos = todos)


#Burası ile durum güncelledeki butona basarak değişiklik yapıyoruz.
#Fonksiyondaki ilk satır siteden örnek alınarak yazıldı.
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first() 
    """
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False
    """
    todo.complete = not todo.complete 
    db.session.commit()  #Veritabanında değişiklik yaptığımızı söylüyoruz.
    return redirect(url_for("index"))

#index.html de yazdığımız form kısmını burada sadece post methodunu yazarak alıyoruz.
#yazılan işlemler Flask_sqlalchemy sitesine bakılarak yazıldı.
#bu işlem sayesinde forma yazdığımız başlığı db browser'e gönderebiliyoruz.
@app.route("/add",methods=["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

#Class'ı yine sayfadan bakarak yazdık.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

#Servir'i (sunucuyu) ayağa kaldırmak için klasik olan fonksiyonumuzu yazıyoruz.
if __name__ == "__main__":
    db.create_all()  #Class'ı oluşturuyor.
    app.run(debug=True)