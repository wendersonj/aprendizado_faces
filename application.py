#!/usr/bin/python3

from flask import Flask, request, jsonify

app = Flask(__name__)


import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('pymysql')
import pymysql
#import mysql.connector

def connection():
    return pymysql.connect(host="localhost", user = "root", passwd = "toor", db = "imoveis")
    
def getNomesDb():
    query='SELECT `nome` FROM `auths`.`nomes_auth`'
    try:
        c=connection()
        with c.cursor() as cursor:
            data = cursor.execute(query)
            print("data:", data)
            data = cursor.fetchall()
            c.commit()
            return data
        
    except Exception as e:
        print("ero:", str(e))
        return({"resultado:": 0, 'erro':str(e)})
    finally:
        c.close()



def postNomesDb(nomes):
    try:
        c = connection()
        with c.cursor() as cursor:
            print(nomes)
            #res = c.executemany("INSERT INTO nomes_auth (nome) VALUES (%s)", nomes)
            #nomes=[['abc'],['dce']]
            #for n in nomes:
            cursor.execute("DELETE FROM `auths`.`nomes_auth`")
            c.commit()

            res = cursor.executemany("INSERT INTO `auths`.`nomes_auth` (`nome`) VALUES (%s)", nomes)
            c.commit()
            return 1
    except Exception as e:
        print("ero:", str(e))
        return({"resultado:": 0, 'erro':str(e)})
    finally:
        c.close()

@app.route("/api/autorizados",methods=["GET"])
def autorizados():
    auths=getNomesDb()
    a=[]
    for i in auths: #tratamento da resposta - resultado é uma lista de nomes
        a.append(i[0])
    response = {"autorizados": a}
    return jsonify(response)

@app.route("/api/novo_autorizado",methods=["POST"])
def novo_autorizado():
    try:
        req = request.get_json() #Content-type no HEADER tem que ser application/json
        print("REQUSICAO:", req["nomes"])
        
        nomes=[]
        if req and req!=None:
            '''
            for i in req["nomes"]:
                if type(i) != str:
                    nomes.append(str(i))
                else:
                    nomes.append(i) 
            '''
            nomes=[[x] for x in req["nomes"]]
            print(nomes)
        if nomes == None or len(nomes) == 0:
            response={"resultado": "Nomes insuficientes."}
            return jsonify(response)
        
        else:
            response = postNomesDb(nomes)
            return jsonify({"resultado":response})

        return jsonify({"resultado":"noideia"})

    except Exception as e:
        return(str(e))

@app.route("/")
def hello():
    return jsonify(response="Oi !")

if __name__ == '__main__':
    app.run(debug=False)
