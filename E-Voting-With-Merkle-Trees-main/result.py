# from csv import DictWriter
# from flask import Flask, render_template, flash, request
# from wtforms import Form
# from flask import Markup
# from flask import Flask
# from flask import render_template
# from count_votes import *
# from forms import *
# #app = Flask(__name__)
 
# def winner():
#     dict_count = run_count()
#     count_lst =[dict_count['2'],dict_count['3'],dict_count['4']]
#     key_list = [2,3,4]
#     won_num = 0
#     print(count_lst)
#     for i in range(len(count_lst)):
#         if won_num < count_lst[i]:
#             won_num = count_lst[i]
#             won_key = key_list[i]
#     print(won_key)
#     print(won_num)
#     return (won_key, won_num)


# @app.route("/result")
# def vote_count():
#     win = winner()
#     if win[0] == 2:
#         win_name = 'Aiman Haq'
#     elif win[0] == 3:
#         win_name = 'Niha Faisal'
#     elif win[0] == 4:
#         win_name = 'Hafsa Irfan'
#     print(win_name, win[1])
#     return render_template('result.html', set= (win_name, win[1]))


# # if __name__ == "__main__":
# #     app.run()