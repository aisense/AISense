from operator import methodcaller
import MySQLdb
from flask import request, make_response, jsonify, render_template, session, g
from flask.ext.socketio import emit, disconnect, close_room, leave_room, join_room
from application import application
from main.ml.companyAnalysis import predictor
from main.ml.dbAccess import dbAccessor
from main.ml.patternAnalysis import patternAnalyser
from main.ml.portfolioAnalysis import portfolioPredictor
from main.utils import bot

__author__ = 'Gangeshwar'
chatbot = None


@application.route('/index')
@application.route('/')
def index():
    return 'Welcome to AISense!'


@application.route('/login', methods=['POST'])
def login():
    userId = str(request.form['username'])  # , type=str)
    password = str(request.form['password'])  # , type=str)
    db = MySQLdb.connect("localhost", "root", "root", "socgen")
    cursor = db.cursor()
    query = "select * from users where uid = " + userId
    cursor.execute(query)
    user = cursor.fetchone()
    print(user)
    if user is None:
        response = make_response(jsonify(fail='User doesn\'t exist. Sign up before you auth!'), 400)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return response
    if not user[1] == password:
        response = make_response(jsonify(fail='Username and Password doesn\'t match.'), 400)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return response

    session['uid'] = user[0]
    response = make_response(jsonify(success='Login successful!'), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/create_bot')
def create_bot():
    global chatbot
    chatbot = bot()
    response = make_response(jsonify(reply="Why are you sending me an empty message? :/"), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/refresh')
def refresh_bot():
    global chatbot
    chatbot = bot()
    response = make_response(jsonify(success="Bot refreshed."), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/chat', methods=['POST'])
def chat1():
    global chatbot
    try:
        msg = str(request.form['msg'])
    except:
        response = make_response(jsonify(reply="Why are you sending me an empty message? :/"), 200)
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return response
    if msg == '':
        response = make_response(jsonify(reply="Why are you sending me an empty message? :/"), 200)
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return response
    if chatbot is None:
        chatbot = bot()
    reply = chatbot.reply(user=str(session.get('uid', 1)), msg=msg)
    if str(reply) == "ERR: No Reply Matched":
        reply = "Please refresh me."
    response = make_response(jsonify(reply=str(reply)), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    print(reply)
    return response


@application.route('/api/predict/company_monthly_returns/<string:compsymb>', methods=['GET'])
def predict_company_monthly_returns(compsymb):
    p = predictor()
    res = p.getMonthlyReturns(compsymb)
    print(res)
    if res < 0.85:
        data = "Company had a bad performance in the past month. You would have lost " + str(
            round(((1 - res) * 100), 2)) + "% of your money if you had invested."
    elif res > 1.15:
        data = "Company has done really well in the last month. It would be wise to invest in this stock now."
    else:
        data = "Company has moderate performance."
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/api/predict/company_analysis/<string:compsymb>', methods=['POST'])
def company_analysis_view(compsymb):
    try:
        holding = bool(request.form['holding'])
        res = company_analysis(compsymb, holding=holding)
    except:
        res = company_analysis(compsymb)
    response = make_response(jsonify(data=res), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


def company_analysis(compsymb, holding=None, name=None):
    p = predictor()
    res = p.getAnalysis(compsymb, holding)
    if name == None:
        return {"COMP": compsymb,
                "result": res}
    else:
        return {"COMP": compsymb,
                "result": res,
                "name": name}


@application.route('/api/get_all_company_analysis', methods=['POST'])
def get_all_investments():
    dba = dbAccessor()
    stocks = dba.getInvestments(session.get('uid', 1))
    print(stocks)
    data = []
    for stock in stocks:
        data.append(company_analysis(stock[1], holding=True, name=stock[5]))
    print data
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/api/get_portfolio_trends', methods=['POST'])
def get_portfolio_trends():
    p = portfolioPredictor()
    data = p.getPortfolioAnalysis(session.get('uid', 1))
    print(data)
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/api/get_top_performers/<string:categ>', methods=['POST'])
def get_top_performers(categ):
    p = portfolioPredictor()
    data = p.getTopPerformers(category=str(categ))
    print(data)
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/api/get_offers', methods=['POST'])
def get_offers():
    p = patternAnalyser(session.get('uid', 1))
    amount_data = p.getOfferList('amount')
    frequency_data = p.getOfferList('frequency')
    location_data = p.getOfferList('location')
    res = []
    i = amount_data[0]
    data = {"title": i[1],
            "desc": i[5],
            "categ": i[2],
            "exp_date": i[3],
            "discount": i[4],
            "location": i[6]
            }
    res.append(data)

    i = frequency_data[0]
    data = {"title": i[1],
            "desc": i[5],
            "categ": i[2],
            "exp_date": i[3],
            "discount": i[4],
            "location": i[6]
            }
    res.append(data)

    i = location_data[0]
    data = {"title": i[1],
            "desc": i[5],
            "categ": i[2],
            "exp_date": i[3],
            "discount": i[4],
            "location": i[6]
            }
    res.append(data)

    print(location_data)
    print(amount_data)
    print(frequency_data)
    response = make_response(jsonify(data=res), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/dashboard', methods=['POST'])
def dashboard():
    total = 0
    p = dbAccessor()
    res = p.getInvestments(session.get('uid', 1))
    stock = []
    print(res)
    for i in res:
        total += i[2]
        stocks = {
            "name": i[5],
            "num": i[2]
        }
        stock.append(stocks)

    data = {
        "total": total,
        "stocks": stock
    }
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response


@application.route('/transactions', methods=['POST'])
def trans():
    total = 0
    p = dbAccessor()
    res = p.getTransactions(session.get('uid', 1))
    stock = []
    print(res)
    for i in res:
        total += i[2]
        stocks = {
            "name": i[5],
            "num": i[2]
        }
        stock.append(stocks)

    data = {
        "total": total,
        "stocks": stock
    }
    response = make_response(jsonify(data=data), 200)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response
