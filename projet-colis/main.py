import tkinter as tk
from login2 import LoginPage
import customtkinter as ctk
from creeuncpt import Choixcmpt
from createtrp import CreatEntr
from createuser import CreatUser
from mdpsoublier import Mdps
from acc import TrackingApp
from account import Account
from security import Security
from modifmdps import ModifMdps
from procurationamis import Procami
from notification import notif
from modifinfo import Modifinf
from demenagementsfinal2 import Demanagement
from creecoli import Colis
from GPSsuiviecolis import SuiviColis
from paiement import Paiement
from supprimer import Suppcmpt
from mescolis import HistoriqueColis


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Application SPEEDY")
        self.configure(fg_color="white")# Fond blanc
        self.iconbitmap('logo.ico')
        
        # Conteneur pour les pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Création des pages
        self.frames = {}
        for F in (LoginPage, Choixcmpt,CreatEntr,CreatUser,Mdps,TrackingApp,Account,Security,ModifMdps,Procami,notif,Modifinf,Suppcmpt,Demanagement,Colis,SuiviColis,Paiement,HistoriqueColis):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Affiche la page de connexion par défaut
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()




if __name__ == "__main__":
    app = App()
    app.mainloop()
