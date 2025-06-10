import tkinter as tk
from tkinter import messagebox
import random

# إعدادات حجم اللعبة وعدد الألغام
WIDTH, HEIGHT, MINES = 10, 10, 15
CELL_SIZE = 2

# مصفوفات لتخزين حالة كل خلية
cells = []       # أزرار الخلايا
revealed = []    # الخلايا اللي تم كشفها
flagged = []     # الخلايا اللي عليها علم
is_mine = []     # الخلايا اللي فيها لغم

# متغيرات الحالة
first_click = True     # أول نقرة؟ لو نعم: لازم تكون آمنة
flags_left = MINES     # عدد الأعلام المتبقية
game_over = False      # هل اللعبة خلصت؟


# دي الدالة اللي بتجهز كل حاجة من الأول
def setup_board():
    global cells, revealed, flagged, is_mine, flags_left, first_click, game_over

    flags_left = MINES
    first_click = True
    game_over = False
    flag_label.config(text=f"🚩 Flags Left: {flags_left}")

    # نمسح القديم
    for widget in game_frame.winfo_children():
        widget.destroy()

    cells.clear()
    revealed.clear()
    flagged.clear()
    is_mine.clear()

    # نبدأ نرسم الخلايا
    for y in range(HEIGHT):
        row_cells = []
        row_revealed = []
        row_flagged = []
        row_mines = []
        for x in range(WIDTH):
            btn = tk.Button(game_frame, width=CELL_SIZE, height=1, bg="#ddd")
            btn.grid(row=y, column=x)
            btn.bind("<Button-1>", lambda e, i=x, j=y: reveal_cell(i, j))  # كليك شمال
            btn.bind("<Button-3>", lambda e, i=x, j=y: toggle_flag(i, j))  # كليك يمين
            row_cells.append(btn)
            row_revealed.append(False)
            row_flagged.append(False)
            row_mines.append(False)
        cells.append(row_cells)
        revealed.append(row_revealed)
        flagged.append(row_flagged)
        is_mine.append(row_mines)

# توزيع الألغام بشكل عشوائي (لكن بعيد عن أول ضغطة)
def place_mines(safe_x, safe_y):
    count = 0
    while count < MINES:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if not is_mine[y][x] and (x != safe_x or y != safe_y):
            is_mine[y][x] = True
            count += 1

# نحسب عدد الألغام حوالي خلية معينة
def count_adjacent_mines(x, y):
    count = 0
    for j in range(max(0, y - 1), min(HEIGHT, y + 2)):
        for i in range(max(0, x - 1), min(WIDTH, x + 2)):
            if is_mine[j][i]:
                count += 1
    return count

# دي الدالة اللي بتشتغل لما ندوس كليك شمال
def reveal_cell(x, y):
    global first_click, game_over

    if game_over:
        return

    # لو الخلية متعلم عليها أو مفتوحة، منعملش حاجة
    if flagged[y][x] or revealed[y][x]:
        return

    if first_click:
        place_mines(x, y)
        first_click = False

    revealed[y][x] = True

    if is_mine[y][x]:
        cells[y][x].config(text="💣", bg="red")
        show_mines()
        game_over = True
        messagebox.showwarning("Game Over", "💥 خبطت في لغم! حاول تاني.")
        restart_game()
    else:
        count = count_adjacent_mines(x, y)
        cells[y][x].config(text=str(count) if count > 0 else "", bg="white", relief="sunken")

        # لو مفيش ألغام حوالين الخلية، نكشف اللي جنبها كمان
        if count == 0:
            for j in range(max(0, y - 1), min(HEIGHT, y + 2)):
                for i in range(max(0, x - 1), min(WIDTH, x + 2)):
                    if not revealed[j][i]:
                        reveal_cell(i, j)

    if check_win():
        messagebox.showinfo("Bravo!", "🎉 كسبت اللعبة! كل الألغام اتجنبت.")
        restart_game()

# دي بتشتغل مع كليك يمين عشان نضيف أو نشيل علم
def toggle_flag(x, y):
    global flags_left

    if revealed[y][x] or game_over:
        return

    if not flagged[y][x] and flags_left > 0:
        cells[y][x].config(text="🚩", fg="blue")
        flagged[y][x] = True
        flags_left -= 1
    elif flagged[y][x]:
        cells[y][x].config(text="")
        flagged[y][x] = False
        flags_left += 1

    flag_label.config(text=f"🚩 Flags Left: {flags_left}")

# لما نخسر نعرض كل الألغام
def show_mines():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if is_mine[y][x]:
                cells[y][x].config(text="💣", bg="red")

# نراجع هل اللاعب كسب ولا لأ
def check_win():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if not is_mine[y][x] and not revealed[y][x]:
                return False
    return True

# نعيد تشغيل اللعبة من الأول
def restart_game():
    setup_board()

# رسالة ترحيب أول ما اللعبة تبدأ
def start_game():
    messagebox.showinfo(
        "أهلا بيك!",
        "🎯 هدفك إنك تكشف كل الخلايا اللي مفيهاش ألغام\n🖱 كليك شمال: تكشف خلية\n🚩 كليك يمين: تحط علم\nبالتوفيق!"
    )
    setup_board()

# نبدأ الواجهة
root = tk.Tk()
root.title("Minesweeper 💣")

top_frame = tk.Frame(root)
top_frame.pack(pady=5)

flag_label = tk.Label(top_frame, text="", font=("Arial", 12))
flag_label.pack(side="left", padx=10)

restart_button = tk.Button(top_frame, text="🔁 Restart", command=restart_game)
restart_button.pack(side="right", padx=10)

game_frame = tk.Frame(root)
game_frame.pack()

start_game()

root.mainloop()
