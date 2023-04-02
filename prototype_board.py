import tkinter as tk

root = tk.Tk()

buttons = []
for x in range(1,9):
    row = []
    for y in range(1,9):
        button = tk.Button(root, width=10, height=5)
        button.grid(row=x, column=y, padx=0.1, pady=0.1)
        if x % 2 == 0 and y % 2 != 0:
            button.config(bg="brown")
        elif x % 2 != 0 and y % 2 == 0:
            button.config(bg="brown")
        row.append(button)
    buttons.append(row)

for row in buttons:
    for button in row:
        if button.grid_info()['column'] == 3 and button.grid_info()['row'] == 2:
            piece_image = tk.PhotoImage(file ="pieces/b_pawn.png")
            
            
for y in range(1,9):
    y_label = tk.Label(root, text=str(y))
    y_label.grid(column=9, row=y)

letters = ["A","B","C","D","E","F","G","H"]
for x in range(1,9):
    y_label = tk.Label(root, text=letters[x - 1])
    y_label.grid(column=x, row=9)


root.mainloop()
