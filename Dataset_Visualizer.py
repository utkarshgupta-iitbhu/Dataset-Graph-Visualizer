import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os

df = None
ax = None

# --- ELEGANT COLOR SCHEME ---
COLOR_PRIMARY = "#4f46e5"      # Indigo Accent
COLOR_PRIMARY_DARK = "#4338ca" # Indigo Hover
COLOR_SECONDARY = "#10b981"    # Emerald Green
COLOR_DANGER = "#ef4444"       # Red
COLOR_BG_DARK = "#0f172a"      # Dark Slate
COLOR_BG_LIGHT = "#f8fafc"     # Soft Gray Background
COLOR_CARD = "#ffffff"         # Card White
COLOR_TEXT_MAIN = "#1e293b"    # Charcoal Text
COLOR_TEXT_MUTED = "#64748b"   # Muted Slate Text
COLOR_BORDER = "#e2e8f0"       # Light Border
COLOR_DISABLED = "#cbd5e1"     # Disabled Gray

STYLE_MAP = {"Solid": "-", "Dashed": "--", "Dash-Dot": "-.", "Dotted": ":"}
MARKER_MAP = {"None": "None", "Circle": "o", "Square": "s", "Triangle": "^", "Diamond": "D", "Star": "*", "Cross": "x"}
PALETTE = {
    "Default": None,
    "Indigo Blue": "#4f46e5",
    "Emerald": "#10b981",
    "Coral Red": "#f43f5e",
    "Teal": "#06b6d4",
    "Golden Yellow": "#eab308",
    "Purple": "#a855f7",
    "Rose Pink": "#ec4899",
    "Amber Orange": "#f59e0b",
    "Dark Gray": "#334155"
}

def load_data():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel", "*.xlsx")])
    if not file_path:
        return
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        file_name = os.path.basename(file_path)
        update_ui_after_data_load(f"File: {file_name}")
        
    except Exception as e:
        messagebox.showerror("Loading Error", f"Failed to load dataset.\n\nDetails: {str(e)}")

