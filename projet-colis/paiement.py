from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import os

class Paiement(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")

        # Données d'exemple
        self.donnees_exemple = {
            "expediteur": {
                "nom": "Mohamed Alami",
                "adresse": "123 Rue Hassan II, Casablanca",
                "telephone": "0612345678",
                "email": "m.alami@email.com",
                "ville": "Casablanca"
            },
            "destinataire": {
                "nom": "Ahmed Benjelloun",
                "adresse": "45 Avenue FAR, Marrakech",
                "telephone": "0698765432",
                "email": "a.benjelloun@email.com",
                "ville": "Marrakech"
            },
            "colis": {
                "poids": 12.5,
                "dimension": "40x30x20",
                "articles": [
                    {"nom": "Livre", "description": "Manuel scolaire"},
                    {"nom": "Vêtements", "description": "2 chemises, 1 pantalon"}
                ]
            }
        }

        # Coordonnées des villes marocaines
        self.coords_villes = {
            "Casablanca": (33.5731, -7.5898),
            "Rabat": (34.0209, -6.8416),
            "Marrakech": (31.6295, -7.9811),
            "Fès": (34.0333, -5.0000),
            "Tanger": (35.7595, -5.8340),
            "Agadir": (30.4278, -9.5981),
            "Meknès": (33.8935, -5.5547),
            "Oujda": (34.6867, -1.9114),
            "Kenitra": (34.2610, -6.5802),
            "Tetouan": (35.5889, -5.3626),
            "El Jadida": (33.2316, -8.5007),
            "Safi": (32.2994, -9.2372),
            "Mohammedia": (33.6866, -7.3833),
            "Béni Mellal": (32.3373, -6.3498),
            "Nador": (35.1667, -2.9333)
        }

        # Tarifs
        self.prix_base = 50  # Prix de base en DH
        self.prix_par_kg = 5  # Prix par kg en DH
        self.prix_par_km = 0.5  # Prix par km en DH

        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"

        self.creer_en_tete()
        self.creer_corps()
        self.afficher_details()

    def creer_en_tete(self):
        self.frame_sup = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=self.blue_ciel)
        self.frame_sup.pack(fill="x", side="top")

        self.bouton_retour = ctk.CTkButton(
            self.frame_sup,
            text="◁ Retour",
            command=self.retour_page,
            font=("Helvetica", 14, "bold"),
            fg_color=self.blue_ciel,
            text_color="white",
            hover_color="#FFB84D"
        )
        self.bouton_retour.pack(side="left", padx=10, pady=10)

        self.label_titre = ctk.CTkLabel(
            self.frame_sup,
            text="Facture et Paiement",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500"
        )
        self.label_titre.pack(pady=(10, 20))

    def creer_corps(self):
        self.frame_principal = ctk.CTkScrollableFrame(self, fg_color="white")
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Création d'une frame principale pour les informations
        self.frame_info = ctk.CTkFrame(self.frame_principal, fg_color="#F0F8FF")
        self.frame_info.pack(fill="x", pady=10, padx=10)

        # Frame gauche pour expéditeur et colis
        self.frame_gauche = ctk.CTkFrame(self.frame_info, fg_color="transparent")
        self.frame_gauche.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame droite pour destinataire et articles
        self.frame_droite = ctk.CTkFrame(self.frame_info, fg_color="transparent")
        self.frame_droite.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Détails expéditeur
        self.frame_expediteur = self.creer_cadre_titre(self.frame_gauche, "Détails de l'expéditeur")
        self.label_exp = ctk.CTkLabel(
            self.frame_expediteur, 
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_exp.pack(pady=5, padx=10, anchor="w")

        # Détails colis
        self.frame_colis = self.creer_cadre_titre(self.frame_gauche, "Détails du colis")
        self.label_colis = ctk.CTkLabel(
            self.frame_colis,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_colis.pack(pady=5, padx=10, anchor="w")

        # Détails destinataire
        self.frame_destinataire = self.creer_cadre_titre(self.frame_droite, "Détails du destinataire")
        self.label_dest = ctk.CTkLabel(
            self.frame_destinataire,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_dest.pack(pady=5, padx=10, anchor="w")

        # Articles
        self.frame_articles = self.creer_cadre_titre(self.frame_droite, "Articles")
        self.label_articles = ctk.CTkLabel(
            self.frame_articles,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_articles.pack(pady=5, padx=10, anchor="w")

        # Frame pour les frais (en bas)
        self.frame_bas = ctk.CTkFrame(self.frame_principal, fg_color="#F0F8FF")
        self.frame_bas.pack(fill="x", pady=(20,10), padx=10)

        # Calcul des frais
        self.frame_frais = self.creer_cadre_titre(self.frame_bas, "Détails des frais")
        self.label_frais = ctk.CTkLabel(
            self.frame_frais,
            text="",
            justify="left",
            font=("Helvetica", 14, "bold")
        )
        self.label_frais.pack(pady=10, padx=10, anchor="w")

        # Boutons
        self.frame_boutons = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_boutons.pack(fill="x", pady=20)

        self.bouton_payer = ctk.CTkButton(
            self.frame_boutons,
            text="Générer La Facture",
            command=self.payer_et_generer_facture,
            font=("Helvetica", 20, "bold"),
            fg_color=self.orange,
            hover_color="green",
            height=50
        )
        self.bouton_payer.pack(side="right", padx=20)
    def calculer_distance(self, ville1, ville2):
        if ville1 in self.coords_villes and ville2 in self.coords_villes:
            lat1, lon1 = self.coords_villes[ville1]
            lat2, lon2 = self.coords_villes[ville2]
            
            R = 6371  # Rayon de la Terre en km
            
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            
            return round(distance, 2)
        return 0

    def calculer_prix(self):
        poids = self.donnees_exemple["colis"]["poids"]
        distance = self.calculer_distance(
            self.donnees_exemple["expediteur"]["ville"],
            self.donnees_exemple["destinataire"]["ville"]
        )
        
        prix_poids = poids * self.prix_par_kg
        prix_distance = distance * self.prix_par_km
        total = self.prix_base + prix_poids + prix_distance
        
        return {
            "prix_base": self.prix_base,
            "prix_poids": round(prix_poids, 2),
            "prix_distance": round(prix_distance, 2),
            "total": round(total, 2),
            "distance": distance
        }

    def afficher_details(self):
        # Afficher détails expéditeur
        exp = self.donnees_exemple["expediteur"]
        self.label_exp.configure(text=(
            f"Nom: {exp['nom']}\n"
            f"Adresse: {exp['adresse']}\n"
            f"Téléphone: {exp['telephone']}\n"
            f"Email: {exp['email']}\n"
            f"Ville: {exp['ville']}"
        ))

        # Afficher détails destinataire
        dest = self.donnees_exemple["destinataire"]
        self.label_dest.configure(text=(
            f"Nom: {dest['nom']}\n"
            f"Adresse: {dest['adresse']}\n"
            f"Téléphone: {dest['telephone']}\n"
            f"Email: {dest['email']}\n"
            f"Ville: {dest['ville']}"
        ))

        # Afficher détails colis
        colis = self.donnees_exemple["colis"]
        self.label_colis.configure(text=(
            f"Poids: {colis['poids']} kg\n"
            f"Dimensions: {colis['dimension']}"
        ))

        # Afficher articles
        articles_text = "Articles inclus:\n"
        for article in colis['articles']:
            articles_text += f"- {article['nom']}: {article['description']}\n"
        self.label_articles.configure(text=articles_text)

        # Calculer et afficher les frais
        tarifs = self.calculer_prix()
        self.label_frais.configure(text=(
            f"Prix de base: {tarifs['prix_base']} DH\n"
            f"Frais de poids ({self.prix_par_kg} DH/kg × {colis['poids']} kg): {tarifs['prix_poids']} DH\n"
            f"Distance: {tarifs['distance']} km\n"
            f"Frais de distance ({self.prix_par_km} DH/km): {tarifs['prix_distance']} DH\n"
            f"Total: {tarifs['total']} DH"
        ))

    def generer_facture(self):
        now = datetime.now()
        nom_fichier = f"facture_speedy_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(nom_fichier, pagesize=A4)
        try:
        # Chemin vers votre logo
            logo_path = "logo.ico"  # Ajustez le chemin selon votre structure
        # Position et taille du logo
            c.drawImage(logo_path, 40, 750, width=100, height=80, preserveAspectRatio=True)
        except:
        # Si le logo n'est pas trouvé, on garde le rectangle vide
            c.rect(40, 750, 100, 80, stroke=1, fill=0)
        
        # Couleurs
        bleu_clair = colors.HexColor('#B8D7E9') 
        bleu_fonce = colors.HexColor('#2C5282')
        gris = colors.HexColor('#718096')

        # Marges
        marge_gauche = 40
        marge_droite = 550
        largeur_utile = marge_droite - marge_gauche

        # En-tête - Logo et informations société
        
 # Espace logo
        
        # Informations expéditeur
        c.setFillColor(bleu_fonce)
        c.setFont("Helvetica-Bold", 17)
        c.drawString(150, 800, "SPEEDY LIVRAISON")
        
        exp = self.donnees_exemple["expediteur"]
        c.setFillColor(gris)
        c.setFont("Helvetica", 10)
        c.drawString(150, 785, "Service de livraison express")
        c.drawString(150, 770, f"Nom: {exp['nom']}")
        c.drawString(150, 755, f"Adresse: {exp['adresse']}")
        c.drawString(150, 740, f"Tel: {exp['telephone']}")
        c.drawString(150, 725, f"Email: {exp['email']}")
        c.drawString(150, 710, f"Ville: {exp['ville']}")

        # Cadre destinataire
        c.rect(350, 730, 200, 100, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(bleu_fonce)
        c.drawString(360, 810, "DESTINATAIRE")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 9)
        dest = self.donnees_exemple["destinataire"]
        c.drawString(360, 790, f"Nom: {dest['nom']}")
        c.drawString(360, 775, f"Adresse: {dest['adresse']}")
        c.drawString(360, 760, f"Ville: {dest['ville']}")
        c.drawString(360, 745, f"Tel: {dest['telephone']}")
        c.drawString(360, 730, f"Email: {dest['email']}")

        # Numéro de facture et date
        c.setFillColor(bleu_fonce)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(marge_gauche, 650, f"FACTURE N° {now.strftime('%Y%m%d%H%M')}")
        c.setFont("Helvetica", 10)
        c.drawString(marge_droite - 150, 650, f"Date: {now.strftime('%d/%m/%Y')}")

        # Tableau 1 - Articles
        y = 580
        c.setFillColor(bleu_clair)
        c.rect(marge_gauche, y, largeur_utile, 20, stroke=1, fill=1)
        
        c.setFillColor(bleu_fonce)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(marge_gauche + 5, y+5, "ARTICLES ET DESCRIPTION")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 9)
        y -= 25
        
        articles = self.donnees_exemple["colis"]["articles"]
        for article in articles:
            c.drawString(marge_gauche + 5, y, f"• {article['nom']}: {article['description']}")
            y -= 20

        # Tableau 2 - Détails colis et tarifs
        y -= 20
        c.setFillColor(bleu_clair)
        c.rect(marge_gauche, y, largeur_utile, 20, stroke=1, fill=1)
        
        c.setFillColor(bleu_fonce)
        c.setFont("Helvetica-Bold", 10)
        colonnes = [
            ("DÉTAILS", 250),
            ("UNITÉ", 60),
            ("QUANTITÉ", 60),
            ("P.U HT", 80),
            ("TOTAL HT", 80)
        ]
        
        x = marge_gauche + 5
        for titre, largeur in colonnes:
            c.drawString(x, y+5, titre)
            x += largeur

        # Contenu détails colis
        c.setFillColor(gris)
        c.setFont("Helvetica", 9)
        y -= 25
        
        tarifs = self.calculer_prix()
        colis = self.donnees_exemple["colis"]
        
        details = [
            {"detail": "Poids du colis", "unite": "kg", "qte": colis["poids"], "pu": self.prix_par_kg},
            {"detail": "Distance de livraison", "unite": "km", "qte": tarifs["distance"], "pu": self.prix_par_km},
            {"detail": "Frais de base", "unite": "forfait", "qte": 1, "pu": self.prix_base}
        ]

        for detail in details:
            x = marge_gauche + 5
            c.drawString(x, y, detail["detail"])
            x += 250
            c.drawString(x, y, detail["unite"])
            x += 60
            c.drawRightString(x+30, y, str(detail["qte"]))
            x += 60
            c.drawRightString(x+50, y, f"{detail['pu']:.2f} €")
            x += 80
            total = detail["qte"] * detail["pu"]
            c.drawRightString(x+50, y, f"{total:.2f} €")
            y -= 20

        # Récapitulatif des prix
        y = 300
        c.setFillColor(bleu_clair)
        c.rect(350, y-100, 200, 100, stroke=1, fill=0)
        
        c.setFillColor(bleu_fonce)
        c.setFont("Helvetica-Bold", 10)
        recap = [
            ("TOTAL HT", f"{tarifs['total']:.2f} €"),
            ("TVA 20%", f"{tarifs['total']*0.2:.2f} €"),
            ("TOTAL TTC", f"{tarifs['total']*1.2:.2f} €")
        ]
        
        y_recap = y - 20
        for label, montant in recap:
            c.drawString(360, y_recap, label)
            c.drawRightString(530, y_recap, montant)
            y_recap -= 15

        # Conditions et politique
        y = 150
        c.setFont("Helvetica-Bold", 9)
        c.drawString(marge_gauche, y, "CONDITIONS DE LIVRAISON ET POLITIQUE")
        c.setFont("Helvetica", 8)
        conditions = [
            "• Délai de livraison estimé: 24-48h selon la destination",
            "• Les prix incluent l'assurance de base du colis",
            "• Paiement à la déposition des colis",
            "• En cas de dommages, contactez notre service client sous 48h"
        ]
        
        for condition in conditions:
            y -= 15
            c.drawString(marge_gauche, y, condition)

        # Mentions légales
        c.setFont("Helvetica", 7)
        c.drawString(marge_gauche, 50, "Conformément aux conditions générales de vente disponibles sur notre site web")
        c.drawString(marge_gauche, 40, "SPEEDY LIVRAISON - SIRET: 123 456 789 00000 - TVA: FR 12 345 678 900")
        
        c.save()
        return nom_fichier

    def payer_et_generer_facture(self):
        try:
            nom_fichier = self.generer_facture()
            messagebox.showinfo("Succès", 
                              f"Paiement effectué avec succès!\n"
                              f"La facture a été générée: {nom_fichier}")
            
        except Exception as e:
            messagebox.showerror("Erreur", 
                               f"Une erreur est survenue lors de la génération de la facture:\n{str(e)}")

    def retour_page(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def creer_cadre_titre(self, parent, titre):
        frame = ctk.CTkFrame(parent, fg_color=self.blue_ciel)
        frame.pack(fill="x", padx=20, pady=10)
        
        label_titre = ctk.CTkLabel(
            frame, 
            text=titre, 
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        label_titre.pack(anchor="w", padx=5, pady=5)
        
        return frame

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x900")
    app.title("Speedy - Page de paiement")
    paiement_page = Paiement(app, app)
    paiement_page.pack(fill="both", expand=True)
    app.mainloop()
