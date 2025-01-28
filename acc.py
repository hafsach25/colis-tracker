import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import customtkinter as ctk
import sqlite3
import webbrowser 

# Couleurs
orange = "#FF7F32"  # Couleur orange
blue_ciel = "#87CEFA"  # Bleu ciel
bg_color = "#f5f5f5"  # Fond gris clair

class TrackingApp(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")
        self.result_frame = tk.Frame(self, bg="white")
        self.result_frame.pack_forget()

        # Frame supérieure
        self.create_top_frame()

        # Chemin de l'image de fond
        self.image_path = "photo.png"  # Remplacez par le chemin correct de votre image
        try:
            self.background_image = Image.open(self.image_path)
        except FileNotFoundError:
            print(f"Erreur : L'image '{self.image_path}' est introuvable.")
            self.background_image = None

        # Frame inférieure pour l'image de fond
        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.pack(fill="both", expand=True, side="top")  # Ensure it fills the top space

        # Label pour l'image de fond
        self.background_label = tk.Label(self.bottom_frame, bg="white")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind pour redimensionner la fenêtre
        self.bottom_frame.bind("<Configure>", self.update_background)

        # Menu Frame
        self.menu_frame = tk.Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")

        # Créer les boutons du menu
        home_icon = ctk.CTkButton(
            self.menu_frame,
            text="🏠",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
        )

        gps_icon = ctk.CTkButton(
            self.menu_frame,
            text="🧭",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
            command=self.gomap
        )

        compte_icon = ctk.CTkButton(
            self.menu_frame,
            text="👤",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
            command=self.alleraccount
        )

        # Add buttons to the grid
        home_icon.grid(row=0, column=0, padx=10, pady=5)
        gps_icon.grid(row=0, column=1, padx=10, pady=5)
        compte_icon.grid(row=0, column=2, padx=10, pady=5)

        # Configure column weights for resizing
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)

        # Champ de recherche
        self.search_frame = tk.Frame(self, bg="#e8fbff", bd=0)
        self.search_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Entrer le numéro de votre colis",
            width=500,
            height=35,
            font=("Arial", 16),
            corner_radius=100,
            border_width=0,
            fg_color="#e8fbff",
            text_color="black",
        )
        self.search_entry.pack(side="left", padx=10)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Chercher",
            font=("Arial", 17),
            corner_radius=0,
            width=150,
            height=40,
            fg_color=orange,
            hover_color="#FF944D",
            text_color="white",
            command=self.rechercher_colis  # Ajout de la commande
        )
        self.search_button.pack(side="right",padx=0)
        # Créer la frame de résultat (initialement cachée)
        self.result_frame = tk.Frame(self, bg="white")
        self.result_frame.pack_forget()

        self.reclamation = ctk.CTkButton(
            self.bottom_frame,
            text="Réclamation", 
            font=("Arial", 17),
            corner_radius=0,
            width=150,
            height=10,
            fg_color=blue_ciel,
            hover_color="#FF944D",
            text_color="white",
            command=self.ouvrir_reclamation
        )
        self.reclamation.pack(pady=150)


        # Créer la side frame mais ne pas l'afficher au départ
        self.side_frame = tk.Frame(self, bg="white")
        self.side_frame.pack_forget()  # Ne pas l'afficher

        # Ajouter le contenu de la side frame
        self.createMenuFrame()  # Nom corrigé
    def ouvrir_reclamation(self):
    
        gmail_url = "https://mail.google.com/mail/?view=cm&fs=1&to=speedyexpress026@gmail.com&su=Réclamation"
        webbrowser.open(gmail_url)
    
    def rechercher_colis(self):
        # Nettoyer toutes les frames existantes
        self.bottom_frame.pack_forget()
        self.search_frame.place_forget()
        self.side_frame.pack_forget()  # S'assurer que la side_frame est cachée
        
        # Vider la frame de résultat avant d'ajouter de nouveaux éléments
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Afficher la frame de résultat en plein écran
        self.result_frame.pack(fill="both", expand=True)
        
        # Récupérer l'ID du colis
        id_colis = self.search_entry.get()
        
        # Données de test (simulant une base de données)
        colis_test = {
            "12345": {
                "statut": "En cours de livraison",
                "ville_depart": "Casablanca", 
                "ville_arrivee": "Rabat",
                "date_expedition": "2024-01-15"
            },
            "67890": {
                "statut": "En attente de récupération",
                "ville_depart": "Marrakech",
                "ville_arrivee": "Tanger", 
                "date_expedition": "2024-01-16"
            }
        }
        
        if id_colis in colis_test:
            colis = colis_test[id_colis]
            
            # Créer les labels pour afficher les informations
            info_frame = tk.Frame(self.result_frame, bg="white")
            info_frame.pack(pady=20)
            
            tk.Label(info_frame, text=f"Colis N° {id_colis}", font=("Arial", 20, "bold"), bg="white").pack()
            tk.Label(info_frame, text=f"Statut: {colis['statut']}", font=("Arial", 16), bg="white").pack()
            tk.Label(info_frame, text=f"De: {colis['ville_depart']}", font=("Arial", 16), bg="white").pack()
            tk.Label(info_frame, text=f"Vers: {colis['ville_arrivee']}", font=("Arial", 16), bg="white").pack()
            tk.Label(info_frame, text=f"Date d'expédition: {colis['date_expedition']}", font=("Arial", 16), bg="white").pack()
            
           
            
            # Bouton pour revenir à la recherche
            retour_button = ctk.CTkButton(
                self.result_frame,
                text="Nouvelle recherche",
                font=("Arial", 17),
                corner_radius=0,
                width=200,
                height=40,
                fg_color=blue_ciel,
                hover_color="#70B9F2",
                text_color="white",
                command=self.retour_recherche
            )
            retour_button.pack(pady=10)
            
        else:
            # Message si aucun colis n'est trouvé
            tk.Label(self.result_frame, 
                    text="Aucun colis trouvé avec cet identifiant", 
                    font=("Arial", 16), 
                    bg="white").pack(pady=20)
            
            # Bouton pour revenir à la recherche
            retour_button = ctk.CTkButton(
                self.result_frame,
                text="Retour",
                font=("Arial", 17),
                corner_radius=0,
                width=200,
                height=40,
                fg_color=blue_ciel,
                hover_color="#70B9F2",
                text_color="white",
                command=self.retour_recherche
            )
            retour_button.pack(pady=10)

    def retour_recherche(self):
        # Nettoyer la frame de résultat
        self.result_frame.pack_forget()
    # Réinitialiser le champ de recherche
        self.search_entry.delete(0, 'end')
    
    # Réafficher la frame de fond et la barre de recherche
        self.bottom_frame.pack(fill="both", expand=True, side="top")
        self.search_frame.place(relx=0.5, rely=0.3, anchor="center")

    def create_top_frame(self):
        """Crée la frame supérieure avec le titre de l'application."""
        top_frame = tk.Frame(self, height=100, bg=blue_ciel)
        top_frame.pack(fill="x", side="top")
        app_name = tk.Label(top_frame, text="Speedy", font=("Arial", 55, "bold"), fg="#FF7F32", bg=blue_ciel)
        app_name.place(relx=0.5, rely=0.5, anchor="center")

        menu = ctk.CTkButton(
            top_frame,
            text="☰",
            font=("Arial", 25, "bold"),
            corner_radius=15,
            width=20,
            height=20,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            text_color="white",
            command=self.show_side_frame  # Référence à la méthode
        )
        menu.place(x=0, y=65)
        notif = ctk.CTkButton(
            top_frame,
            text="🔔 ",
            font=("Arial", 25, "bold"),
            corner_radius=15,
            width=20,
            height=20,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            text_color="white",
            command=self.shownotif  # Référence à la méthode
        )
        notif.place(x=44, y=63)

    def createMenuFrame(self):
        """Crée la barre latérale avec le contenu du menu."""
        # Exemple de contenu pour la side frame
        self.side_frame = tk.Frame(self, bg="white")
        self.side_frame.pack(fill="both", expand=True, side="left")

         # Création de la première colonne de boutons
        button1 = tk.Button(
            self.side_frame,
            text="➕ Ajouter un colis",
            font=("Arial", 28, "bold"),
            bg="white",
            fg=orange,
            relief="flat",
            command=self.ajcoli
        )
        button1.place(x=40,y=20)
        canvas1 = tk.Canvas(self.side_frame, width=650, height=1, bg="black")
        canvas1.place(x=0,y=100)

        button2 = tk.Button(
            self.side_frame,
            text="📦 Mes colis",
            font=("Arial", 28, "bold"),
            bg="white",
            fg=orange,
            relief="flat",
            command=self.gotohis
        )
        button2.place(x=40,y=120)
        canvas2 = tk.Canvas(self.side_frame, width=650, height=1, bg="black")
        canvas2.place(x=0,y=200)

        button3 = tk.Button(
            self.side_frame,
            text="🛋 Déménagement",
            font=("Arial", 28, "bold"),
            bg="white",
            fg=orange,
            relief="flat",
            command=self.godem
        )
        button3.place(x=800,y=20)
        

        # Création d'une ligne verticale entre les deux colonnes
        canvas_vert = tk.Canvas(self.side_frame, width=1, height=202, bg="black")
        canvas_vert.place(x=650,y=0)
        
        
        
        
        canvas3 = tk.Canvas(self.side_frame, width=710, height=1, bg="black")
        canvas3.place(x=651,y=100)

        
        canvas4 = tk.Canvas(self.side_frame, width=710, height=1, bg="black")
        canvas4.place(x=651,y=200)

        
       
        
        
        button8 = tk.Button(
            self.side_frame,
            text="👥 Procurer un ami(e)",
            font=("Arial", 28, "bold"),
            bg="white",
            fg=orange,
            relief="flat",
            command=self.allerproc
        )
        button8.place(x=800,y=120)
        rest = tk.Label(self.side_frame, text="Restons-connecté :    📧 speedyexpress026@gmail.com       📞+212578654291 ", font=("Arial", 24, "bold"), fg="Black",bg="white")
        rest.place(x=50,y=320)
        # Ajoutez ici le contenu de la side_frame (boutons, étiquettes, etc.)
        

    def update_background(self, event):
        """Mise à jour de l'image de fond lors du redimensionnement de la fenêtre."""
        if not self.background_image:
            return

        # Obtenez les dimensions du bottom_frame
        new_width = self.bottom_frame.winfo_width()
        new_height = self.bottom_frame.winfo_height()

        if new_width > 0 and new_height > 0:
            # Redimensionner l'image
            resized_image = self.background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Appliquer l'amélioration
            enhancer = ImageEnhance.Brightness(resized_image)
            enhanced_image = enhancer.enhance(0.7)

            # Convertir en PhotoImage
            self.background_photo = ImageTk.PhotoImage(enhanced_image)

            # Mettre à jour le label
            self.background_label.configure(image=self.background_photo)
            self.background_label.image = self.background_photo  # Préserver la référence

    def show_side_frame(self):
        """Affiche ou masque la barre latérale."""
        if self.side_frame.winfo_ismapped():
            # Si la side_frame est déjà affichée, la masquer et montrer la bottom_frame
            self.side_frame.pack_forget()
            self.bottom_frame.pack(fill="both", expand=True, side="top")
        else:
            # Sinon, montrer la side_frame et masquer la bottom_frame
            self.bottom_frame.pack_forget()
            self.side_frame.pack(fill="both", expand=True, side="top")
    def alleraccount(self):
        from account import Account
        self.controller.show_frame("Account")
    def allerproc(self):
        from procurationamis import Procami
        self.controller.show_frame("Procami")
        modifinf_frame = self.controller.frames["Procami"]
        modifinf_frame.insertent()
    def shownotif(self):
        from notification import notif
        self.controller.show_frame("notif")
    def godem(self):
        from demenagementsfinal2 import Demanagement
        self.controller.show_frame("Demanagement")
    def ajcoli(self):
        from creecoli import Colis
        self.controller.show_frame("Colis")
    def gomap(self):
        from GPSsuiviecolis import SuiviColis
        self.controller.show_frame("SuiviColis")
    def gotohis(self):
        from mescolis import HistoriqueColis
        self.controller.show_frame("HistoriqueColis")
    
        
        




        
        
       
        
        

# Lancer l'application
if __name__ == "__main__":
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    app.geometry("800x600")
    tracking_app = TrackingApp(app, app)
    tracking_app.pack(fill="both", expand=True)
    app.mainloop()





