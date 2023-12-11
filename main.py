from flask import Flask, render_template, request, redirect
from func import manager

app = Flask(__name__)


@app.route('/')
def index():
    balance = manager.balance
    komunikat = manager.komunikat
    history = manager.warehouse
    manager.history_write()
    return render_template('page.html', balance=balance, komunikat=komunikat, history=history)


@app.route("/purchase", methods=["POST"])
def purchase_view():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    cost = request.form.get("cost")
    manager.purchase(item, quantity, cost)
    return redirect('/')


@app.route("/sell", methods=["POST"])
def sell_view():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    cost = request.form.get("cost")
    manager.sell(item, quantity, cost)
    return redirect('/')


@app.route("/balance", methods=["POST"])
def balance():
    add = request.form.get("add")
    manager.balancee(add)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
