from flask import Flask, render_template, request
import joblib
from groq import Groq

import os

app = Flask(__name__)

# create GROQ_API_KEY via https://console.groq.com/keys
api_key = os.getenv("GROQ_API_KEY")
# Set it for Groq client or environment if needed
os.environ["GROQ_API_KEY"] = api_key
# for cloud ....


@app.route("/llama",methods=["GET","POST"])
def llama():
    return(render_template("llama.html"))

@app.route("/llama_reply", methods=["GET", "POST"])
def llama_reply():
    q = request.form.get("q")
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": q}
        ]
    )
    # Extract reply
    reply = completion.choices[0].message.content
    return render_template("llama_reply.html", q=q, r=reply)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    # db
    return(render_template("main.html", myName=q))  # pass myName to main.html

@app.route("/dbs",methods=["GET","POST"])
def dbs():
    return(render_template("dbs.html"))

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q"))

    # load model
    model = joblib.load("dbs.jl")

    # make prediction
    pred = model.predict([[q]])

    return(render_template("prediction.html",r=pred))

if __name__ == "__main__":
    app.run()
