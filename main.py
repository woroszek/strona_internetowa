from flask import Flask, render_template, request, redirect

import func
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
    try:
        manager.purchase(item, quantity, cost)
    except ValueError:
        manager.komunikat = 'Uzupełnij wszystkie pola formularzu.'
    return redirect('/')


@app.route("/sell", methods=["POST"])
def sell_view():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    cost = request.form.get("cost")
    try:
        manager.sell(item, quantity, cost)
    except ValueError:
        manager.komunikat = 'Uzupełnij wszystkie pola formularzu.'
    return redirect('/')


@app.route("/balance", methods=["POST"])
def balance():
    add = request.form.get("add")
    try:
        manager.balancee(add)
    except ValueError:
        manager.komunikat = 'Podaj wartość do dodania lub odjęcia.'
    return redirect('/')


@app.route('/history.html')
def history():
    history_a = ''
    komunikat = manager.komunikat
    return render_template("history.html", history_a=history_a, komunikat=komunikat)


@app.route('/history', methods=["POST"])
def history_view():
    od = request.form.get("Od")
    do = request.form.get("Do")
    komunikat = manager.komunikat
    if len(manager.history) < 1:
        komunikat = 'Brak zapisanej historii.'
    try:
        history_a = func.history_number(od, do)
    except ValueError:
        komunikat = "Podano nieprawidlowe dane. Program wyświetli całą historię."
        history_a = func.history_number(1, len(manager.history))

    return render_template("history.html", history_a=history_a, komunikat=komunikat)


if __name__ == "__main__":
    app.run(debug=True)
