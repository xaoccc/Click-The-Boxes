from flask import Flask, render_template, redirect, request
import random, datetime
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


def mark_red(boxes, row, col, box):
    global score
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return

    if boxes[row][col] != box:
        return

    if boxes[row][col] == box:
        if box == 'yellow':
            score += 1
        elif box == 'orange':
            score += 3
        elif box == 'green':
            score += 5
        elif box == 'purple':
            score += 10
        boxes[row][col] = "red"

    mark_red(boxes, row - 1, col, box)
    mark_red(boxes, row, col - 1, box)
    mark_red(boxes, row + 1, col, box)
    mark_red(boxes, row, col + 1, box)

    return redirect("/")


def unmark_red(boxes, row, col, box):
    global score
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return

    if boxes[row][col] != "red":
        return

    if boxes[row][col] == "red":
        r = random.randint(0, 12)
        if r < 6:
            boxes[row][col] = "yellow"
        elif r < 9:
            boxes[row][col] = "orange"
        elif r < 11:
            boxes[row][col] = "green"
        else:
            boxes[row][col] = "purple"

    unmark_red(boxes, row - 1, col, box)
    unmark_red(boxes, row, col - 1, box)
    unmark_red(boxes, row + 1, col, box)
    unmark_red(boxes, row, col + 1, box)

    return boxes


def click(position):
    global score
    row = position[0]
    col = position[1]
    box = boxes[row][col]
    mark_red(boxes, row, col, box)
    unmark_red(boxes, row, col, box)

    return redirect("/")

boxes = generate_random_boxes()
score = 0
all_scores = [0]
game_over = False
start = datetime.datetime.now()


def reset():
    global boxes
    boxes = generate_random_boxes()
    global score
    score = 0
    global game_over
    game_over = False
    return redirect('/')


@app.route('/Click', methods=['GET', 'POST'])
def click_on_box():
    position = request.values.get('position')[1:-1]
    position = [int(i) for i in position.split(',')]
    global start
    global all_scores
    end = datetime.datetime.now()
    time_diff = end - start
    time_diff = time_diff.seconds
    if time_diff > 10:
        all_scores.append(score)
        start = datetime.datetime.now()
        return reset()

    return click(position)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", rows=rows, boxes=boxes, cols=cols, score=score, game_over=game_over, best_score=max(all_scores))


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



