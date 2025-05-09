import json
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import os
import shutil
from fpdf import FPDF

class RecipeBook:
    def __init__(self):
        self.file_path = os.path.join(os.path.expanduser("~"), "Documents", "recipes.json")
        self.image_folder = os.path.join(os.path.expanduser("~"), "Documents", "recipe_images")
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        self.recipes = {}
        self.load_recipes()
    
    def load_recipes(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.recipes = json.load(f)
        except FileNotFoundError:
            self.recipes = {}
    
    def save_recipes(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, indent=4, ensure_ascii=False)
    
    def add_recipe(self, name, ingredients, instructions, category, image_path):
        if image_path:
            new_image_path = os.path.join(self.image_folder, os.path.basename(image_path))
            shutil.copy(image_path, new_image_path)
        else:
            new_image_path = ""
        
        self.recipes[name] = {
            'ingredients': ingredients,
            'instructions': instructions,
            'category': category,
            'image': new_image_path
        }
        self.save_recipes()
    
    def delete_recipe(self, name):
        if name in self.recipes:
            recipe = self.recipes[name]
            if recipe['image'] and os.path.exists(recipe['image']):
                os.remove(recipe['image'])
            del self.recipes[name]
            self.save_recipes()
    
    def search_recipe(self, search_term):
        results = {}
        for name, details in self.recipes.items():
            if search_term.lower() in name.lower() or search_term.lower() in details['category'].lower():
                results[name] = details
        return results

class RecipeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Digitales Kochbuch")
        self.recipe_book = RecipeBook()
        self.image_path = ""
        
        self.create_widgets()
        self.update_recipe_list()
    
    def create_widgets(self):
        ttk.Label(self.master, text="Rezeptname:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.master, text="Zutaten:").grid(row=1, column=0, padx=5, pady=5)
        self.ingredients_entry = tk.Text(self.master, height=5, width=30)
        self.ingredients_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.master, text="Zubereitung:").grid(row=2, column=0, padx=5, pady=5)
        self.instructions_entry = tk.Text(self.master, height=10, width=30)
        self.instructions_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.master, text="Kategorie:").grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.master, width=30)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.master, text="Bild hinzufügen", command=self.add_image).grid(row=4, column=0, padx=5, pady=5)
        self.image_label = ttk.Label(self.master, text="Kein Bild ausgewählt")
        self.image_label.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Button(self.master, text="Rezept hinzufügen", command=self.add_recipe).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Rezept löschen", command=self.delete_recipe).grid(row=5, column=1, padx=5, pady=5)
        
        self.recipe_list = tk.Listbox(self.master, width=50)
        self.recipe_list.grid(row=0, column=2, rowspan=6, padx=5, pady=5)
        self.recipe_list.bind('<<ListboxSelect>>', self.show_recipe_details)
        
        ttk.Label(self.master, text="Suche:").grid(row=6, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.master, width=30)
        self.search_entry.grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Suchen", command=self.search_recipes).grid(row=6, column=2, padx=5, pady=5)
        
        self.details_text = tk.Text(self.master, height=15, width=50)
        self.details_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        
        self.image_display = ttk.Label(self.master)
        self.image_display.grid(row=0, column=3, rowspan=7, padx=5, pady=5)
        
        ttk.Button(self.master, text="Als PDF exportieren", command=self.export_to_pdf).grid(row=5, column=2, padx=5, pady=5)
    
    def add_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if self.image_path:
            self.image_label.config(text=os.path.basename(self.image_path))
    
    def add_recipe(self):
        name = self.name_entry.get()
        ingredients = self.ingredients_entry.get("1.0", tk.END).strip()
        instructions = self.instructions_entry.get("1.0", tk.END).strip()
        category = self.category_entry.get()
        
        if not name or not ingredients or not instructions or not category:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")
            return
        
        self.recipe_book.add_recipe(name, ingredients, instructions, category, self.image_path)
        self.update_recipe_list()
        self.clear_fields()
    
    def delete_recipe(self):
        selection = self.recipe_list.curselection()
        if not selection:
            return
        name = self.recipe_list.get(selection[0])
        self.recipe_book.delete_recipe(name)
        self.update_recipe_list()
    
    def search_recipes(self):
        search_term = self.search_entry.get()
        results = self.recipe_book.search_recipe(search_term)
        self.recipe_list.delete(0, tk.END)
        for name in results:
            self.recipe_list.insert(tk.END, name)
    
    def update_recipe_list(self):
        self.recipe_list.delete(0, tk.END)
        for name in self.recipe_book.recipes:
            self.recipe_list.insert(tk.END, name)
    
    def show_recipe_details(self, event):
        selection = self.recipe_list.curselection()
        if not selection:
            return
        name = self.recipe_list.get(selection[0])
        recipe = self.recipe_book.recipes[name]
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Kategorie: {recipe['category']}\n\n")
        self.details_text.insert(tk.END, "Zutaten:\n" + recipe['ingredients'] + "\n\n")
        self.details_text.insert(tk.END, "Zubereitung:\n" + recipe['instructions'])
        self.details_text.config(state=tk.DISABLED)
        
        if recipe['image'] and os.path.exists(recipe['image']):
            image = Image.open(recipe['image'])
            image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_display.config(image=photo)
            self.image_display.image = photo
        else:
            self.image_display.config(image='')
    
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.ingredients_entry.delete(1.0, tk.END)
        self.instructions_entry.delete(1.0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.image_path = ""
        self.image_label.config(text="Kein Bild ausgewählt")
    
    def export_to_pdf(self):
        selection = self.recipe_list.curselection()
        if not selection:
            messagebox.showerror("Fehler", "Bitte ein Rezept auswählen!")
            return
            
        name = self.recipe_list.get(selection[0])
        recipe = self.recipe_book.recipes[name]
        
        pdf = FPDF()
        pdf.add_page()
        
        # Schriftarten hinzufügen
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
        
        pdf.set_font('DejaVu', size=12)
        
        # PDF-Header
        pdf.set_font('DejaVu', 'B', 20)
        pdf.cell(200, 10, txt=name, ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(200, 10, txt=f"Kategorie: {recipe['category']}", ln=2)
        
        # Bild hinzufügen
        if recipe['image'] and os.path.exists(recipe['image']):
            pdf.image(recipe['image'], x=10, y=40, w=50)
            pdf.set_y(100)  # Position nach dem Bild
            
        # Zutaten
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(200, 10, txt="Zutaten:", ln=1)
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 10, txt=recipe['ingredients'])
        
        # Zubereitung
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(200, 10, txt="Zubereitung:", ln=1)
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 10, txt=recipe['instructions'])
        
        # Datei speichern
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Dateien", "*.pdf")],
            initialfile=f"{name}.pdf"
        )
        
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Erfolg", f"PDF wurde gespeichert unter:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
