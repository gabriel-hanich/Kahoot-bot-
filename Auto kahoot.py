import json
import requests
import time
import webbrowser
import os
import requests
import sys
from tkinter import *

root = Tk()
root.geometry("550x500")
root.title("Kahoot Bot")
# Creating a label widget
mywelcomelabel = Label(root, text="Welcome to the Kahoot Bot", font=("Arial", 30), bg='#7a2aa8', fg='white')
def show_user_manual ():
    manual_box = Toplevel()
    manual_box.geometry("645x500")
    manual_box.title("User manual")
    manual_text1 = Label(manual_box, text="This bot scans the kahoot page, gets the correct answers and then allows you the ability to use them in game, \nBelow are some controls in the order they need to be used:", font=("Arial",10), bg='#3fadd9')
    manual_text2 = Label(manual_box, text="1. Left arrow key\nThis needs to be pressed when you see the area to fill in the game code, this initializes the code \nand types the game code",font=("Arial",10), bg='#59b1d4')
    manual_text3 = Label(manual_box, text="2.Right arrow key\nThis will type the name", font=("Arial",10), bg='#7cbed9')
    manual_text4 = Label(manual_box, text="After this press a every time the kahoot allows you to answer a question press a", font=("Arial",10), bg='#94c3d6')
    manual_text5 = Label(manual_box, text="Up arrow key to skip forward a question and down arrow to go back", font=("Arial",10), bg='#b0c9d4')
    manual_text6 = Label(manual_box, text="Press q to check what question the bot is up to", font=("Arial",10), bg='#d8e5eb')
    manual_text1.grid(row=1, column=1)
    manual_text2.grid(row=2, column=1)
    manual_text3.grid(row=3, column=1)
    manual_text4.grid(row=4, column=1)
    manual_text5.grid(row=5, column=1)
    manual_text6.grid(row=6, column=1)



def submit ():
    global url1
    global game_code
    global user_name
    url1 = url_entry.get()
    game_code = game_entry.get()
    if terry_true.get() == 1:
        user_name = 'Terry'
    else:
        user_name = name_entry.get()
    root.destroy()

see_user_manual = Button(root, text="Do you want to see the user manual", font=("arial", 15), bg="#1de02a", command=show_user_manual)
spacer = Label(root,text='')
spacer2 = Label(root,text='')
url_label = Label(root, text="Please copy paste URL below:", font=("Arial",15), bg='#7a2aa8')
url_entry = Entry(root, width=50, font=("Arial",15), borderwidth=7)

gamecode_label = Label(root, text="Please type game code below:", font=("Arial",15), bg='#7a2aa8')
game_entry = Entry(root, width=50, font=("Arial",15), borderwidth=7)

name_label = Label(root, text="Please type your name below:", font=("Arial",15), bg='#7a2aa8')
name_entry = Entry(root, width=50, font=("Arial",15), borderwidth=7)
terry_true = IntVar()
terry_box = Checkbutton(root, text="Terry", variable=terry_true)

submit_btn = Button(root, text="Submit", font=("arial", 15), bg="#1de02a", command=submit)

mywelcomelabel.grid(row=1, column=1)
see_user_manual.grid(row=2, column=1)
url_label.grid(row=3, column=1)
url_entry.grid(row=4, column=1)
spacer.grid(row=5, column=1)
gamecode_label.grid(row=6, column=1)
game_entry.grid(row=7, column=1)
spacer2.grid(row=8, column=1)
name_label.grid(row=9, column=1)
name_entry.grid(row=10, column=1)
terry_box.grid(row=11, column=1)
submit_btn.grid(row=12, column=1)
root.mainloop()



print('From now on the bot will be controlled via this terminal')


website = requests.get(url1)

if website.status_code == 200:
    print("Website server found:")
if website.status_code == 404:
    print("ERROR 404\nPAGE NOT FOUND")
    sys.exit()
code = game_code
name = user_name


print("Please wait while we contact the kahoot servers")
type_list = []
kahoot_id = url1.split('/')[-1]
answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.format(kahoot_id=kahoot_id)
data = requests.get(answers_url).json()

# Declare variables

this_type = ''
first_answer = ''
second_answer = ''
third_answer = ''
fourth_answer = ''
answers_list = []
got_answer = False
choice_list = []
question_type_list = []
questions = data['kahoot']['questions']
questions_num = 0
rotations = 0
delay = 1

