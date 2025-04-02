import tkinter as tk
from tkinter import messagebox
import threading
import time
from PIL import Image, ImageTk
import json
import os
import sys
from vk.methods import get_user_credentials, send_message

class MessageSenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Отправка сообщений VK")
        self.geometry("500x500")

        def add_context_menu(entry):
            menu = tk.Menu(entry, tearoff=0)
            menu.add_command(label="Вставить", command=lambda: entry.event_generate('<<Paste>>'))
            entry.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))
            entry.bind("<Control-v>", lambda event: self.handle_paste(entry, event))

        def handle_paste(self, entry, event):
            entry.event_generate('<<Paste>>')
            return "break"

        cookie_frame = tk.Frame(self)
        cookie_frame.pack(pady=5)
        tk.Label(cookie_frame, text="Cookie (remixdsid):").pack(side="left")
        self.cookie_entry = tk.Entry(cookie_frame, width=40)
        self.cookie_entry.pack(side="left")
        add_context_menu(self.cookie_entry)
        self.add_question_mark(cookie_frame,
            "Для получения куки:\n"
            "1. Откройте Сферум в браузере.\n"
            "2. Нажмите Ctrl + Shift + C.\n"
            "3. Перейдите в Application → Storage → Cookies → https://web.vk.me.\n"
            "4. В фильтре введите 'remixdsid' и скопируйте значение из столбца 'Value'.")

        message_frame = tk.Frame(self)
        message_frame.pack(pady=5)
        tk.Label(message_frame, text="Сообщение:").pack(side="left")
        self.message_entry = tk.Entry(message_frame, width=40)
        self.message_entry.pack(side="left")
        add_context_menu(self.message_entry)
        self.add_question_mark(message_frame,
            "Напишите сообщение, которое вы хотите отправить.")

        chat_ids_frame = tk.Frame(self)
        chat_ids_frame.pack(pady=5)
        tk.Label(chat_ids_frame, text="Chat IDs (через запятую):").pack(side="left")
        self.chat_ids_entry = tk.Entry(chat_ids_frame, width=40)
        self.chat_ids_entry.pack(side="left")
        add_context_menu(self.chat_ids_entry)
        self.add_question_mark_with_image(chat_ids_frame,
            "ID чата можно найти в адресной строке браузера.\n"
            "Например, в URL 'https://web.vk.me/convo/123456789?entrypoint=list_all' ID чата — '123456789'.",
            "chat_id_example.png")

        self.start_button = tk.Button(self, text="Начать отправку", command=self.start_sending)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Прекратить отправку", command=self.stop_sending, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self, text="Статус: Ожидание")
        self.status_label.pack(pady=10)

        self.count_label = tk.Label(self, text="Отправлено сообщений: 0")
        self.count_label.pack(pady=10)

        tk.Label(self, text="Сообщения отправляются каждые 5 секунд.", fg="gray").pack(pady=5)

        self.stop_sending_flag = False
        self.message_count = 0

        self.load_settings()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_question_mark(self, parent, tooltip_text):
        question_mark = tk.Label(parent, text="?", fg="blue", cursor="question_arrow")
        question_mark.pack(side="left", padx=5)
        question_mark.bind("<Enter>", lambda event: self.show_tooltip(event, tooltip_text))
        question_mark.bind("<Leave>", self.hide_tooltip)

    def add_question_mark_with_image(self, parent, tooltip_text, image_path):
        question_mark = tk.Label(parent, text="?", fg="blue", cursor="question_arrow")
        question_mark.pack(side="left", padx=5)
        question_mark.bind("<Enter>", lambda event: self.show_tooltip_with_image(event, tooltip_text, image_path))
        question_mark.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event, text):
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        tk.Label(self.tooltip, text=text, background="white", relief="solid", borderwidth=1).pack()
        self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

    def show_tooltip_with_image(self, event, text, image_path):
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        tk.Label(self.tooltip, text=text, background="white", relief="solid", borderwidth=1).pack()

        try:
            img_path = resource_path(image_path)
            img = Image.open(img_path)
            img = img.resize((611, 60), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.tooltip, image=photo)
            img_label.image = photo  # Сохраняем ссылку, чтобы изображение не удалялось
            img_label.pack()
        except FileNotFoundError:
            print(f"Ошибка: изображение не найдено по пути {img_path}")

        self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def load_settings(self):
        settings_file = "settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.cookie_entry.insert(0, settings.get("cookie", ""))
                    self.message_entry.insert(0, settings.get("message", ""))
                    self.chat_ids_entry.insert(0, settings.get("chat_ids", ""))
            except (json.JSONDecodeError, IOError):
                print("Ошибка загрузки настроек")

    def save_settings(self):
        settings = {
            "cookie": self.cookie_entry.get(),
            "message": self.message_entry.get(),
            "chat_ids": self.chat_ids_entry.get()
        }
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
        except IOError:
            print("Ошибка сохранения настроек")

    def on_closing(self):
        self.save_settings()
        self.destroy()

    def start_sending(self):
        cookie = self.cookie_entry.get().strip()
        message = self.message_entry.get().strip()
        chat_ids_str = self.chat_ids_entry.get().strip()

        if not cookie or not message or not chat_ids_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        self.chat_ids = [cid.strip() for cid in chat_ids_str.split(",")]

        try:
            user = get_user_credentials(cookie)
            self.access_token = user.access_token
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить access token: {e}")
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Статус: Отправка...")
        self.message_count = 0
        self.update_count_label()

        self.stop_sending_flag = False
        threading.Thread(target=self.sending_loop, args=(self.access_token, self.chat_ids, message), daemon=True).start()

    def stop_sending(self):
        self.stop_sending_flag = True
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Статус: Остановлено")

    def sending_loop(self, access_token, chat_ids, message):
        while not self.stop_sending_flag:
            for chat_id in chat_ids:
                try:
                    send_message(access_token, chat_id, message)
                    self.message_count += 1
                    self.update_count_label()
                except Exception as e:
                    print(f"Ошибка при отправке в {chat_id}: {e}")
            time.sleep(5)

    def update_count_label(self):
        self.count_label.config(text=f"Отправлено сообщений: {self.message_count}")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = MessageSenderApp()
    app.mainloop()