def open_create_dataset_window():
    create_win = tk.Toplevel(window)
    create_win.title("Create Custom Dataset (30 Points)")
    create_win.geometry("550x580")
    create_win.config(bg=COLOR_BG_LIGHT)
    create_win.grab_set() 
    create_win.resizable(False, False)

    tk.Label(create_win, text="Enter your data points below:", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MAIN, font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

    name_frame = tk.Frame(create_win, bg=COLOR_BG_LIGHT)
    name_frame.pack(pady=5)
    
    tk.Label(name_frame, text="X Column Name:", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=10, sticky="w")
    tk.Label(name_frame, text="Y Column Name:", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=10, sticky="w")
    
    x_name_entry, y_name_entry = tk.Entry(name_frame, font=("Segoe UI", 10), width=20), tk.Entry(name_frame, font=("Segoe UI", 10), width=20)
    x_name_entry.insert(0, "X-Axis")
    y_name_entry.insert(0, "Y-Axis")
    x_name_entry.grid(row=1, column=0, padx=10)
    y_name_entry.grid(row=1, column=1, padx=10)

    grid_frame = tk.Frame(create_win, bg=COLOR_CARD, bd=1, relief=tk.SOLID)
    grid_frame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

    tk.Label(grid_frame, text="X Values", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=0, pady=2)
    tk.Label(grid_frame, text="Y Values", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=1, pady=2)
    tk.Label(grid_frame, text="   |   ", bg=COLOR_CARD).grid(row=0, column=2) 
    tk.Label(grid_frame, text="X Values", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=3, pady=2)
    tk.Label(grid_frame, text="Y Values", bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=4, pady=2)

    entry_rows = []
    for i in range(30):
        col_offset = 0 if i < 15 else 3
        row_pos = (i % 15) + 1
        
        x_val = tk.Entry(grid_frame, font=("Consolas", 10), width=12, justify="center", bg=COLOR_BG_LIGHT, relief=tk.FLAT)
        y_val = tk.Entry(grid_frame, font=("Consolas", 10), width=12, justify="center", bg=COLOR_BG_LIGHT, relief=tk.FLAT)
        
        x_val.grid(row=row_pos, column=col_offset, padx=5, pady=2)
        y_val.grid(row=row_pos, column=col_offset + 1, padx=5, pady=2)
        
        if i < 15: 
            tk.Label(grid_frame, text="   |   ", bg=COLOR_CARD).grid(row=row_pos, column=2)
            
        entry_rows.append((x_val, y_val))

    def save_manual_data():
        global df
        x_name, y_name = x_name_entry.get().strip() or "X-Axis", y_name_entry.get().strip() or "Y-Axis"
        if x_name == y_name: y_name += " (Y)"
        
        x_data, y_data = [], []
        for x_entry, y_entry in entry_rows:
            xv, yv = x_entry.get().strip(), y_entry.get().strip()
            if xv and yv:
                x_data.append(xv)
                y_data.append(yv)
                
        if not x_data: return messagebox.showwarning("No Data", "Please enter at least one valid pair.", parent=create_win)
            
        df = pd.DataFrame({x_name: x_data, y_name: y_data})
        df[x_name] = pd.to_numeric(df[x_name], errors='coerce')
        df[y_name] = pd.to_numeric(df[y_name], errors='coerce')
        
        update_ui_after_data_load("File: Custom Dataset")
        create_win.destroy()

    save_btn = tk.Button(create_win, text="💾 Save & Load Dataset", bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, pady=8, cursor="hand2", command=save_manual_data)
    save_btn.pack(fill=tk.X, padx=20, pady=(10, 15))
    save_btn.bind("<Enter>", lambda e: save_btn.config(bg=COLOR_PRIMARY_DARK))
    save_btn.bind("<Leave>", lambda e: save_btn.config(bg=COLOR_PRIMARY))

def on_graph_type_change(event=None):
    if type_combo.get() in ["Histogram", "Box Plot"]:
        y_combo.set("")
        y_combo.config(state=tk.DISABLED)
    else:
        y_combo.config(state="readonly")
        if df is not None and len(df.columns) > 1:
            y_combo.set(df.columns[1])

def update_ui_after_data_load(file_label):
    columns = list(df.columns)
    x_combo['values'] = columns
    y_combo['values'] = columns
    
    if len(columns) > 0: x_combo.set(columns[0])
    on_graph_type_change() 
    
    stats_text.config(state=tk.NORMAL)
    stats_text.delete(1.0, tk.END)
    stats_text.insert(tk.END, f"{file_label}\n")
    stats_text.insert(tk.END, f"Rows: {df.shape[0]} | Columns: {df.shape[1]}\n\n")
    stats_text.insert(tk.END, "Missing Values:\n")
    stats_text.insert(tk.END, str(df.isnull().sum()))
    stats_text.config(state=tk.DISABLED)
    
    plot_btn.config(state=tk.NORMAL, bg=COLOR_PRIMARY)
    clear_btn.config(state=tk.NORMAL, bg=COLOR_DANGER)

def clear_graph():
    global ax
    ax.clear()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_DISABLED)
    ax.spines['bottom'].set_color(COLOR_DISABLED)
    ax.set_title("Graph Cleared", color=COLOR_TEXT_MUTED, fontsize=14, pad=15)
    current_canvas.draw()
    
    stats_text.config(state=tk.NORMAL)
    stats_text.delete(1.0, tk.END)
    stats_text.insert(tk.END, "Canvas cleared. Ready for new plot.")
    stats_text.config(state=tk.DISABLED)

def on_click_annotate(event):
    if not annotate_var.get() or event.inaxes != ax: return
    if event.xdata and event.ydata:
        ax.annotate(f"({event.xdata:.2f}, {event.ydata:.2f})",
                    (event.xdata, event.ydata),
                    textcoords="offset points", xytext=(10,10),
                    bbox=dict(boxstyle="round,pad=0.3", fc="#fef08a", alpha=0.9, ec="#ca8a04"),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="#854d0e"))
        current_canvas.draw()

