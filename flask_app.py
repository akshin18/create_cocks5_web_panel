from flask import Flask,render_template, url_for,request,redirect
from upup import *
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False




class Article(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    proxy_ip = db.Column(db.String(100),nullable=False )



    def __repr__(self):
        return '<Article %r>' % self.id




@app.route('/',methods=['POST','GET'])
def index():

    if request.method == 'POST':
        admin_login = request.form['login']
        admin_password = request.form['password']
        if admin_login == '123' and admin_password == '123':
            return render_template('dash.html',action=Article.query.all())
        else:
            return render_template('index_error_login.html')

    else:return render_template('index.html')



@app.route('/tambol', methods=['POST','GET'])
def cartez():

    if request.method == 'POST':
        try:




            if request.form['submit_button'] == 'up_proxy':
                a = request.form['input_value']

                if a != '':

                    dann = a.split(':')

                    main_deploy(dann[0],dann[1],dann[2],dann[3],dann[4])

                    article = Article(proxy_ip=a)
                    try:
                        db.session.add(article)
                        db.session.commit()
                    except:
                        print('cart')




                return render_template('dash.html',action=Article.query.all())
            elif request.form['submit_button'] == 'reload_proxy':
                a = request.form['input_value']
                daan3 = a.split(':')
                proxy_restart(daan3[0],daan3[1],daan3[2])
                return render_template('dash.html', action=Article.query.all())
            elif request.form['submit_button'] == 'delete_proxy':
                a = request.form['input_value']
                daan2 = a.split(':')
                proxy_stop(daan2[0],daan2[1],daan2[2])
                articles = Article.query.all()

                for i in articles:
                    if   a.split(':')[0] in i.proxy_ip:
                        db.session.delete(i)
                        db.session.commit()
                        break

                return render_template('dash.html', param1=3,action=Article.query.all())



        except:

            render_template('index.html')

    render_template('index.html')



@app.errorhandler(500)
def internal_error(error):

    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

@app.route('/main')
def maino():
    return 'About page'

if __name__ == '__main__':
    app.run()