from tkinter import *
import math
from notifypy import Notify

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


notification = Notify(
  default_notification_title="Pomodoro Timer",
  default_notification_icon="tomato.png",
  default_notification_audio="pomodoro_chime.wav"
)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    checkmark_label.config(text="")
    start_button.config(state=NORMAL)
    reset_button.config(state=DISABLED)
    global reps
    reps = 0



# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
        start_button.config(state=DISABLED)
        reset_button.config(state=NORMAL)
        window.focus_force()
        notification.message = "Time for a long break!"
        notification.send()
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
        start_button.config(state=DISABLED)
        reset_button.config(state=NORMAL)
        window.focus_force()
        notification.message = "Time for a short break!"
        notification.send()

    else:
        count_down(work_sec)
        timer_label.config(text="WORK", fg=GREEN)
        start_button.config(state=DISABLED)
        reset_button.config(state=NORMAL)
        window.focus_force()
        notification.message = "Time for work!"
        notification.send()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)  # shows the largest whole number smaller than 'count'
    count_sec = count % 60              # shows the remainder number of seconds after count is divided by 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"     # A E S T H E T I C    // turns the seconds to double digits when < 10


    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"

        checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
timer_label = Label(text="Timer", font=(FONT_NAME, 48), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# use highlightbackground argument on MacOS dark mode to fix gray buttons
start_button = Button(text="Start", highlightthickness=0, highlightbackground=YELLOW, fg="black", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, highlightbackground=YELLOW, fg="black",state=DISABLED, command=reset_timer)
reset_button.grid(column=2, row=2)

checkmark_label = Label(bg=YELLOW, fg=GREEN)
checkmark_label.grid(column=1, row=3)

window.mainloop()
