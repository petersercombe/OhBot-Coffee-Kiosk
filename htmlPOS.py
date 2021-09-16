from flask import *
from dbUtils import *
import datetime
from menu import *

app = Flask(__name__)

@app.route("/", methods=['GET', "POST"])
@app.route("/home", methods=['GET', "POST"])
def home():
    orderData = getOrders()
    # Swap \r\n for html tag <br>
    for i, entry in enumerate(orderData):
        entry = list(entry)
        entry[1] = entry[1].replace('\r\n', '<br>')
        entry[4] = entry[4][10:19]
        entry = tuple(entry)
        orderData[i] = entry
    return render_template("home.html", orderData=orderData)


@app.route("/add", methods=["GET", "POST"])
def add():
    # Method check
    if request.method == "GET":
        return render_template("add.html", drinks=drinks, milk=milk, shots=shots)
    else:
        # Get current time
        currentDT = datetime.datetime.now()
        # Get data from form
        data = ("Name: " + request.form["name"] +
                "\r\nOrder: " + request.form["order1"] + " " + request.form["shots1"] + " " + request.form["milk1"] +
                "\r\nOrder: " + request.form["order2"] + " " + request.form["shots2"] + " " + request.form["milk2"] +
                "\r\nOrder: " + request.form["order3"] + " " + request.form["shots3"] + " " + request.form["milk3"] +
                "\r\nOrder: " + request.form["order4"] + " " + request.form["shots4"] + " " + request.form["milk4"] +
                "\r\nOrder: " + request.form["order5"] + " " + request.form["shots5"] + " " + request.form["milk5"] +
                "\r\nSpecial Requests: " + request.form["special"],
                request.form["cost"],
                request.form["paid"],
                currentDT)
        # Insert data into DB
        runQuery(insertOrder, data)
        return redirect(url_for('home'))


@app.route("/edit/<orderID>", methods=["GET", "POST"])
def edit(orderID):
    if request.method == "GET":
        order = getQuery(getOrder, (orderID,))
        return render_template("edit.html", order=order)
    else:
        data = (request.form["orderData"],
                request.form["cost"],
                request.form["paid"],
                orderID)
        runQuery(updateOrder, data)
        return redirect(url_for('home'))


@app.route("/paid", methods=["GET"])
def paid():
    orderID = request.args.get("orderID")
    runQuery(updatePaid, (orderID,))
    return redirect(url_for('home'))


@app.route("/processdelivery/<orderID>", methods=["GET", "POST"])
def processdelivery(orderID):
    if request.method == "GET":
        order = getQuery(getOrder, (orderID,))
        for i, entry in enumerate(order):
            entry = list(entry)
            entry[1] = entry[1].replace('\r\n', '<br>')
            entry[4] = entry[4][10:19]
            entry = tuple(entry)
            order[i] = entry
        return render_template("confirmation.html", order=order)
    else:
        # Get current time
        currentDT = datetime.datetime.now()
        runQuery(processDelivery, (currentDT, orderID))
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

