import psutil
import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import numpy as np

# ---------------- SETTINGS ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("⚙️ Real-Time Process Monitor")
app.geometry("1050x700")

# ---------------- TOP STATS FRAME ----------------
top_frame = ctk.CTkFrame(app, corner_radius=15)
top_frame.pack(pady=10, padx=10, fill="x")

cpu_label = ctk.CTkLabel(top_frame, text="CPU Usage", font=("Segoe UI", 16))
cpu_label.grid(row=0, column=0, padx=20, pady=5)
cpu_bar = ctk.CTkProgressBar(top_frame, width=400, height=15)
cpu_bar.grid(row=1, column=0, padx=20)
cpu_percent = ctk.CTkLabel(top_frame, text="0%", font=("Segoe UI", 14))
cpu_percent.grid(row=2, column=0)

mem_label = ctk.CTkLabel(top_frame, text="Memory Usage", font=("Segoe UI", 16))
mem_label.grid(row=0, column=1, padx=20, pady=5)
mem_bar = ctk.CTkProgressBar(top_frame, width=400, height=15)
mem_bar.grid(row=1, column=1, padx=20)
mem_percent = ctk.CTkLabel(top_frame, text="0%", font=("Segoe UI", 14))
mem_percent.grid(row=2, column=1)

# ---------------- REFRESH RATE SLIDER ----------------
slider_frame = ctk.CTkFrame(app, corner_radius=10)
slider_frame.pack(pady=5, padx=10, fill="x")

refresh_label = ctk.CTkLabel(slider_frame, text="Refresh Rate (seconds):", font=("Segoe UI", 14))
refresh_label.grid(row=0, column=0, padx=15, pady=10)

refresh_value_label = ctk.CTkLabel(slider_frame, text="0.5s", font=("Segoe UI", 14))
refresh_value_label.grid(row=0, column=2, padx=10)

refresh_rate = ctk.DoubleVar(value=2)

def on_slider_change(value):
    refresh_value_label.configure(text=f"{float(value):.1f}s")

refresh_slider = ctk.CTkSlider(
    slider_frame, from_=2, to=10, number_of_steps=18,
    variable=refresh_rate, command=on_slider_change, width=300
)
refresh_slider.grid(row=0, column=1, padx=10, pady=10)

# ---------------- PROCESS TABLE ----------------
table_frame = ctk.CTkFrame(app, corner_radius=15)
table_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("PID", "Name", "CPU (%)", "Memory (%)")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)
tree.pack(fill="both", expand=True)

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
tree.configure(yscroll=vsb.set)

# ---------------- BUTTON FRAME ----------------
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=8)

def kill_process():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("No Selection", "Please select a process first.")
        return
    pid = int(tree.item(sel[0])['values'][0])
    try:
        psutil.Process(pid).terminate()
        messagebox.showinfo("Terminated", f"Process {pid} terminated.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to terminate: {e}")

def suspend_process():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("No Selection", "Please select a process first.")
        return
    pid = int(tree.item(sel[0])['values'][0])
    try:
        psutil.Process(pid).suspend()
        messagebox.showinfo("Suspended", f"Process {pid} suspended.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to suspend: {e}")

def resume_process():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("No Selection", "Please select a process first.")
        return
    pid = int(tree.item(sel[0])['values'][0])
    try:
        psutil.Process(pid).resume()
        messagebox.showinfo("Resumed", f"Process {pid} resumed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to resume: {e}")

kill_btn = ctk.CTkButton(button_frame, text="❌ Kill", command=kill_process, fg_color="red", hover_color="#b30000", width=120)
kill_btn.grid(row=0, column=0, padx=10, pady=10)
suspend_btn = ctk.CTkButton(button_frame, text="⏸ Suspend", command=suspend_process, fg_color="#ff8800", hover_color="#cc7000", width=120)
suspend_btn.grid(row=0, column=1, padx=10, pady=10)
resume_btn = ctk.CTkButton(button_frame, text="▶ Resume", command=resume_process, fg_color="#00aa55", hover_color="#008844", width=120)
resume_btn.grid(row=0, column=2, padx=10, pady=10)

# ---------------- GRAPH FRAME ----------------
graph_frame = ctk.CTkFrame(app, corner_radius=15)
graph_frame.pack(padx=10, pady=10, fill="both", expand=True)

fig, ax = plt.subplots(figsize=(7, 2), dpi=100)
ax.set_title("CPU Usage Over Time", color="white")
ax.set_ylim(0, 100)
ax.set_facecolor("#202020")
fig.patch.set_facecolor("#202020")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_color("white")

cpu_data = []
line, = ax.plot(cpu_data, color='cyan', linewidth=2, alpha=0.9)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------- SMOOTHING FUNCTION ----------------
def smooth_transition(current, target, alpha=0.2):
    return current + alpha * (target - current)

# ---------------- UPDATE LOOP ----------------
def update_stats():
    smooth_cpu = psutil.cpu_percent(interval=None)
    smooth_mem = psutil.virtual_memory().percent
    last_table_update = time.time()

    while True:
        try:
            interval = float(refresh_rate.get())
            cpu = psutil.cpu_percent(interval=interval)
            mem = psutil.virtual_memory().percent

            # Smooth CPU/Memory
            smooth_cpu = smooth_transition(smooth_cpu, cpu)
            smooth_mem = smooth_transition(smooth_mem, mem)

            cpu_bar.set(smooth_cpu / 100)
            mem_bar.set(smooth_mem / 100)
            cpu_percent.configure(text=f"{smooth_cpu:.1f}%")
            mem_percent.configure(text=f"{smooth_mem:.1f}%")

            # Update process table every 1s
            if time.time() - last_table_update >= 1:
                for i in tree.get_children():
                    tree.delete(i)
                procs = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        procs.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                procs.sort(key=lambda p: p.get('cpu_percent', 0), reverse=True)
                for p in procs[:50]:
                    tree.insert("", "end", values=(
                        p['pid'],
                        (p['name'] or "")[:25],
                        f"{p['cpu_percent']:.1f}",
                        f"{p['memory_percent']:.1f}"
                    ))
                last_table_update = time.time()

            # Smooth Graph Update
            if len(cpu_data) > 200:
                cpu_data.pop(0)
            cpu_data.append(smooth_cpu)
            line.set_ydata(cpu_data)
            line.set_xdata(np.linspace(0, len(cpu_data) - 1, len(cpu_data)))
            ax.set_xlim(0, len(cpu_data))
            ax.figure.canvas.draw_idle()

        except Exception:
            pass

# ---------------- START THREAD ----------------
thread = threading.Thread(target=update_stats, daemon=True)
thread.start()

# ---------------- RUN APP ----------------
app.mainloop()
