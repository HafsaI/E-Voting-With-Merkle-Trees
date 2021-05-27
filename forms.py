from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, validators, IntegerField, RadioField, PasswordField
import csv
import hashlib
from wtforms.widgets.core import Option
from registeration import *
from vote_cast import *
from audit_trail import *
from count_votes import *

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"


def extract_voter_id():
    with open("Files\Data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        reg_id_lst = []
        for row in csv_reader:
            if len(row) > 0:
                reg_id_lst.append(row[3])
        print(reg_id_lst)
    return reg_id_lst


class Register(Form):
    name = TextField("Name:", validators=[validators.required()])
    id = IntegerField("ID:")
    batch_year = IntegerField(
        "Batch Year:",
        validators=[
            validators.required(),
            validators.NumberRange(
                min=2019, max=2024, message="You are not eligible to cast a vote."
            ),
        ],
    )

    def validate_id(form, field):
        if len(str(field.data)) != 4:
            raise validators.ValidationError("HU ID must be of 5 digits.")

    @app.route("/", methods=["GET", "POST"])
    def main1():
        form2 = Register(request.form)
        return render_template("main.html", form=form2)

    @app.route("/reg", methods=["GET", "POST"])
    def hello():
        form = Register(request.form)

        # print(form.errors)
        if request.method == "POST":
            name = request.form["name"]
            hu_id = request.form["hu_id"]
            batch_year = request.form["batch_year"]

            v_Id = hashlib.shake_256(hu_id.encode("utf-8")).hexdigest(5)

            reg_data = [name, str(hu_id), batch_year, v_Id]
            lst = extract_voter_id()

            if form.validate():
                with open("Files\Data.csv", "a") as fp:
                    if v_Id not in lst:
                        storeData(reg_data)
                        wr = csv.writer(fp, dialect="excel")
                        wr.writerow(reg_data)
                        flash(
                            "Thanks for registring "
                            + name
                            + "! Your voter id is: "
                            + f"{v_Id}",
                            "success",
                        )
                    else:
                        flash(
                            "You are already registered, kindly Proceed to Login.",
                            "error",
                        )
                # return redirect(url_for("cast_vote"))

            elif not form.validate():
                lst = form.errors.items()
                for i in lst:
                    # print(i)
                    str1 = "".join(i[1])
                    if str1 in (
                        "HU ID must be of 5 digits.",
                        "You are not eligible to cast a vote.",
                    ):
                        flash(str1, "error")

        return render_template("hello.html", form=form)


#################################CAST VOTE#####################################################
################################################################################################


class Voting(Form):
    name = TextField("Name:", validators=[validators.required()])
    voter_id = TextField("Voter ID:", validators=[validators.required()])
    option = RadioField(
        "option", choices=[("Aiman"), ("Niha"), ("Hafsa")], validate_choice=True
    )

    @app.route("/cast_vote", methods=["GET", "POST"])
    def cast_vote():
        form2 = Voting(request.form)

        if request.method == "POST":
            name = request.form["name"]
            voter_id = request.form["voter_id"]
            option = request.form["option"]
            cand_val = 100
            if option == "Aiman":
                cand_val = 2
            elif option == "Niha":
                cand_val = 3
            elif option == "Hafsa":
                cand_val = 4

            vote_data = [name, voter_id, option, cand_val]
            voted = run_polls(vote_data)

            if form2.validate():
                if voted:
                    flash("Thank You for your vote " + name + ".", "success")
                    with open("Files\Voting_data.csv", "a") as fp1:
                        wr = csv.writer(fp1, dialect="excel")
                        wr.writerow(vote_data)
                else:
                    flash("You have already voted!", "error")
                # return redirect(url_for("hello"))

            else:
                flash("Invalid attempt! Please Retry.", "error")
            #     lst = form2.errors.items()
            #     for i in lst:
            #         str1 = ''.join(i[1])
            #         if str1 in ('CNIC# must be of 13 digits'):
            #             flash(str1,"error")

        return render_template("cast_vote.html", form=form2)


#################################### Login Form ################################################
#################################################################################################


class Login(Form):
    name = TextField("Name:", validators=[validators.required()])
    voter_id = TextField("Voter ID:", validators=[validators.required()])

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = Login(request.form)

        if request.method == "POST":
            name = request.form["name"]
            voter_id = request.form["voter_id"]

            # vote_data=[name, voter_id]

            lst = extract_voter_id()

            if form.validate():
                if voter_id in lst:
                    flash("Logged In!", "success")
                else:
                    flash(
                        "You are not registered to Vote, Please Register first!",
                        "error",
                    )
                # return redirect(url_for("hello"))

            else:
                flash("Login Failed", "error")

        return render_template("login.html", form=form)


class Auditing(Form):
    password = PasswordField("password:", validators=[validators.required()])
    # option = RadioField("option", choices=[("Aiman"), ("Niha"), ("Hafsa")])
    voter_id = TextField("voter_id: ", validators=[validators.required()])

    def validate_password(form, field):
        if field.data != "pw12345":
            print("hello")
            raise validators.ValidationError("Incorrect Password! Try again")

    @app.route("/audit", methods=["GET", "POST"])
    def audit():
        form = Auditing(request.form)

        if request.method == "POST":
            voter = request.form["voter_id"]
            # password= request.form["password"]

            audit_data = [voter]
            valid = run_audit(voter)

            if form.validate():
                print("validate")
                with open("Files\\audit_data.csv", "a") as fp1:
                    wr = csv.writer(fp1, dialect="excel")
                    wr.writerow(audit_data)
                if valid:
                    flash("Voter " + voter + " exists.", "success")

                else:
                    flash("Voter " + voter + " doesn't exist!", "error")

            else:
                flash("Invalid Password or Invalid Attempt! Please try again.", "error")

        return render_template("audit.html", form=form)


def winner():
    dict_count = run_count()
    count_lst = [dict_count["2"], dict_count["3"], dict_count["4"]]
    key_list = [2, 3, 4]
    won_num = 0
    print(count_lst)
    for i in range(len(count_lst)):
        if won_num < count_lst[i]:
            won_num = count_lst[i]
            won_key = key_list[i]
    print(won_key)
    print(won_num)
    return (won_key, won_num)


@app.route("/result")
def vote_count():
    win = winner()
    if win[0] == 2:
        win_name = "Aiman Haq"
    elif win[0] == 3:
        win_name = "Niha Faisal"
    elif win[0] == 4:
        win_name = "Hafsa Irfan"
    # print(win_name, win[1])
    return render_template("result.html", set=(win_name, win[1]))


if __name__ == "__main__":
    app.run()