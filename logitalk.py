from customtkinter import *
from socket import *
import threading
class Window(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.minsize(300, 300)

    

        # --- БІЧНЕ МЕНЮ ---
        self.menu = CTkFrame(self, fg_color="#2b2b2b")   # темно-сірий фон
        self.menu.place(x=0, y=0, relheight=1)
        self.menu.configure(width=0)
        self.menu.pack_propagate(False)

        self.show_menu = False
        self.menu_width = 0

        self.text = CTkLabel(self.menu, text='Ваш нік', text_color="white")
        self.text.pack(pady=30)

        self.pole = CTkEntry(self.menu, placeholder_text="Введіть нік", fg_color="#3c3f41", text_color="white")
        self.pole.pack()

        self.btn = CTkButton(self, text='🔱', width=40, height=40,
        command=self.show_hide,
        fg_color="#1e90ff", hover_color="#4682b4")  # синя кнопка
        self.btn.place(x=5, y=5)

        # --- ЧАТ ---
        self.comm = CTkTextbox(self, state='disable', fg_color="#1c1c1c", text_color="white")
        self.comm.place(x=0, y=0)

        # --- ПОЛЕ ВВЕДЕННЯ ---
        self.message_input = CTkEntry(self, placeholder_text="Введіть повідомлення",
        fg_color="#2f4f4f", text_color="white")
        self.message_input.place(x=0, y=0)

        self.send_btn = CTkButton(self, text="▶️", width=30,
        command=self.send_message,
        fg_color="#325ecd", hover_color="#228b22")  # зелена кнопка
        self.send_btn.place(x=0, y=0)

        self.name = 'Taymalo'
        ...
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("localhost", 8080))
            self.sock.send(self.name.encode("utf-8"))
            threading.Thread(target=self.receive_message).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитись до сервера {e}")
        self.adaptive()

    def adaptive(self):
        menu_w = self.menu.winfo_width()
        win_w = self.winfo_width()
        win_h = self.winfo_height()

        input_h = 35
        padding = 10

        # Відображення повідомлень
        self.comm.configure(width=win_w - menu_w, height=win_h - input_h - 150)
        self.comm.place(x=menu_w, y=50)

        # Поле введення
        self.message_input.configure(width=win_w - menu_w - 170, height=input_h)
        self.message_input.place(x=menu_w + padding, y=win_h - input_h - 100)

        # Кнопка відправки
        self.send_btn.configure(width=30, height=input_h)
        self.send_btn.place(x=win_w - 150, y=win_h - input_h - 100)

        self.after(30, self.adaptive)

    # --- МЕНЮ ---
    def show_hide(self):
        if self.show_menu:
            self.show_menu = False
            self.close_menu()
        else:
            self.show_menu = True
            self.open_menu()

    def open_menu(self):
        self.name = self.pole.get()
        if self.menu_width < 200:
            self.menu_width += 20
            self.menu.configure(width=self.menu_width)
            self.after(20, self.open_menu)
    def close_menu(self):
        self.name = self.pole.get()
        if self.menu_width > 0:
            self.menu_width -= 20
            self.menu.configure(width=self.menu_width)
            self.after(20, self.close_menu)
    def add_message(self, text):
        self.comm.configure(state='normal')
        self.comm.insert(END, text + '\n')
        self.comm.configure(state='disable')
    def send_message(self):
        message = self.message_input.get()
        if message:
            self.add_message(f"{self.name}: {message}")
            data = f"TEXT@{self.name}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_input.delete(0, END)
    def receive_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()
    
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author = parts[1]
                filename = parts[2]

                self.add_message(f"{author} надіслав(ла) зображення: {filename}")

        else:
            self.add_message(line)



win = Window()
win.mainloop()