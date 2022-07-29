from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config['SECRET_KEY'] = 'GIZLI ANAHTAR KELIME'

def auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = kwargs['token']
        except:
            token = request.args.get('token') or \
                request.form.get('token')

        if not token:
            return jsonify({'message': 'Token Gerekli!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token Geçersiz!'}), 403

        return f(*args,**kwargs)
    
    return wrapper



@app.route('/home', methods=['GET'])
@auth
def home():
    return  "Token geçerli"
 


@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    kullanici_adi = request_data['username']
    kullanici_sifre = request_data['password']
    token = ''
    if kullanici_adi and kullanici_sifre == '1234567':
        token = jwt.encode({
            'user': kullanici_adi,
            'password': kullanici_sifre,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        }, app.config['SECRET_KEY'])
    else:
        token = 'Kullanıcı adı veya şifre geçersiz'

    return jsonify({'token': token.decode('UTF-8')})

if __name__ == '__main__':
    app.run(port=2121, debug=True)
