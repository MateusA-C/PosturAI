import customtkinter as ctk
from tkinter import messagebox

class App(ctk.CTk):

    def __init__(self):
        
        super().__init__()

        self.geometry("600x500")
        self.title("teste ctk")

        self.texto = ctk.CTkLabel(self,text = "Testando o Customtkinter!",text_color='green')
        self.texto.grid(row = 5 , column = 1,padx = 20, pady = 20)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=0)
        self.grid_columnconfigure(2,weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.button_info = ctk.CTkButton(self,text= 'info',command=self.button_info_click,fg_color='blue')
        self.button_info.grid(row = 0, column = 1,padx=10,pady=10)

        self.button_allert = ctk.CTkButton(self,text='allert', command = self.button_allert_click,fg_color='red')
        self.button_allert.grid(row = 1, column = 1,padx=10,pady=10)

        self.button_error = ctk.CTkButton(self,text='error', command= self.button_error_click,fg_color='yellow')
        self.button_error.grid(row = 2, column = 1,padx=10,pady=10)

        self.nome_usuario = ctk.CTkEntry(self,placeholder_text= "Digite o seu nome por favor!")
        self.nome_usuario.grid(row = 3, column = 0,padx=10,pady=10)

        self.botao_printar_usuario = ctk.CTkButton(self,text="enviar",command = lambda: messagebox.showinfo('llll',f'seu nome é: {self.nome_usuario.get()}'))
        self.botao_printar_usuario.grid(row = 3, column = 2, padx=10 ,pady=10)
    def button_info_click(self):

        print("botão pressionado")
        messagebox.showinfo("botão pressionado!"," o botão fpoi pressionado")

    def button_allert_click(self):
        messagebox.showwarning("o botão de erro foi pressionado","botão de erro pressionado!")

    def button_error_click(self):
        messagebox.showerror("botão de erro foi clicado","botão de erro clicado!")

app = App()
app.mainloop()