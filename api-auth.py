#!/usr/bin/python3

from flask import Flask, request, jsonify

app = Flask(__name__)

'''
ENDPOINT='https://tpml-db.documents.azure.com:443/auth'
KEY1='SSnGP49WKUaQDMNLaazKgdCkfsAgbUBbwAZvdGZ1EBVUJ6B8uZ2OZmvZ1OtciROcuOAzezERfgzuHWZ460zQ9w=='
CADEIA1='AccountEndpoint=https://tpml-db.documents.azure.com:443/;AccountKey=SSnGP49WKUaQDMNLaazKgdCkfsAgbUBbwAZvdGZ1EBVUJ6B8uZ2OZmvZ1OtciROcuOAzezERfgzuHWZ460zQ9w==;'

client = CosmosClient(endpoint, key)
container='cont1'
'''

import mysql.connector

def connection():
    conn = mysql.connector.connect(host="34.67.4.127",
                           user = "root",
                           passwd = "123456",
                           db = "auths")
    c = conn.cursor()

    return c, conn

def getNomesDb():
    query='SELECT * FROM `auths`.`nomes_auth`'
    try:
        c, conn = connection()
        data = c.execute(query)
        data = c.fetchall()

        c.close()
        conn.close()
        return data
       
    except Exception as e:
        return(str(e))

    return 0


def postNomesDb(nomes):
    query=''
    for n in nomes:
        query=query+' INSERT INTO `auths`.`nomes_auth` (`nome`) VALUES ('+n+');'
    try:
        c, conn = connection()
        res = c.execute(query)
        conn.commit()
        c.close()
        conn.close()
        return res
    except Exception as e:
        return(str(e))

@app.route("/api/autorizados",methods=["GET"])
def autorizados():
    auths=getNomesDb()
    response = {"autorizados": auths}
    return jsonify(response)

@app.route("/api/novo_autorizado",methods=["POST"])
def novo_autorizado():
    req = request.get_json()   
    for i in req.get("nomes"):
        auths = req.get("nomes")    

    if auths != None and len(auths) > 0:
        response={"resultado": "Nomes insuficientes."}
    else:
        res = postNomesDb(auths)
        response = {"resultado:": res}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False)