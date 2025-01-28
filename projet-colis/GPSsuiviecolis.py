import tkinter as tk
from tkinter import messagebox
import tkintermapview
import customtkinter as ctk
from PIL import Image, ImageTk
import time
import sqlite3

class SuiviColis(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        self.dark_blue = "#87CEFA"

        # Header élégant
        self.header_frame = ctk.CTkFrame(self, height=100, fg_color=self.dark_blue)
        self.header_frame.pack(fill="x")

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="◁",
            font=("Helvetica", 24, "bold"),
            width=50,
            corner_radius=25,
            fg_color="transparent",
            text_color="white",
            hover_color=self.orange,
            command=self.revenir_page
        )
        self.back_button.pack(side="left", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Suivi de Colis",
            font=("Helvetica", 36, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)

        # Corps principal avec ombre
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=20,
            border_width=2,
            border_color=self.blue_ciel
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Zone de recherche stylisée
        self.search_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#F8F9FA",
            corner_radius=15
        )
        self.search_frame.pack(fill="x", padx=30, pady=20)

        self.track_label = ctk.CTkLabel(
            self.search_frame,
            text="Numéro de Suivi",
            font=("Helvetica", 18),
            text_color=self.dark_blue
        )
        self.track_label.pack(pady=(10, 5))

        self.track_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Entrez votre numéro de suivi...",
            font=("Arial", 16),
            width=400,
            height=45,
            corner_radius=10,
            border_color=self.blue_ciel
        )
        self.track_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Rechercher",
            font=("Helvetica", 16, "bold"),
            fg_color=self.orange,
            hover_color=self.dark_blue,
            corner_radius=10,
            height=40,
            command=self.get_tracking_info
        )
        self.search_button.pack(pady=15)

        # Panneau d'informations
        self.info_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#F8F9FA",
            corner_radius=15
        )
        self.info_frame.pack(fill="x", padx=30, pady=10)

        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="Statut : En attente...",
            font=("Helvetica", 16),
            text_color=self.dark_blue
        )
        self.status_label.pack(pady=5)

        self.location_label = ctk.CTkLabel(
            self.info_frame,
            text="Position : --",
            font=("Helvetica", 16),
            text_color=self.dark_blue
        )
        self.location_label.pack(pady=5)

        # Carte interactive
        self.map_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=15
        )
        self.map_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.map_widget = tkintermapview.TkinterMapView(
            self.map_frame,
            width=800,
            height=400,
            corner_radius=15
        )
        self.map_widget.pack(fill="both", expand=True, padx=5, pady=5)

        # Barre de navigation
        self.nav_frame = ctk.CTkFrame(
            self,
            height=60,
            fg_color=self.dark_blue,
            corner_radius=0
        )
        self.nav_frame.pack(fill="x", side="bottom")

        # Boutons de navigation
        nav_buttons = [
            ("🏠", "Accueil"),
            ("📦", "Colis"),
            ("👤", "Compte")
        ]

        for icon, text in nav_buttons:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=f"{icon}\n{text}",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color=self.orange,
                corner_radius=10,
                width=100
            )
            btn.pack(side="left", expand=True, pady=5)

        # Destinations simulées
        """self.destinations = {
            "123456": {
                "current": (33.2563, -8.5091),  # Position actuelle
                "start": (33.5731, -7.5898),    # Point de départ
                "end": (34.0209, -6.8416),      # Destination finale (Rabat)
                "status": "En cours de livraison"
            }
        }"""
        # Initialiser la carte
        self.initial_map_position()

    def revenir_page(self):
        """Retour à la page précédente"""
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def initial_map_position(self):
        """Position initiale de la carte sur le Maroc"""
        self.map_widget.set_position(31.7917, -7.0926)
        self.map_widget.set_zoom(6)

    def get_tracking_info(self):
        """Gestion du suivi de colis"""
        tracking_number = self.track_entry.get().strip()
    
        if not tracking_number:
            messagebox.showerror(
                "Erreur",
                "Veuillez entrer un numéro de suivi."
            )
            return
    
        try:
            conn = sqlite3.connect("C:\\Users\\Utilisateur\\Desktop\\SSSS.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id_colis, etatlivrs,
                       x, y,
                       posit_depart_lat, posit_depart_lon,
                       posit_desti_lat, posit_desti_lon
                FROM colis
                WHERE id_colis = ?
                ''', (tracking_number,))
        
            result = cursor.fetchone()
        
            if result:
                # Extraction des positions
                current_pos = (result[2], result[3])
                start_pos = (result[4], result[5])
                end_pos = (result[6], result[7])
            
                # Mise à jour des labels d'information
                self.status_label.configure(text=f"Statut: {result[1]}")
                self.location_label.configure(
                    text=f"Position actuelle: {current_pos[0]:.4f}, {current_pos[1]:.4f}"
                )
            
                # Affichage sur la carte
                self.display_route(current_pos, start_pos, end_pos)
            
            else:
                messagebox.showerror(
                    "Erreur",
                    "Numéro de colis non trouvé dans la base de données."
                )
                # Réinitialisation
                self.status_label.configure(text="Statut : En attente...")
                self.location_label.configure(text="Position : --")
                self.initial_map_position()
            
        except sqlite3.Error as e:
            messagebox.showerror(
                "Erreur",
                f"Erreur lors de la recherche: {str(e)}"
            )
        finally:
            if 'conn' in locals():
                conn.close()

    def display_route(self, current_pos, start_pos, end_pos):
        """Affichage des positions et de la route"""
        self.map_widget.delete_all_path()
        self.map_widget.delete_all_marker()
        
        # Centrer la carte
        center_lat = (current_pos[0] + end_pos[0]) / 2
        center_lon = (current_pos[1] + end_pos[1]) / 2
        self.map_widget.set_position(center_lat, center_lon)
        self.map_widget.set_zoom(9)

        # Marqueurs
        self.map_widget.set_marker(
            current_pos[0],
            current_pos[1],
            text="Position Actuelle",
            text_color="white",
            marker_color_circle="#FF0000",
            marker_color_outside="#8B0000"
        )
        
        self.map_widget.set_marker(
            start_pos[0],
            start_pos[1],
            text="Point de Départ",
            text_color="white",
            marker_color_circle="#008000",
            marker_color_outside="#006400"
        )

        self.map_widget.set_marker(
            end_pos[0],
            end_pos[1],
            text="Destination",
            text_color="white",
            marker_color_circle="#0000FF",
            marker_color_outside="#00008B"
        )

        # Routes
        self.map_widget.set_path([current_pos, start_pos, end_pos])
    
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("900x800")
    app.title("Suivi de Colis")
    tracking_app = SuiviColis(app, app)
    tracking_app.pack(fill="both", expand=True)
    app.mainloop()


