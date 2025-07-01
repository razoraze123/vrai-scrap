import tkinter as tk
from tkinter import messagebox, scrolledtext
from bs4 import BeautifulSoup


def est_image_valide(img_tag):
    src = img_tag.get("src", "")
    if not src or "data:" in src or not src.startswith(("//", "http")):
        return False

    parent = img_tag.find_parent()
    if parent:
        parent_classes = parent.get("class", [])
        if any(cls in parent_classes for cls in ["thumbnail", "product-gallery__thumbnail", "scroll-area"]):
            return False

    try:
        width = int(img_tag.get("width", 0))
        height = int(img_tag.get("height", 0))
        if width < 500 or height < 500:
            return False
    except Exception:
        return False

    return True


def launch_tool(parent=None):
    fenetre = tk.Toplevel(parent) if parent else tk.Tk()
    fenetre.title("\U0001F9E0 D\u00e9tecteur intelligent de s\u00e9lecteur CSS")
    fenetre.geometry("850x600")
    fenetre.resizable(True, True)

    label = tk.Label(fenetre, text="\U0001F4E5 Collez ici un extrait HTML :", font=("Helvetica", 12, "bold"))
    label.pack(pady=10)

    champ_html = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=100, height=20)
    champ_html.pack(padx=10, pady=5)

    bouton_analyser = tk.Button(fenetre, text="\U0001F50D Analyser le HTML")
    bouton_analyser.pack(pady=10)

    resultats = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=100, height=15)
    resultats.pack(padx=10, pady=5)

    btn_copier = tk.Button(fenetre, text="\U0001F4CB Copier les s\u00e9lecteurs")
    btn_copier.pack(pady=10)

    def analyser_html():
        contenu_html = champ_html.get("1.0", tk.END)
        if not contenu_html.strip():
            messagebox.showwarning("Attention", "Veuillez coller du HTML.")
            return

        soup = BeautifulSoup(contenu_html, 'html.parser')
        resultats.delete("1.0", tk.END)

        tag_principal = soup.find(True)
        if tag_principal:
            tag_name = tag_principal.name
            classes = tag_principal.get('class', [])
            sel_css = f"{tag_name}{'.' + '.'.join(classes) if classes else ''}"
            resultats.insert(tk.END, f"\U0001F4E6 Bloc principal : {sel_css}\n\n")

        images = soup.find_all("img")
        images_valides = [img for img in images if est_image_valide(img)]

        if images_valides:
            resultats.insert(tk.END, f"\U0001F5BC\uFE0F Images d\u00e9tect\u00e9es ({len(images_valides)}):\n")
            for i, img in enumerate(images_valides, start=1):
                img_class = img.get("class", [])
                src = img.get("src")
                sel_img = f"img{'.' + '.'.join(img_class) if img_class else ''}"
                resultats.insert(tk.END, f"  {i}. {sel_img} \u2192 src: {src}\n")
            resultats.insert(tk.END, "\n")

        text_blocks = soup.find_all(['p', 'span', 'div'], string=True)
        descriptions = []
        for tag in text_blocks:
            text = tag.get_text(strip=True)
            if len(text) > 30:
                sel = tag.name + ('.' + '.'.join(tag.get('class', [])) if tag.get('class') else '')
                descriptions.append((sel, text))

        if descriptions:
            resultats.insert(tk.END, "\U0001F4C4 Blocs texte / descriptions d\u00e9tect\u00e9s :\n")
            for i, (sel, texte) in enumerate(descriptions[:5], start=1):
                resultats.insert(tk.END, f"  {i}. {sel} \u2192 \"{texte[:60]}...\"\n")

    def copier_resultat():
        contenu = resultats.get("1.0", tk.END)
        fenetre.clipboard_clear()
        fenetre.clipboard_append(contenu)
        fenetre.update()
        messagebox.showinfo("Copi\u00e9", "Le s\u00e9lecteur a \u00e9t\u00e9 copi\u00e9 dans le presse-papier.")

    bouton_analyser.config(command=analyser_html)
    btn_copier.config(command=copier_resultat)

    if parent is None:
        fenetre.mainloop()
    return fenetre


if __name__ == "__main__":
    launch_tool()
