import re
import tkinter as tk
from tkinter import messagebox

LABEL = re.compile(r"\[(Verse|Chorus|Refrain|Bridge|Outro|Intro|Pre-Chorus|Hook|Interlude)[^\]]*\]", re.I)

def convert():
    text = inp.get("1.0", "end")
    # [line text](url) -> line text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)

    blocks, cur, skipping = [], None, False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.lower() == "you might also like":
            skipping = True
            continue
        if LABEL.fullmatch(line):
            skipping = False
            if cur:
                blocks.append(cur)
            cur = [line]
        elif cur is not None and not skipping:
            cur.append(line)
    if cur:
        blocks.append(cur)

    if not blocks:
        messagebox.showwarning("Nothing found", "No section labels like [Verse 1] were found in the pasted text.")
        return

    html = "\n\n".join("<p> " + " <br>\n".join(b) + " </p>" for b in blocks) + "\n"

    out.delete("1.0", "end")
    out.insert("1.0", html)

    with open("lyrics.html", "w", encoding="utf-8") as f:
        f.write(html)

    root.clipboard_clear()
    root.clipboard_append(html)
    status.config(text=f"Done: {len(blocks)} sections. Copied to clipboard and saved to lyrics.html")

root = tk.Tk()
root.title("Lyrics to HTML")

tk.Label(root, text="Paste lyrics here:").pack(anchor="w", padx=8, pady=(8, 0))
inp = tk.Text(root, width=90, height=15)
inp.pack(padx=8, pady=4)

tk.Button(root, text="Convert", command=convert).pack(pady=4)
status = tk.Label(root, text="")
status.pack()

tk.Label(root, text="HTML output:").pack(anchor="w", padx=8)
out = tk.Text(root, width=90, height=15)
out.pack(padx=8, pady=(4, 8))

root.mainloop()
