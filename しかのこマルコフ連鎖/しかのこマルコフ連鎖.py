import random
import time
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image, ImageTk

# マルコフ連鎖の遷移確率定義
transitions = {
    'ん': {'': 0.5, 'た': 0.5},
    '': {'ん': 0.5, 'し': 0.5},
    'た': {'ん': 1},
    'し': {'か': 0.5, 'た': 0.5},
    'か': {'の': 1},
    'の': {'こ': 1},
    'こ': {'の': 0.5, 'し': 0.25, 'こ':0.25}
}

def generate_text(start_state, length):
    current_state = start_state
    text = current_state
    for _ in range(length - 1):
        if current_state not in transitions:
            break
        next_state = random.choices(
            list(transitions[current_state].keys()),
            weights=list(transitions[current_state].values())
        )[0]
        text += next_state
        current_state = next_state
    return text

def run_generation():
    target_text = "しかのこのこのここしたんたん"
    start_state = 'し'
    text_length = len(target_text)
    attempts = 0

    while True:
        attempts += 1
        generated_text = generate_text(start_state, text_length)
        text_box.insert(tk.END, f"試行 {attempts}: {generated_text}\n")
        text_box.see(tk.END)
        
        if generated_text == target_text:
            message_var.set(f"生成されました！ 合計試行回数: {attempts}")
            break
        time.sleep(0.01)

def start_generation():
    threading.Thread(target=run_generation, daemon=True).start()

# GUI作成
root = tk.Tk()
root.title("生成")

root.geometry("650x700")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 画像
image = Image.open("sikanoko.jpeg") 
image = image.resize((400, 200), Image.LANCZOS)  # サイズを調整
photo = ImageTk.PhotoImage(image)
image_label = ttk.Label(frame, image=photo)
image_label.image = photo
image_label.grid(row=0, column=0, pady=10)

# テキストボックス
text_box = tk.Text(frame, width=80, height=20) 
text_box.grid(row=1, column=0, pady=10)

# メッセージ
message_var = tk.StringVar()
message_label = ttk.Label(frame, textvariable=message_var, font=("", 20))  # フォントサイズを大きく
message_label.grid(row=2, column=0, pady=10)

# 生成ボタン
generate_button = ttk.Button(frame, text="生成", command=start_generation)
generate_button.grid(row=3, column=0, pady=10)

root.mainloop()