def generate_graph():
    global ax
    graph_type = type_combo.get()
    color_choice = PALETTE.get(color_combo.get())
    actual_style = STYLE_MAP.get(style_combo.get(), "-")
    actual_marker = MARKER_MAP.get(marker_combo.get(), "None")
    
    x_col = x_combo.get()
    y_col = y_combo.get()

    if not x_col or not graph_type:
        messagebox.showwarning("Missing Information", "Please select an X-Axis and a Graph Type.")
        return

    if not overlay_var.get():
        ax.clear()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLOR_DISABLED)
        ax.spines['bottom'].set_color(COLOR_DISABLED)
        ax.tick_params(colors='#475569')

    if grid_var.get():
        ax.grid(True, linestyle='-', alpha=0.25, color=COLOR_DISABLED)
    else:
        ax.grid(False)

    plot_kwargs = {}
    if color_choice: plot_kwargs['color'] = color_choice
    if actual_marker != "None": plot_kwargs['marker'] = actual_marker

    extra_stats = ""
    try:
        if graph_type == "Line Plot":
            plot_kwargs['linestyle'] = actual_style
            ax.plot(df[x_col], df[y_col], linewidth=2, label=y_col, **plot_kwargs)
            ax.set_ylabel("Values" if overlay_var.get() else y_col, color=COLOR_TEXT_MAIN, fontweight='bold')
            
        elif graph_type == "Scatter Plot":
            ax.scatter(df[x_col], df[y_col], alpha=0.7, label=y_col, **plot_kwargs)
            ax.set_ylabel("Values" if overlay_var.get() else y_col, color=COLOR_TEXT_MAIN, fontweight='bold')
            
            # --- BEST FIT LINE WITH EQUATION LABEL ---
            if best_fit_var.get():
                x_num, y_num = pd.to_numeric(df[x_col], errors='coerce'), pd.to_numeric(df[y_col], errors='coerce')
                mask = ~x_num.isna() & ~y_num.isna() 
                if mask.sum() > 1:
                    m, c = np.polyfit(x_num[mask], y_num[mask], 1)
                    
                    # Sort x data strictly to draw a clean line
                    x_sorted = np.sort(x_num[mask])
                    sign = "+" if c >= 0 else "-"
                    label_equation = f"Fit Line (y = {m:.2f}x {sign} {abs(c):.2f})"
                    
                    ax.plot(x_sorted, m * x_sorted + c, color=COLOR_DANGER, linestyle='--', linewidth=2, label=label_equation)
                    extra_stats = f"Slope (m): {m:.4f}\nIntercept: {c:.4f}\n"
            
        elif graph_type == "Bar Chart":
            ax.bar(df[x_col], df[y_col], alpha=0.9, label=y_col, **({'color': color_choice} if color_choice else {'color': COLOR_PRIMARY}))
            ax.set_ylabel("Values" if overlay_var.get() else y_col, color=COLOR_TEXT_MAIN, fontweight='bold')
            
        elif graph_type == "Histogram":
            num_data = pd.to_numeric(df[x_col], errors='coerce').dropna()
            if num_data.empty: return messagebox.showerror("Invalid Data", f"'{x_col}' requires numbers.")
            ax.hist(num_data, bins=20, edgecolor='white', linewidth=1.2, label=x_col, **({'color': color_choice} if color_choice else {'color': COLOR_SECONDARY}))
            ax.set_ylabel("Frequency", color=COLOR_TEXT_MAIN, fontweight='bold')
            
        elif graph_type == "Box Plot":
            num_data = pd.to_numeric(df[x_col], errors='coerce').dropna()
            if num_data.empty: return messagebox.showerror("Invalid Data", f"'{x_col}' requires numbers.")
            bp = ax.boxplot(num_data, patch_artist=True, boxprops=dict(facecolor=color_choice if color_choice else "#a855f7", color="#475569"), medianprops=dict(color="#ffffff", linewidth=2))
            ax.set_ylabel("Values", color=COLOR_TEXT_MAIN, fontweight='bold')

        ax.set_xlabel(x_col, color=COLOR_TEXT_MAIN, fontweight='bold')
        
        custom_title = title_entry.get().strip()
        if custom_title:
            ax.set_title(custom_title, fontsize=14, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
        elif overlay_var.get() and graph_type not in ["Box Plot"]:
            ax.set_title("Overlay Comparison", fontsize=14, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
        else:
            ax.set_title(f"{graph_type}: {x_col}" if graph_type in ["Histogram", "Box Plot"] else f"{graph_type}: {y_col} vs {x_col}", fontsize=14, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
        
        if legend_var.get() and graph_type not in ["Box Plot"]:
            ax.legend(frameon=True, labelcolor=COLOR_TEXT_MUTED, fancybox=True, shadow=True)

        fig.tight_layout()
        current_canvas.draw()

        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        target_col = x_col if graph_type in ["Histogram", "Box Plot"] else y_col
        numeric_data = pd.to_numeric(df[target_col], errors='coerce')
        
        if numeric_data.notna().sum() > 0:
            stats_text.insert(tk.END, f"--- {target_col} Stats ---\n")
            stats_text.insert(tk.END, f"Mean:   {numeric_data.mean():.2f}\n")
            stats_text.insert(tk.END, f"Median: {numeric_data.median():.2f}\n")
            stats_text.insert(tk.END, f"Max:    {numeric_data.max():.2f}\n")
            stats_text.insert(tk.END, f"Min:    {numeric_data.min():.2f}\n\n")
            if extra_stats: stats_text.insert(tk.END, f"--- Best Fit ---\n{extra_stats}")
        else:
            stats_text.insert(tk.END, f"Cannot calculate stats.\n'{target_col}' contains no numbers.")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n\n{str(e)}")

window = tk.Tk()
window.title("Data Dashboard Pro")
window.state('zoomed') 
window.config(bg=COLOR_BG_LIGHT) 

FONT_MAIN = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 10, "bold")

sidebar = tk.Frame(window, bg=COLOR_CARD, width=360, padx=15, pady=10, relief=tk.RIDGE, bd=1)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False) 

btn_frame = tk.Frame(sidebar, bg=COLOR_CARD)
btn_frame.pack(fill=tk.X, pady=(0, 10))

load_btn = tk.Button(btn_frame, text="📂 Load CSV / Excel", bg=COLOR_PRIMARY, fg="white", font=FONT_BTN, relief=tk.FLAT, pady=4, cursor="hand2", command=load_data)
load_btn.pack(fill=tk.X, pady=(0, 5))
load_btn.bind("<Enter>", lambda e: load_btn.config(bg=COLOR_PRIMARY_DARK))
load_btn.bind("<Leave>", lambda e: load_btn.config(bg=COLOR_PRIMARY))

create_btn = tk.Button(btn_frame, text="✏️ Create Dataset", bg=COLOR_SECONDARY, fg="white", font=FONT_BTN, relief=tk.FLAT, pady=4, cursor="hand2", command=open_create_dataset_window)
create_btn.pack(fill=tk.X)
create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#059669"))
create_btn.bind("<Leave>", lambda e: create_btn.config(bg=COLOR_SECONDARY))

tk.Label(sidebar, text="DATA SELECTION", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(fill=tk.X, pady=(5, 2))
sel_frame = tk.Frame(sidebar, bg=COLOR_CARD)
sel_frame.pack(fill=tk.X)
sel_frame.columnconfigure(1, weight=1) 

tk.Label(sel_frame, text="Graph Type:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 10))
type_combo = ttk.Combobox(sel_frame, values=["Line Plot", "Scatter Plot", "Bar Chart", "Histogram", "Box Plot"], state="readonly", font=FONT_MAIN)
type_combo.grid(row=0, column=1, sticky="ew", pady=3)
type_combo.set("Scatter Plot") # Set default to Scatter Plot
type_combo.bind("<<ComboboxSelected>>", on_graph_type_change)

tk.Label(sel_frame, text="X-Axis:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=1, column=0, sticky="w", pady=3, padx=(0, 10))
x_combo = ttk.Combobox(sel_frame, state="readonly", font=FONT_MAIN)
x_combo.grid(row=1, column=1, sticky="ew", pady=3)

tk.Label(sel_frame, text="Y-Axis:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=2, column=0, sticky="w", pady=3, padx=(0, 10))
y_combo = ttk.Combobox(sel_frame, state="readonly", font=FONT_MAIN)
y_combo.grid(row=2, column=1, sticky="ew", pady=3)

tk.Label(sidebar, text="FORMATTING", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(fill=tk.X, pady=(10, 2))
fmt_frame = tk.Frame(sidebar, bg=COLOR_CARD)
fmt_frame.pack(fill=tk.X)
fmt_frame.columnconfigure(1, weight=1)

tk.Label(fmt_frame, text="Custom Title:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 10))
title_entry = tk.Entry(fmt_frame, font=FONT_MAIN, bg=COLOR_BG_LIGHT, relief=tk.SOLID, bd=1)
title_entry.grid(row=0, column=1, sticky="ew", pady=3)

tk.Label(fmt_frame, text="Color:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=1, column=0, sticky="w", pady=3, padx=(0, 10))
color_combo = ttk.Combobox(fmt_frame, values=list(PALETTE.keys()), state="readonly", font=FONT_MAIN)
color_combo.grid(row=1, column=1, sticky="ew", pady=3)
color_combo.set("Default")

tk.Label(fmt_frame, text="Line Style:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=2, column=0, sticky="w", pady=3, padx=(0, 10))
style_combo = ttk.Combobox(fmt_frame, values=list(STYLE_MAP.keys()), state="readonly", font=FONT_MAIN)
style_combo.grid(row=2, column=1, sticky="ew", pady=3)
style_combo.set("Solid")

tk.Label(fmt_frame, text="Marker:", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, font=FONT_MAIN).grid(row=3, column=0, sticky="w", pady=3, padx=(0, 10))
marker_combo = ttk.Combobox(fmt_frame, values=list(MARKER_MAP.keys()), state="readonly", font=FONT_MAIN)
marker_combo.grid(row=3, column=1, sticky="ew", pady=3)
marker_combo.set("None")

tog_frame = tk.Frame(sidebar, bg=COLOR_CARD)
tog_frame.pack(fill=tk.X, pady=(10, 10))

overlay_var, grid_var = tk.BooleanVar(value=False), tk.BooleanVar(value=True)
legend_var, best_fit_var = tk.BooleanVar(value=False), tk.BooleanVar(value=False)
annotate_var = tk.BooleanVar(value=False)

tk.Checkbutton(tog_frame, text="Overlay", variable=overlay_var, bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, selectcolor=COLOR_BG_LIGHT, font=("Segoe UI", 9), padx=0, pady=0).grid(row=0, column=0, sticky="w")
tk.Checkbutton(tog_frame, text="Grid", variable=grid_var, bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, selectcolor=COLOR_BG_LIGHT, font=("Segoe UI", 9), padx=0, pady=0).grid(row=0, column=1, sticky="w")
tk.Checkbutton(tog_frame, text="Legend", variable=legend_var, bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, selectcolor=COLOR_BG_LIGHT, font=("Segoe UI", 9), padx=0, pady=0).grid(row=0, column=2, sticky="w")
tk.Checkbutton(tog_frame, text="Best Fit", variable=best_fit_var, bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, selectcolor=COLOR_BG_LIGHT, font=("Segoe UI", 9), padx=0, pady=0).grid(row=0, column=3, sticky="w")
tk.Checkbutton(tog_frame, text="Click to Annotate (Mark Values)", variable=annotate_var, bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, selectcolor=COLOR_BG_LIGHT, font=("Segoe UI", 9), padx=0, pady=0).grid(row=1, column=0, columnspan=4, sticky="w", pady=(5,0))

act_frame = tk.Frame(sidebar, bg=COLOR_CARD)
act_frame.pack(fill=tk.X, pady=(0, 10))
plot_btn = tk.Button(act_frame, text="📊 Plot", bg=COLOR_DISABLED, fg="white", font=FONT_BTN, relief=tk.FLAT, pady=5, cursor="hand2", state=tk.DISABLED, command=generate_graph)
plot_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
clear_btn = tk.Button(act_frame, text="🗑️ Clear", bg=COLOR_DISABLED, fg="white", font=FONT_BTN, relief=tk.FLAT, pady=5, cursor="hand2", state=tk.DISABLED, command=clear_graph)
clear_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))

plot_btn.bind("<Enter>", lambda e: plot_btn.config(bg=COLOR_PRIMARY_DARK) if plot_btn["state"] == tk.NORMAL else None)
plot_btn.bind("<Leave>", lambda e: plot_btn.config(bg=COLOR_PRIMARY) if plot_btn["state"] == tk.NORMAL else None)
clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#dc2626") if clear_btn["state"] == tk.NORMAL else None)
clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=COLOR_DANGER) if clear_btn["state"] == tk.NORMAL else None)

tk.Label(sidebar, text="DATASET INFO", bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"), anchor="w").pack(fill=tk.X, pady=(0,2))
stats_text = tk.Text(sidebar, bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_MAIN, font=("Consolas", 9), relief=tk.FLAT, padx=10, pady=10, state=tk.DISABLED)
stats_text.pack(fill=tk.BOTH, expand=True)

graph_frame = tk.Frame(window, bg=COLOR_BG_LIGHT, bd=0)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_DISABLED)
ax.spines['bottom'].set_color(COLOR_DISABLED)
ax.tick_params(colors='#475569')
ax.grid(True, linestyle='-', alpha=0.25, color=COLOR_DISABLED)

current_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

current_canvas.mpl_connect('button_press_event', on_click_annotate)

current_toolbar = NavigationToolbar2Tk(current_canvas, graph_frame)
current_toolbar.update()
current_toolbar.config(bg=COLOR_CARD)
for child in current_toolbar.winfo_children():
    try:
        child.configure(bg=COLOR_CARD)
    except tk.TclError:
        pass

window.mainloop()
