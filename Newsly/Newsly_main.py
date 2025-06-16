import customtkinter as ctk
import threading
import queue
import time
from NewsChat import run_chat_ui
from Testagent import get_ai_news

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

news_data = get_ai_news()
new_news_queue = queue.Queue()
rendered_titles = set()
loading_in_progress = False

def handle_chat(news_item):
    print("[CHAT] Title:", news_item["title"])
    run_chat_ui(news_item["title"])

def handle_like(news_item):
    print("[LIKE] Title:", news_item["title"])

def background_news_loader():
    global loading_in_progress
    loading_in_progress = True
    time.sleep(1.5)  # simulate delay

    # Fake new items
    more_news = get_ai_news()
    for item in more_news:
        news_data.append(item)
        new_news_queue.put(item)

    loading_in_progress = False

def create_news_ui(news_data, handle_chat, handle_like):
    app = ctk.CTk()
    app.title("Newsly-News")
    app.geometry("900x700")

    scroll_frame = ctk.CTkScrollableFrame(app, width=860, height=660)
    scroll_frame.pack(pady=10, padx=10,fill="both",expand=True)

    canvas = scroll_frame._parent_canvas

    def render_news_item(news_item):
        title = news_item["title"]
        bullets = news_item["Bullets"]

        if title in rendered_titles:
            return
        rendered_titles.add(title)

        card = ctk.CTkFrame(scroll_frame, border_width=1,width=810)
        card.pack(fill="x",expand=True, pady=10, padx=5)

        ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"),
                     wraplength=800, anchor="w").pack(pady=5, padx=10)

        for point in bullets:
            ctk.CTkLabel(card, text="• " + point, font=("Arial", 13),
                         wraplength=800, anchor="w", justify="left",width=810).pack(anchor="w", padx=20)

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=5, padx=10, anchor="e")

        ctk.CTkButton(button_frame, text="💬 Chat", width=80,
                      command=lambda item=news_item: handle_chat(item)).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="❤️ Like", width=80,
                      command=lambda item=news_item: handle_like(item)).pack(side="left", padx=5)

    def check_scroll_position(event=None):
        yview = canvas.yview()
        if yview[1] >= 0.99 and not loading_in_progress:
            threading.Thread(target=background_news_loader, daemon=True).start()

    def poll_new_items():
        while not new_news_queue.empty():
            item = new_news_queue.get()
            render_news_item(item)
        app.after(500, poll_new_items)

    def _on_mousewheel(event):
        canvas.yview_scroll((-1 * (event.delta // 120))*45, "units")
        check_scroll_position()

    def _bind_mousewheel(widget):
        widget.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        widget.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-3, "units"))  # Linux
        widget.bind_all("<Button-5>", lambda e: canvas.yview_scroll(10, "units"))   # Linux

    _bind_mousewheel(canvas)

    for item in news_data:
        render_news_item(item)

    canvas.bind("<Configure>", check_scroll_position)
    poll_new_items()
    app.mainloop()



if __name__ == "__main__":
    create_news_ui(news_data, handle_chat, handle_like)
