import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox
import csv

class HistoriqueColis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Définition des couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        self.blanc = "white"

        # Initialisation de la base de données
        self.conn = sqlite3.connect('colis_database.db')
        self.cursor = self.conn.cursor()
        self.creer_tables()
        
        # Configuration de l'interface
        self.setup_interface()

    def creer_tables(self):
        # Table des colis
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS colis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_colis TEXT UNIQUE NOT NULL,
            date_creation DATE NOT NULL,
            expediteur_id INTEGER,
            destinataire_id INTEGER,
            statut TEXT NOT NULL,
            lieu_actuel TEXT,
            description TEXT,
            FOREIGN KEY (expediteur_id) REFERENCES utilisateurs(id),
            FOREIGN KEY (destinataire_id) REFERENCES utilisateurs(id)
        )
        ''')

        # Table des utilisateurs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE,
            telephone TEXT,
            adresse TEXT
        )
        ''')

        # Table de l'historique des mouvements
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS historique_mouvements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colis_id INTEGER,
            date_mouvement DATETIME NOT NULL,
            ancien_statut TEXT,
            nouveau_statut TEXT,
            ancien_lieu TEXT,
            nouveau_lieu TEXT,
            commentaire TEXT,
            FOREIGN KEY (colis_id) REFERENCES colis(id)
        )
        ''')
        self.conn.commit()

    def setup_interface(self):
        # Frame principale
        self.main_frame = ctk.CTkFrame(self, fg_color=self.blanc)
        self.main_frame.pack(fill="both", expand=True)

        # Frame supérieure
        self.frame_sup = ctk.CTkFrame(self.main_frame, height=100, fg_color=self.blue_ciel)
        self.frame_sup.pack(fill="x")
        self.back_button = ctk.CTkButton(self.frame_sup, text="◁ Retour", command=self.revenir_page,
                                        font=("Helvetica", 14, "bold"), corner_radius=10, fg_color=self.orange,
                                        text_color="white", hover_color="#FFB84D")
        self.back_button.pack(side="left",pady=20, padx=10)
        # Titre
        self.titre = ctk.CTkLabel(
            self.frame_sup,
            text="Mes Colis",
            font=("Helvetica", 40, "bold"),
            text_color=self.orange
        )
        self.titre.pack(side="top",pady =20)
        # Frame de filtres
        self.frame_filtres = ctk.CTkFrame(self.main_frame, fg_color=self.blanc)
        self.frame_filtres.pack(fill="x", padx=20, pady=10)

        # Barre de recherche
        self.recherche = ctk.CTkEntry(
            self.frame_filtres,
            placeholder_text=" 🔍 Rechercher un colis...",
            width=300,
            height=35,
            font=("Helvetica", 15,"bold")
        )
        self.recherche.pack(side="left", padx=10, pady=10)

        # Filtre de statut
        self.statut_var = ctk.StringVar(value="Tous les statuts")
        self.filtre_statut = ctk.CTkOptionMenu(
            self.frame_filtres,
            values=["Tous les statuts", "En transit", "Livré", "En attente"],
            variable=self.statut_var,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.filtre_statut.pack(side="left", padx=10)

        # Boutons
        self.bouton_rechercher = ctk.CTkButton(
            self.frame_filtres,
            text="🔍 Rechercher",
            command=self.rechercher,
            fg_color=self.orange,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_rechercher.pack(side="left", padx=5)

        self.bouton_actualiser = ctk.CTkButton(
            self.frame_filtres,
            text="🔄 Actualiser",
            command=self.actualiser_donnees,
            fg_color=self.orange,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_actualiser.pack(side="left", padx=5)

        self.bouton_exporter = ctk.CTkButton(
            self.frame_filtres,
            text="📥 Exporter CSV",
            command=self.exporter_csv,
            fg_color=self.blue_ciel,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_exporter.pack(side="left", padx=5)

        # Frame pour le tableau
        self.frame_tableau = ctk.CTkFrame(self.main_frame, fg_color=self.blanc)
        self.frame_tableau.pack(fill="both", expand=True, padx=20, pady=10)

        # Tableau
        colonnes = ('Numéro', 'Date', 'Expéditeur', 'Destinataire', 'Statut', 'Lieu actuel')
        self.tableau = ttk.Treeview(self.frame_tableau, columns=colonnes, show='headings')
        
        # Configuration des colonnes
        for col in colonnes:
            self.tableau.heading(col, text=col, command=lambda c=col: self.trier_tableau(c))
            self.tableau.column(col, width=150, anchor='center')

        # Style du tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 15, 'bold'))
        style.configure("Treeview", font=('Helvetica', 15), rowheight=30)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tableau, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tableau.pack(fill="both", expand=True)

        # Événements du tableau
        self.tableau.bind("<Button-3>", self.afficher_menu_contextuel)
        self.tableau.bind("<Double-1>", self.afficher_details_selection)

        # Frame statistiques
        self.frame_stats = ctk.CTkFrame(self.main_frame, height=100, fg_color=self.blue_ciel)
        self.frame_stats.pack(fill="x", side="bottom")

        # Charger les données initiales
        self.actualiser_donnees()

    def rechercher(self):
        terme = self.recherche.get()
        statut = self.statut_var.get()
        
        # Effacer le tableau actuel
        for item in self.tableau.get_children():
            self.tableau.delete(item)

        # Exécuter la recherche dans la base de données
        query = '''
        SELECT c.numero_colis, c.date_creation, 
               u1.nom || ' ' || u1.prenom as expediteur,
               u2.nom || ' ' || u2.prenom as destinataire,
               c.statut, c.lieu_actuel
        FROM colis c
        LEFT JOIN utilisateurs u1 ON c.expediteur_id = u1.id
        LEFT JOIN utilisateurs u2 ON c.destinataire_id = u2.id
        WHERE 1=1
        '''
        params = []

        if terme:
            query += ''' AND (c.numero_colis LIKE ? OR 
                            u1.nom LIKE ? OR 
                            u2.nom LIKE ? OR 
                            c.lieu_actuel LIKE ?)'''
            terme = f"%{terme}%"
            params.extend([terme, terme, terme, terme])

        if statut != "Tous les statuts":
            query += " AND c.statut = ?"
            params.append(statut)

        self.cursor.execute(query, params)
        resultats = self.cursor.fetchall()

        for resultat in resultats:
            self.tableau.insert('', 'end', values=resultat)

    def actualiser_donnees(self):
        # Effacer le tableau actuel
        for item in self.tableau.get_children():
            self.tableau.delete(item)

        # Récupérer toutes les données
        self.cursor.execute('''
        SELECT c.numero_colis, c.date_creation, 
               u1.nom || ' ' || u1.prenom as expediteur,
               u2.nom || ' ' || u2.prenom as destinataire,
               c.statut, c.lieu_actuel
        FROM colis c
        LEFT JOIN utilisateurs u1 ON c.expediteur_id = u1.id
        LEFT JOIN utilisateurs u2 ON c.destinataire_id = u2.id
        ''')
        resultats = self.cursor.fetchall()

        for resultat in resultats:
            self.tableau.insert('', 'end', values=resultat)

        self.actualiser_statistiques()

    def actualiser_statistiques(self):
     self.cursor.execute('''
        SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN statut = 'En transit' THEN 1 ELSE 0 END) as en_transit,
        SUM(CASE WHEN statut = 'Livré' THEN 1 ELSE 0 END) as livres,
        SUM(CASE WHEN statut = 'En attente' THEN 1 ELSE 0 END) as en_attente
        FROM colis
        ''')
     total, en_transit, livres, en_attente = self.cursor.fetchone()

    # Configuration des statistiques avec icônes et couleurs
     stats = [
        {
            "titre": "Total des colis",
            "valeur": str(total or 0),
            "icone": "📦",
            "couleur": "#FF7F32"  # Orange
        },
        {
            "titre": "En transit",
            "valeur": str(en_transit or 0),
            "icone": "🚚",
            "couleur": "#4CAF50"  # Vert
        },
        {
            "titre": "Livrés",
            "valeur": str(livres or 0),
            "icone": "✅",
            "couleur": "#2196F3"  # Bleu
        },
        {
            "titre": "En attente",
            "valeur": str(en_attente or 0),
            "icone": "⏳",
            "couleur": "#FFC107"  # Jaune
        }
     ]

    # Supprimer les anciens widgets
     for widget in self.frame_stats.winfo_children():
        widget.destroy()

    # Créer les cartes de statistiques
     for i, stat in enumerate(stats):
        # Frame pour chaque carte
        carte = ctk.CTkFrame(
            self.frame_stats,
            width=250,
            height=80,
            fg_color="white",
            corner_radius=10
        )
        carte.pack(side="left", padx=20, pady=10)
        carte.pack_propagate(False)  # Maintenir la taille fixe

        # Frame pour l'icône
        icon_frame = ctk.CTkFrame(
            carte,
            width=50,
            height=50,
            fg_color=stat["couleur"],
            corner_radius=25
        )
        icon_frame.place(x=20, y=15)

        # Icône
        ctk.CTkLabel(
            icon_frame,
            text=stat["icone"],
            font=("Helvetica", 20),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        ctk.CTkLabel(
            carte,
            text=stat["titre"],
            font=("Helvetica", 14),
            text_color="gray"
        ).place(x=80, y=10)

        # Valeur
        ctk.CTkLabel(
            carte,
            text=stat["valeur"],
            font=("Helvetica", 25, "bold"),
            text_color=stat["couleur"]
        ).place(x=80, y=35)

    # Ajuster la hauteur de la frame des statistiques
     self.frame_stats.configure(height=100)
    #########################################
    def revenir_page(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")
    #########################################
    def exporter_csv(self):
     try:
        import os
        from datetime import datetime
        
        # Créer un nom de fichier avec la date et l'heure
        nom_fichier = f"historique_colis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        chemin_fichier = os.path.abspath(nom_fichier)
        
        # Export en CSV
        with open(chemin_fichier, 'w', newline='', encoding='utf-8-sig') as fichier:
            writer = csv.writer(fichier, delimiter=';')
            
            # En-têtes
            colonnes = ['Numéro', 'Date', 'Expéditeur', 'Destinataire', 'Statut', 'Lieu actuel']
            writer.writerow(colonnes)
            
            # Données
            for item in self.tableau.get_children():
                writer.writerow(self.tableau.item(item)["values"])

        # Ouvrir avec Excel
        try:
            if os.name == 'nt':  # Windows
                os.system(f'start excel "{chemin_fichier}"')
            
            messagebox.showinfo("Succès", f"Export CSV réussi!\nFichier: {nom_fichier}")
        except Exception as e:
            messagebox.showinfo("Information", 
                              f"Export CSV réussi!\nFichier: {nom_fichier}\n"
                              f"Le fichier n'a pas pu être ouvert automatiquement: {str(e)}")
            
     except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def afficher_menu_contextuel(self, event):
        item = self.tableau.identify_row(event.y)
        if item:
            self.tableau.selection_set(item)
            menu = ctk.CTkMenu(self)
            menu.add_command(label="Voir détails", command=self.afficher_details_selection)
            menu.add_command(label="Modifier statut", command=self.modifier_statut)
            menu.add_separator()
            menu.add_command(label="Supprimer", command=self.supprimer_selection)
            menu.post(event.x_root, event.y_root)

    def afficher_details_selection(self, event=None):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un colis")
            return

        item = selection[0]
        valeurs = self.tableau.item(item)['values']
        
        details = f"Détails du colis:\n\n"
        details += f"Numéro: {valeurs[0]}\n"
        details += f"Date: {valeurs[1]}\n"
        details += f"Expéditeur: {valeurs[2]}\n"
        details += f"Destinataire: {valeurs[3]}\n"
        details += f"Statut: {valeurs[4]}\n"
        details += f"Lieu actuel: {valeurs[5]}"
        
        messagebox.showinfo("Détails du colis", details)

    def modifier_statut(self):
        selection = self.tableau.selection()
        if not selection:
            return

        item = selection[0]
        valeurs = self.tableau.item(item)['values']

        # Création d'une nouvelle fenêtre pour la modification
        fenetre_modif = ctk.CTkToplevel(self)
        fenetre_modif.title(f"Modifier le statut - Colis {valeurs[0]}")
        fenetre_modif.geometry("400x300")

        frame_modif = ctk.CTkFrame(fenetre_modif)
        frame_modif.pack(fill="both", expand=True, padx=20, pady=20)

        statut_var = ctk.StringVar(value=valeurs[4])
        lieu_var = ctk.StringVar(value=valeurs[5])

        ctk.CTkLabel(frame_modif, text="Nouveau statut:").pack(pady=5)
        statut_menu = ctk.CTkOptionMenu(
            frame_modif,
            values=["En transit", "Livré", "En attente"],
            variable=statut_var
        )
        statut_menu.pack(pady=5)

        ctk.CTkLabel(frame_modif, text="Nouveau lieu:").pack(pady=5)
        lieu_entry = ctk.CTkEntry(frame_modif, textvariable=lieu_var)
        lieu_entry.pack(pady=5)

        def sauvegarder():
            nouveau_statut = statut_var.get()
            nouveau_lieu = lieu_entry.get()
            
            try:
                self.cursor.execute('''
                UPDATE colis 
                SET statut = ?, lieu_actuel = ? 
                WHERE numero_colis = ?
                ''', (nouveau_statut, nouveau_lieu, valeurs[0]))
                self.conn.commit()
                
                self.tableau.set(item, "Statut", nouveau_statut)
                self.tableau.set(item, "Lieu actuel", nouveau_lieu)
                
                fenetre_modif.destroy()
                self.actualiser_statistiques()
                messagebox.showinfo("Succès", "Statut mis à jour avec succès!")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {str(e)}")

        ctk.CTkButton(
            frame_modif,
            text="Sauvegarder",
            command=sauvegarder,
            fg_color=self.orange
        ).pack(pady=10)

    def supprimer_selection(self):
        selection = self.tableau.selection()
        if not selection:
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce colis ?"):
            item = selection[0]
            valeurs = self.tableau.item(item)['values']
            
            try:
                self.cursor.execute("DELETE FROM colis WHERE numero_colis = ?", (valeurs[0],))
                self.conn.commit()
                self.tableau.delete(item)
                self.actualiser_statistiques()
                messagebox.showinfo("Succès", "Colis supprimé avec succès!")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

    def trier_tableau(self, colonne):
        donnees = []
        for item in self.tableau.get_children():
            valeurs = self.tableau.item(item)['values']
            donnees.append(valeurs)

        colonne_index = list(self.tableau['columns']).index(colonne)
        donnees.sort(key=lambda x: x[colonne_index], reverse=hasattr(self, 'dernier_tri') and self.dernier_tri == colonne)
        self.dernier_tri = colonne if not hasattr(self, 'dernier_tri') or self.dernier_tri != colonne else None

        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for item in donnees:
            self.tableau.insert('', 'end', values=item)

    """def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()"""

if __name__ == "__main__":
    
    app = ctk.CTk()  
    login_page = HistoriqueColis(app, app)
    login_page.pack(fill="both", expand=True)
    app.mainloop()
     












