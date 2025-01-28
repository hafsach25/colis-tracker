from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3


class Colis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")  

        
        orange = "#FF7F32"  
        blue_ciel = "#87CEFA"  

        
        self.selected_ville = ctk.StringVar(self)
        self.selected_services = ctk.StringVar(value="cartons")
        self.selected_transp = ctk.StringVar(value="camion")

        
        self.framesup = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=blue_ciel)
        self.framesup.pack(fill="x", side="top")

        self.back_button = ctk.CTkButton(
            self.framesup,
            text="◁ Retour",
            command=self.revenir_page,
            font=("Helvetica", 14, "bold"),
            corner_radius=10,
            fg_color=blue_ciel,
            text_color="white",
            hover_color="#FFB84D",
        )
        self.back_button.pack(side="left", padx=10, pady=10)

        self.speedy_label = ctk.CTkLabel(
            self.framesup,
            text="Ajouter un Coli",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500",
        )
        self.speedy_label.pack(pady=(10, 20))

        
        self.bframe = ctk.CTkScrollableFrame(self, fg_color="white")
        self.bframe.pack(fill="both", expand=True, side="top")

               
        self.labelpetit = ctk.CTkLabel(
                self.bframe,
                text="Envoyer vos colis en toute simplicité 😊!",
                font=("Arial", 25, "bold"),
                text_color=orange,
        )
        self.labelpetit.pack(pady=10)

      
        self.label2 = ctk.CTkLabel(self.bframe, text="Détails du Coli :", font=("Arial", 27, "bold"))
        self.label2.pack(pady=10)

  
        frame_info_demenagement = self.create_titled_frame(self.bframe, "Informations sur les articles", blue_ciel)
        self.articles = []  

       
        tk.Label(frame_info_demenagement, text="Nom de l'article:").pack(pady=5)
        self.article_name_entry = tk.Entry(frame_info_demenagement, width=40)
        self.article_name_entry.pack(pady=5)

        tk.Label(frame_info_demenagement, text="Description de l'article:").pack(pady=5)
        self.article_description_entry = tk.Entry(frame_info_demenagement, width=40)
        self.article_description_entry.pack(pady=5)

        self.add_button = tk.Button(frame_info_demenagement, text="Ajouter", command=self.add_article)
        self.add_button.pack(pady=10)

        self.article_listbox = tk.Listbox(frame_info_demenagement, width=60, height=10)
        self.article_listbox.pack(pady=10)

       

    

       
        frame_date_heure = self.create_titled_frame(self.bframe, "Informations du colis:", blue_ciel)

        ctk.CTkLabel(frame_date_heure, text="poids en KG", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.date_entry = ctk.CTkEntry(frame_date_heure, placeholder_text="poids", font=("Helvetica", 12))
        self.date_entry.pack(anchor="w",pady=4,padx=4)

        ctk.CTkLabel(frame_date_heure, text="Dimension (999x999cm):", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        
        self.time_combo = ctk.CTkEntry(frame_date_heure, placeholder_text="Dimension", font=("Helvetica", 12))
        self.time_combo.pack(anchor="w",pady=4,padx=4)

        
        frame_biens = self.create_titled_frame(self.bframe, "Informations de déstinataire :", blue_ciel)
        villes_maroc = [
    "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Meknès", 
    "Oujda", "Kenitra", "Tetouan", "Safi", "El Jadida", "Nador", "Beni Mellal", 
    "Mohammedia", "Taza", "Khouribga", "Settat", "Errachidia", "Larache", 
    "Khemisset", "Ouarzazate", "Tiznit", "Tan-Tan", "Guelmim", "Ifrane", 
    "Asilah", "Chefchaouen", "Al Hoceima", "Taroudant", "Oued Zem", 
    "Azrou", "Sidi Kacem", "Sidi Slimane", "Boujdour", "Laâyoune", "Dakhla"
                 ]

        self.name_label = ctk.CTkLabel(frame_biens, text="Nom :",font=("Helvetica", 12,"bold"))
        self.name_label.pack(anchor="w",pady=4,padx=4)
        self.name_entry = ctk.CTkEntry(frame_biens, placeholder_text="Entrez votre nom ", width=300,corner_radius=0)
        self.name_entry.pack(anchor="w",pady=4,padx=4)


        self.surname_label = ctk.CTkLabel(frame_biens, text="Prénom :",font=("Helvetica", 12,"bold"))
        self.surname_label.pack(anchor="w",pady=4,padx=4)
        self.surname_entry =  ctk.CTkEntry(frame_biens, placeholder_text="Entrez votre prénom ", width=300,corner_radius=0)
        self.surname_entry.pack(anchor="w",pady=4,padx=4)


        self.cin_label = ctk.CTkLabel(frame_biens, text="CIN :",font=("Helvetica", 12,"bold"))
        self.cin_label.pack(anchor="w",pady=4,padx=4)
        self.cin_entry =  ctk.CTkEntry(frame_biens, placeholder_text="Entrez votre CIN ", width=300,corner_radius=0)
        self.cin_entry.pack(anchor="w",pady=4,padx=4)
        self.ville_label = ctk.CTkLabel(frame_biens, text="Ville :", font=("Helvetica", 12,"bold"))
        self.ville_label.pack(anchor="w",pady=4,padx=4)
        selected_ville = ctk.StringVar()

         
        selected_ville.set(villes_maroc[0])


        self.ville_menu = ctk.CTkOptionMenu(frame_biens, variable=selected_ville, values=villes_maroc)
        
        self.ville_menu.pack(anchor="w",pady=4,padx=4)
        self.addr_label = ctk.CTkLabel(frame_biens, text="Adresse :",font=("Helvetica", 12,"bold"))
        self.addr_label.pack(anchor="w",pady=4,padx=4)
        self.addr_entry = ctk.CTkEntry(frame_biens,placeholder_text="Entrez votre adress",font=("Arial", 14),corner_radius=0,width=300)
        self.addr_entry.pack(anchor="w",pady=4,padx=4)
        self.email_label = ctk.CTkLabel(frame_biens, text="Email :",font=("Helvetica", 12,"bold"))
        self.email_label.pack(anchor="w",pady=4,padx=4)
        self.email_entry = ctk.CTkEntry(frame_biens,placeholder_text="Entrez votre Email",font=("Arial", 14),corner_radius=0,width=300)
        self.email_entry.pack(anchor="w",pady=4,padx=4)
        self.num_label = ctk.CTkLabel(frame_biens, text="N° de téléphone:",font=("Helvetica", 12,"bold"))
        self.num_label.pack(anchor="w",pady=4,padx=4)
        self.num_entry = ctk.CTkEntry(frame_biens,placeholder_text="Entrez le numéro de téléphone",font=("Arial", 14),corner_radius=0,width=300)
        self.num_entry.pack(anchor="w",pady=4,padx=4)



      
        

        
        self.submite_button = ctk.CTkButton(self.bframe, text="Confirmer", command=self.submit_form,
                                        font=("Helvetica", 30, "bold"), corner_radius=20, fg_color=orange,
                                        text_color="white", hover_color="green",state="normal")
        self.submite_button.pack(padx=250,side="right")
        

        
        self.delet_button = ctk.CTkButton(self.bframe, text="Supprimer", command=self.ask_confirmation,
                                        font=("Helvetica", 30, "bold"), corner_radius=20, fg_color=blue_ciel,
                                        text_color="white", hover_color="red")
        self.delet_button.pack(padx=40,pady=40)
       




    def revenir_page(self):
      
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def ask_confirmation(self):
        response = messagebox.askquestion("Confirmation", "Voulez-vous effacer tous les champs ?")
        if response == "yes":
            self.clear_all_fields()

    def reset_form(self):
        self.addr_entry.delete(0, tk.END)
        self.adrfinalentry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.carton_entry.delete(0, tk.END)
        self.objspecif_entry.delete(0, tk.END)
        self.npers_entry.delete(0, tk.END)
        self.selected_ville.set("El jadida")
        self.selected_services.set("cartons")
        self.selected_transp.set("camion")

        


    def submit_form(self):
        import threading

        lock = threading.Lock()
        if not all(
            [self.date_entry.get(), self.time_combo.get(), self.name_entry.get(), self.surname_entry.get(),self.surname_entry.get(),self.cin_entry.get(),self.email_entry.get(),
             self.ville_menu.get(),self.addr_entry.get()]
        ):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
        else:
          
            conn=sqlite3.connect("suivi_coli.db")
            c=conn.cursor()
            from userclass import user_idg
            print(user_idg)
            c.execute("insert into colis(id_user,poids,dimension) values(:usr,:pd,:dim)",{'usr':user_idg,'pd':self.date_entry.get(),'dim':self.time_combo.get()})
            
            
            c.execute("select id_colis from colis where id_user=? and poids=? and dimension=? ",(user_idg,self.date_entry.get(),self.time_combo.get()))
            
            idc=c.fetchall()
            print(idc)
            
            c.executemany(
                 "INSERT INTO article (id_colis, nom_article, desc_art) VALUES (?, ?, ?)",
                        [(idc[0][0], article[0], article[1]) for article in self.articles]
                                   )
            
            c.execute("insert into destinataire(id_dest,nm_dest,prn_dest,addr_dest,email_dest,num_dest,ville) values(:id_dest,:nm_dest,:prn_dest,:addr_dest,:email_dest,:num_dest,:ville)",{
                         'nm_dest':self.name_entry.get(),
                         'prn_dest':self.surname_entry.get(),
                         'addr_dest':self.addr_entry.get(),
                         'email_dest':self.email_entry.get(),
                         'num_dest':self.num_entry.get(),
                         'ville':self.ville_menu.get(),
                         'id_dest':self.cin_entry.get()})
            
            c.execute("update colis set id_dest=? where id_colis=?",(self.cin_entry.get(),idc[0][0]))
            
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Formulaire enregistré avec succès.")
            
            self.clear_all_fields()
            from paiement import Paiement
            self.controller.show_frame("Paiement")
    
    def create_titled_frame(self, parent, title, bg_color=None):
   
       frame = ctk.CTkFrame(parent, fg_color=bg_color)
       frame.pack(fill="x", padx=20, pady=10)

    
       title_label = ctk.CTkLabel(frame, text=title, font=("Arial", 16, "bold"), text_color="black", bg_color=bg_color)
       title_label.pack(anchor="w", padx=5, pady=5)

       return frame
    def add_article(self):
        """Ajoute un article à la liste"""
        article_name = self.article_name_entry.get().strip()
        article_description = self.article_description_entry.get().strip()

        if article_name and article_description:
            self.articles.append((article_name, article_description))
            self.article_listbox.insert(tk.END, f"{article_name}: {article_description}")
            self.article_name_entry.delete(0, tk.END)  
            self.article_description_entry.delete(0, tk.END)  
            print(self.articles)
        else:
            messagebox.showwarning("Attention", "Veuillez remplir le nom et la description.")
    def clear_all_fields(self):
    
       self.article_name_entry.delete(0, tk.END)
       self.article_description_entry.delete(0, tk.END)
       self.article_listbox.delete(0, tk.END)
       self.date_entry.delete(0, ctk.END)
       self.time_combo.delete(0, ctk.END)
       self.name_entry.delete(0, ctk.END)
       self.surname_entry.delete(0, ctk.END)
       self.cin_entry.delete(0, ctk.END)
       self.addr_entry.delete(0, ctk.END)
       self.email_entry.delete(0, ctk.END)
       self.num_entry.delete(0, ctk.END)
       self.ville_menu.set(self.ville_menu._values[0])
       self.articles=[]
      

    
    




    


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    dem_page = Colis(app, app)
    dem_page.pack(fill="both", expand=True)
    app.mainloop()
