from flask import Flask,request,render_template,redirect


app = Flask(__name__)
Users = {
    1: {'name': '张三', 'age': 18, 'gender': '男', 'text': "道路千万条"},
    2: {'name': '张三', 'age': 18, 'gender': '男', 'text': "道路千万条"},
    3: {'name': '张三', 'age': 18, 'gender': '男', 'text': "道路千万条"},
}
app.config["DEBUG"]=True
app.config.from_object("setting.FlaskSetting")
#method=['GET','POST']
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        name=request.form.get('name')
        pwd=request.form.get('pwd')
        if name == 'pdun' and pwd == '123':
            return redirect('/')
        else:
            return render_template('login.html',error="用户名密码错误")

@app.route('/')
def index():
    return render_template('index.html',user=Users)

@app.route('/detail/<int:id>')
def detail(id):
    user = Users[id]
    return render_template('detail.html',user=user)

if __name__ == '__main__':
    app.run()
