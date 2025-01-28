from tkinter import *
import customtkinter as ctk
from datetime import datetime, date
from tkinter import *
import customtkinter as ctk
from datetime import datetime, date
import sqlite3
class ColisFenetre(ctk.CTkToplevel):
    def __init__(self, parent, colis_data):
        super().__init__(parent)
        self.geometry("600x500")
        self.title("Détails du colis")
        
        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        
        # En-tête
        header = ctk.CTkFrame(self, fg_color=self.blue_ciel, height=80)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="Détails de la livraison",
            font=("Arial", 24, "bold"),
            text_color=self.orange
        )
        title.pack(pady=20)

        # Contenu principal
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Date et Heure
        date_frame = ctk.CTkFrame(content, fg_color="transparent")
        date_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            date_frame,
            text=f"📅 Date: {colis_data['date'].strftime('%d/%m/%Y')}",
            font=("Arial", 18),
            text_color="black"
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            date_frame,
            text=f"🕒 Horaire: {colis_data['heure_debut']} - {colis_data['heure_fin']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(side="left", padx=20)

        # Séparateur
        self.create_separator(content)

        # Localisation
        location_frame = ctk.CTkFrame(content, fg_color="transparent")
        location_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            location_frame,
            text=f"🏙️ Ville: {colis_data['ville']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            location_frame,
            text=f"📍 Adresse: {colis_data['adresse']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(anchor="w", padx=20)

        # Séparateur
        self.create_separator(content)

        # Prix
        price_frame = ctk.CTkFrame(content, fg_color="transparent")
        price_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            price_frame,
            text=f"💰 Prix de livraison: {colis_data['prix']} DH",
            font=("Arial", 20, "bold"),
            text_color=self.orange
        ).pack(anchor="w", padx=20)

        # Séparateur
        self.create_separator(content)

        # Boutons
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)


        ctk.CTkButton(
            buttons_frame,
            text="Fermer",
            font=("Arial", 18),
            fg_color="grey",
            command=self.destroy,
            width=200
        ).pack( padx=20)

    def create_separator(self, parent):
        separator = ctk.CTkFrame(parent, height=2, fg_color="grey")
        separator.pack(fill="x", padx=20, pady=10)

    


   

class notif(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")

        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        self.bg_color = "#f5f5f5"

        # En-tête
        self.create_header()

        # Frame temps
        self.create_time_frame()

        # Frame principale scrollable pour les notifications
        self.framegrande = ctk.CTkScrollableFrame(self, width=900, height=600, corner_radius=3, fg_color=self.blue_ciel, border_width=5)
        self.framegrande.pack(fill="both", expand=True, padx=30, pady=10)
        from userclass import user_idg
        conn=sqlite3.connect("suivi_coli.db")
        c=conn.cursor()
        c.execute("select date_notif,contenu_notif,id_colis,horraire1,horraire2,date_estime from notification where id_user=?",(user_idg,))
        self.notifications=c.fetchall()
        for notif in self.notifications:
            print(notif)
        conn.commit()
        conn.close()
        
        
        self.display_notifications()

    def create_header(self):
        self.framenotif = ctk.CTkFrame(self, height=100, corner_radius=0, fg_color=self.blue_ciel)
        self.framenotif.pack(fill="x")
        
        back_button = ctk.CTkButton(
            self.framenotif, 
            text="⬅️ Retour",
            corner_radius=13,
            font=("Arial", 18, "bold"),
            fg_color=self.orange,
            command=self.go_back,
            width=100
        )
        back_button.pack(side="left", padx=20, pady=10)

        self.labelnotif = ctk.CTkLabel(
            self.framenotif,
            text="Notifications",
            text_color=self.orange,
            font=("Arial", 28, "bold")
        )
        self.labelnotif.pack(pady=20)

    def create_time_frame(self):
        self.frametemp = ctk.CTkFrame(self, height=50, corner_radius=10, fg_color="white")
        self.frametemp.pack(fill="x", padx=30, pady=10)

    def display_notifications(self):
        if not self.notifications:
            no_notif_label = ctk.CTkLabel(
                self.framegrande,
                text="Vous n'avez aucune notification",
                font=("Arial", 20, "bold"),
                text_color="black"
            )
            no_notif_label.pack(pady=50)
            return

        # Grouper les notifications par date
        notifications_by_date = {}
        for notif_data in self.notifications:
            date_key = notif_data["date"]
            if date_key not in notifications_by_date:
                notifications_by_date[date_key] = []
            notifications_by_date[date_key].append(notif_data)

        # Afficher les notifications groupées par date
        for notif_date in sorted(notifications_by_date.keys(), reverse=True):
            # Créer le label de date
            date_text = "Aujourd'hui" if notif_date == date.today() else notif_date.strftime("%d/%m/%Y")
            date_frame = ctk.CTkFrame(self.framegrande, fg_color="transparent")
            date_frame.pack(fill="x", pady=5)
            
            date_label = ctk.CTkLabel(
                date_frame,
                text=date_text,
                font=("Arial", 22, "bold"),
                text_color="black"
            )
            date_label.pack(anchor="w", padx=20)

            # Afficher toutes les notifications de cette date
            for notif_data in notifications_by_date[notif_date]:
                self.create_notification_card(notif_data)

    def create_notification_card(self, notif_data):
        # Frame principale de la notification
        card_frame = ctk.CTkFrame(
            self.framegrande,
            fg_color="white",
            corner_radius=10,
            border_width=2,
            border_color=self.blue_ciel
        )
        card_frame.pack(fill="x", padx=20, pady=5)

        # Frame gauche pour les informations principales
        left_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        # Titre de la notification
        ctk.CTkLabel(
            left_frame,
            text="📦 Disponible pour livrer ?",
            font=("Arial", 20, "bold"),
            text_color="black"
        ).pack(anchor="w")

        # Frame pour les détails (heure et prix)
        details_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=5)

        # Heure
        ctk.CTkLabel(
            details_frame,
            text=f"🕒 {notif_data['heure_debut']} - {notif_data['heure_fin']}",
            font=("Arial", 16),
            text_color="#12818d"
        ).pack(side="left", padx=10)

        # Prix
        ctk.CTkLabel(
            details_frame,
            text=f"💰 {notif_data['prix']} DH",
            font=("Arial", 16),
            text_color="#12818d"
        ).pack(side="left", padx=10)

        # Localisation
        location_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        location_frame.pack(fill="x")

        ctk.CTkLabel(
            location_frame,
            text=f"🏙️ {notif_data['ville']}",
            font=("Arial", 16),
            text_color=self.orange
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            location_frame,
            text=f"📍 {notif_data['adresse']}",
            font=("Arial", 16),
            text_color=self.orange
        ).pack(side="left", padx=10)

        # Bouton flèche à droite
        ctk.CTkButton(
            card_frame,
            text="➡️",
            font=("Arial", 24),
            fg_color="transparent",
            text_color=self.blue_ciel,
            width=50,
            command=lambda: self.open_colis_details(notif_data)
        ).pack(side="right", padx=15)

    def open_colis_details(self, colis_data):
        colis_fenetre = ColisFenetre(self, colis_data)
        colis_fenetre.focus() 

    def go_back(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def page_colis(self):
        print("Aller à la page d'informations de colis")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x800")
    notific = notif(app, app)
    notific.pack(fill="both", expand=True)
    app.mainloop()
