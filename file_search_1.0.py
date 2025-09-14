import os
import time
import difflib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def search_with_progress(folder, mode, query=None):
    matches = []
    files_scanned = 0
    start_time = time.time()

    for root, _, files in os.walk(folder):
        for file in files:
            files_scanned += 1
            path = os.path.join(root, file)

            # Progress update every 25,000 files
            if files_scanned % 25000 == 0:
                results_box.insert(tk.END, f"[INFO] Scanned {files_scanned} files...\n")
                results_box.see(tk.END)
                root_window.update()

            try:
                if mode == "filename":
                    ratio = difflib.SequenceMatcher(None, query.lower(), file.lower()).ratio()
                    if ratio >= 0.6:  # fuzzy threshold
                        matches.append(path)

                elif mode == "extension" and file.endswith(query):
                    matches.append(path)

            except PermissionError:
                continue

    elapsed = time.time() - start_time
    return matches, files_scanned, elapsed


def run_search():
    folder = folder_var.get()
    mode = mode_var.get()
    query = query_var.get()

    if not os.path.exists(folder):
        messagebox.showerror("Error", "Folder does not exist!")
        return

    results_box.delete("1.0", tk.END)
    results_box.insert(tk.END, f"[INFO] Starting search in: {folder}\n")

    if mode == "count":
        total_files = sum(len(files) for _, _, files in os.walk(folder))
        results_box.insert(tk.END, f"[RESULT] Total files in {folder}: {total_files}\n")
        return

    matches, scanned, elapsed = search_with_progress(folder, mode, query)

    results_box.insert(tk.END, f"\n--- RESULTS ---\n")
    if matches:
        for i, path in enumerate(matches, 1):
            results_box.insert(tk.END, f"[MATCH] {i}. {path}\n")
    else:
        results_box.insert(tk.END, "[INFO] No matches found.\n")

    results_box.insert(tk.END, f"\n[INFO] Scanned {scanned} files total.\n")
    results_box.insert(tk.END, f"[INFO] Completed in {elapsed:.2f} seconds\n")


def pick_folder():
    folder = filedialog.askdirectory()
    folder_var.set(folder)


# --- GUI Setup ---
root_window = tk.Tk()
root_window.title("Hacker File Searcher")
root_window.geometry("800x600")
root_window.configure(bg="black")

# --- Styling ---
text_color = "#00FF00"  # neon green
font_style = ("Consolas", 10)

# Title
tk.Label(root_window, text="FILE SEARCHER 1337", font=("Consolas", 14, "bold"),
         fg=text_color, bg="black").pack(pady=10)

# Folder selection
folder_var = tk.StringVar()
tk.Label(root_window, text="Target Directory:", fg=text_color, bg="black", font=font_style).pack(anchor="w")
tk.Entry(root_window, textvariable=folder_var, width=60, font=font_style,
         fg=text_color, bg="black", insertbackground=text_color).pack(anchor="w", pady=2)
tk.Button(root_window, text="Browse", command=pick_folder,
          fg=text_color, bg="black", relief="solid", borderwidth=1).pack(anchor="w", pady=5)

# Search mode
mode_var = tk.StringVar(value="filename")
tk.Label(root_window, text="Search Mode:", fg=text_color, bg="black", font=font_style).pack(anchor="w")
tk.Radiobutton(root_window, text="By Filename (Fuzzy)", variable=mode_var, value="filename",
               fg=text_color, bg="black", selectcolor="black", activeforeground=text_color,
               font=font_style).pack(anchor="w")
tk.Radiobutton(root_window, text="By Extension", variable=mode_var, value="extension",
               fg=text_color, bg="black", selectcolor="black", activeforeground=text_color,
               font=font_style).pack(anchor="w")
tk.Radiobutton(root_window, text="Count Files", variable=mode_var, value="count",
               fg=text_color, bg="black", selectcolor="black", activeforeground=text_color,
               font=font_style).pack(anchor="w")

# Query input
query_var = tk.StringVar()
tk.Label(root_window, text="Search Query (Filename or Extension):",
         fg=text_color, bg="black", font=font_style).pack(anchor="w")
tk.Entry(root_window, textvariable=query_var, width=40, font=font_style,
         fg=text_color, bg="black", insertbackground=text_color).pack(anchor="w", pady=2)

# Search button
tk.Button(root_window, text=">>> EXECUTE SEARCH <<<", command=run_search,
          fg=text_color, bg="black", relief="solid", borderwidth=2,
          font=("Consolas", 11, "bold")).pack(pady=15)

# Results box (terminal vibe)
results_box = scrolledtext.ScrolledText(root_window, width=100, height=20,
                                        font=("Consolas", 9), fg=text_color, bg="black",
                                        insertbackground=text_color)
results_box.pack()

root_window.mainloop()