# Get question type
for i in data['kahoot']['questions']:
    for type in i['type']:
        type_list.append(type)
        this_type = this_type + type_list[rotations]
        rotations += 1
        if this_type == 'quiz':
            questions_num += 1
            this_type = ''
            question_type_list.append("quiz")
        if this_type.lower() == "true_false":
            questions_num += 1
            this_type = ''
            question_type_list.append("true_false")
        if this_type.lower() == "jumble":
            questions_num += 1
            this_type = ''
            question_type_list.append("jumble")
        if this_type.lower() == 'survey':
            this_type = ''
            questions_num += 1
            question_type_list.append("survey")
        if this_type.lower() == 'open_ended':
            this_type = ''
            questions_num += 1
            question_type_list.append("open_ended")
        if this_type.lower() == 'content':
            this_type = ''
            questions_num += 1
            question_type_list.append("content")

rotations = 0
print("got question types")
# Create txt file with the html data
x = open("Code", 'w')
a = json.dumps(data['kahoot']['questions'], indent=4)
x.write(a)
x.close()

def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append(line_number)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


# Search file for required data
start_pos = search_string_in_file("Code", '"choices": [')
end_pos = search_string_in_file("Code", "],")
this_question_num = 0
print("searched")

f=txt = open('Code')
lines = txt.readlines()
txt.close()
rotations = 0
this_question_num = 0
# Find which button the correct answer is (red, blue, yellow, green)

while this_question_num < questions_num:
    num_of_answers_raw = round((end_pos[this_question_num] - start_pos[this_question_num]))
    num_of_answers = num_of_answers_raw / 4.25
    if num_of_answers == 4 and question_type_list[this_question_num] == 'quiz' or 'true_false':
        first_answer = lines[start_pos[this_question_num] + 2]
        second_answer = lines[start_pos[this_question_num] + 6]
        third_answer = lines[start_pos[this_question_num] + 10]
        fourth_answer = lines[start_pos[this_question_num] + 14]
    if num_of_answers == 3 and question_type_list[this_question_num] == 'quiz' or 'true_false':
        first_answer = lines[start_pos[this_question_num] + 2]
        second_answer = lines[start_pos[this_question_num] + 6]
        third_answer = lines[start_pos[this_question_num] + 10]
    if num_of_answers == 2 and question_type_list[this_question_num] == 'quiz' or 'true_false':
        first_answer = lines[start_pos[this_question_num] + 2]
        second_answer = lines[start_pos[this_question_num] + 6]

    if len(first_answer) == 32 and not got_answer:
        got_answer = True
        answers_list.append('red')
    if len(second_answer) == 32 and not got_answer:
        got_answer = True
        answers_list.append('blue')
    if len(third_answer) == 32 and not got_answer:
        got_answer = True
        answers_list.append('yellow')
    if len(fourth_answer) == 32 and not got_answer:
        got_answer = True
        answers_list.append('green')

    got_answer = False
    this_question_num += 1
print("got answers")

rotations = 0
webbrowser.open('kahoot.it')

from pynput.keyboard import Listener
from pynput.mouse import Button, Controller
import time



mouse = Controller()

os.remove("Code")
def initialize():
    global question_number
    question_number = 0


def go_back():
    global question_number
    question_number -= 1


def go_forward():
    global question_number
    question_number += 1


def red():
    mouse.position = (200, 300)
    mouse.press(Button.left)
    time.sleep(0.001)
    mouse.release(Button.left)


def green():
    mouse.position = (1005, 562)
    mouse.press(Button.left)
    time.sleep(0.001)
    mouse.release(Button.left)


def yellow():
    mouse.position = (350, 550)
    mouse.press(Button.left)
    time.sleep(0.001)
    mouse.release(Button.left)


def blue():
    mouse.position = (1000, 300)
    mouse.press(Button.left)
    time.sleep(0.001)
    mouse.release(Button.left)


def Type_game_code():
    from pynput.keyboard import Controller
    keyboard_controller = Controller()
    keyboard_controller.type(str(code))


def type_game_name():
    from pynput.keyboard import Controller
    keyboard_controller = Controller()
    keyboard_controller.type(str(name))


def Questions():
    global question_number

    if answers_list[question_number] == 'red':
        red()
    if answers_list[question_number] == 'blue':
        blue()
    if answers_list[question_number] == 'yellow':
        yellow()
    if answers_list[question_number] == 'green':
        green()
    question_number += 1


print(answers_list)


def read_board(key):
    global question_number
    letter = str(key)
    letter = letter.replace("'", "")
    if letter == "Key.left":
        initialize()
        Type_game_code()
    if letter == "Key.right":
        type_game_name()
    if letter == "a":
        Questions()
        print(question_number)
    if letter == 'Key.down':
        go_back()
        print(question_number)
    if letter == 'Key.up':
        go_forward()
        print(question_number)
    if letter == 'q':
        print(question_number)


with Listener(on_press=read_board) as l:
    l.join()