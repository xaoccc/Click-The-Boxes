from flask import Flask, render_template, redirect, request, jsonify
import random
app = Flask(__name__)
rows = 7
cols = 18


def generate_random_boxes():
    boxes = [[] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            r = random.randint(0, 12)
            if r < 6:
                boxes[row].append("yellow")
            elif r < 9:
                boxes[row].append("orange")
            elif r < 11:
                boxes[row].append("green")
            else:
                boxes[row].append("purple")
    return boxes


boxes = generate_random_boxes()
score = 0
game_over = False


def click(position, start_row, step):
    col = position * (cols - 1) // 100
    row = start_row
    while 0 <= row < rows:
        box = boxes[row][col]
        global score
        if box == 'yellow':
            score += 1
        elif box == 'orange':
            score += 3
        elif box == 'green':
            score += 5
        elif box == 'purple':
            score += 10
        break

        row = row + step

    return redirect("/")


@app.route('/Click')
def click_on_box():
    position = int(request.args['position'])
    return click(position, 0, 1)

@app.route('/')
def index():
    return render_template("index.html", rows=rows, boxes=boxes, cols=cols, score=score, game_over=game_over, click=click)


@app.route('/Reset')
def reset():
    global boxes
    boxes = generate_random_boxes()
    global score
    score = 0
    global game_over
    game_over = False
    return redirect('/')


if __name__ == "__main__":
    app.run()



