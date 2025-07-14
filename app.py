from flask import Flask, render_template, request
import joblib
from groq import Groq

import os
#https://console.groq.com/keys
#os.environ['GROQ_API_KEY'] = "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"  # replace with your actual API key
# for cloud ....
def llama_query():
    client = client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Explain why fast inference is critical for reasoning models"
            }
        ]
    )
    return render_template("llama_reply.html", r=completion.choices[0].message.content)

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    # db
    return(render_template("main.html"))

@app.route("/llama",methods=["GET","POST"])
def llama():
    return(render_template("llama.html"))

@app.route("/llama_reply",methods=["GET","POST"])
def llama_reply():
    q = request.form.get("llama_query")
    return(render_template("llama_reply.html"))

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
