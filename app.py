# coding=UTF-8
# from Paillier.phe_Bob import Phe_Bob
# from Paillier.phe_Alice import Phe_Alice
# from Paillier.paillier import Paillier
from phe import paillier
# import phe.keygen as keygen
# import phe.crypto as crypto
from flask import Flask,render_template,request
import random
import flask_cors
app = Flask(__name__)
cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})

pk, sk = paillier.generate_paillier_keypair(n_length=2048)


# 比较Alice的财富a和Bob的财富b
def compare(a, b):
    # Bob生成两个随机数x和y
    x = random.getrandbits(100)
    y = random.getrandbits(128)

    # Alice公布自己公钥pk
    print("Alice: pk =", pk)

    # Alice计算a的密文并公布
    e_a = pk.encrypt(a)
    print("Alice: E(a) =", e_a)

    # Bob计算b*x+y的密文并公布
    n, _ = pk
    e_bxy = pk.encrypt(b * x + y)
    print("Bob: E(b*x+y) =", e_bxy)

    # Bob计算a*x+y的密文并公布
    e_axy = paillier.secure_addition(
        paillier.crypto.scalar_multiplication(e_a, x, n),
        paillier.crypto.encrypt(pk, y),
        n,
    )
    print("Bob: E(a*x+y) =", e_axy)

    # Alice根据密文反解出b*x+y
    bxy = paillier.crypto.decrypt(pk, sk, e_bxy)

    # Alice根据密文反解出a*x+y
    axy = paillier.crypto.decrypt(pk, sk, e_axy)

    # Alice公布最终的大小结果
    if axy > bxy:
        print("winner: Alice")
    elif bxy > axy:
        print("winner: Bob")
    else:
        print("tie")

@app.route('/submit')
def getResult():
    a = int(request.args.get("Alice"))
    b=int(request.args.get("Bob"))
     # Bob生成两个随机数x和y
    x = random.getrandbits(100)
    y = random.getrandbits(128)
    print(request.args.get("Alice"))
    print(request.args.get("Bob"))
    print(type(a))
    # Alice公布自己公钥pk
    print("Alice: pk =", pk)

    # Alice计算a的密文并公布
    e_a = pk.encrypt(a)
    print("Alice: E(a) =", e_a)

    # Bob计算b*x+y的密文并公布
    e_bxy = pk.encrypt(b * x + y)
    print("Bob: E(b*x+y) =", e_bxy)

    # Bob计算a*x+y的密文并公布
    # e_axy = paillier.crypto.secure_addition(
    #     paillier.crypto.scalar_multiplication(e_a, x, n),
    #     paillier.crypto.encrypt(pk, y),
    #     n,
    # )
    e_axy=e_a*x+y
    print("Bob: E(a*x+y) =", e_axy)

    # Alice根据密文反解出b*x+y
    bxy = sk.decrypt(e_bxy)

    # Alice根据密文反解出a*x+y
    axy = sk.decrypt(e_axy)

    # Alice公布最终的大小结果
    winner=''
    if axy > bxy:
        print("winner: Alice")
        winner="Alice wins!"
    elif bxy > axy:
        print("winner: Bob")
        winner="Bob wins!"
    else:
        print("tie")
        winner="tie"
    results={}
    # results['e_a']=e_a
    # results['e_bxy']=e_bxy
    # results['e_axy']=e_axy
    results['axy']=axy
    results['bxy']=bxy
    results['winner']=winner

    return results

@app.route('/millionaire')
def millionaire():
    return render_template('millionaire.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
