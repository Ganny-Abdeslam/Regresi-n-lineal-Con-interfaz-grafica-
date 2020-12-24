from tkinter import Tk, Text, Button, filedialog, Entry, Label, StringVar
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

class Interfaz:
    def __init__(self, ventana):
        #iniciar ventana con titulo
        self.ventana = ventana
        self.ventana.title("Vlacho")
        self.ventana.config(bg = "gainsboro")
        self.ventana.geometry('900x100')
	
	#Creación de los espacios ha ingresar y lectura de ellos mandandolo a la función data_2D o data_3D
        Label(text = "Ingrese Nombre de la Columna #1", fg = "black", font = ("Verdana", 12)).grid(row = 0, column = 0, padx = 2, pady = 2)

        entrada1 = StringVar()
        msj1 = Entry(main, textvariable = entrada1, width = 14)
        msj1.grid(row = 1, column = 0, padx = 2, pady = 2)

        Label(text = " Ingrese Nombre de la Columna #2", fg = "black", font = ("Verdana", 12)).grid(row = 0, column = 1, padx = 2, pady = 2)

        entrada2 = StringVar()
        msj2 = Entry(main, textvariable = entrada2, width = 14)
        msj2.grid(row = 1, column = 1, padx = 2, pady = 2)

        Label(text = " Ingrese Nombre de la Columna #3", fg = "black", font = ("Verdana", 12)).grid(row = 0, column = 2, padx = 2, pady = 2)

        entrada3 = StringVar()
        msj3 = Entry(main, textvariable = entrada3, width = 14)
        msj3.grid(row = 1, column = 2, padx = 2, pady = 2)

        #Iniciar
        Iniciar_2d = Button(text = "Gráficar 2D", fg = "green", command = lambda:self.data_2d(msj1.get(),msj2.get()))
        Iniciar_2d.grid(row = 2, column = 0, padx = 2, pady = 2)

        Iniciar_3d = Button(text = "Gráficar 3D", fg = "green", command = lambda:self.data_3d(msj1.get(),msj2.get(),msj3.get()))
        Iniciar_3d.grid(row = 2, column = 1, padx = 2, pady = 2)
        
        #New
        Exit = Button(text="Salir", fg="red", command=self.ventana.destroy).grid(row = 2, column = 2, padx = 2, pady = 2)

    def data_2d(self, X, Y):
        archivo = filedialog.askopenfilename(filetypes =[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')]) 
        Matriz = pd.read_excel(archivo)
        df = pd.DataFrame(Matriz, columns= [X,Y])

        n = df[X].values.reshape(-1,1)
        m = df[Y].values.reshape(-1,1)

        lr = LinearRegression()
        lr.fit(n,m)
        pred = lr.predict(n)

        #Ecuación y=mx+c
        M = lr.coef_[0][0]
        C = lr.intercept_[0]

        label = r'%s = %0.2f*%s%+0.2f'%(Y,M,X,C)

	#-------
	#Graficar en 2D
	#-------

        fig = plt.figure(figsize=(14,14))
        plt.scatter(df[X],df[Y])
        plt.plot(n,pred, color = 'red', label = label)
        plt.xlabel(X)
        plt.ylabel(Y)
        plt.legend()
        plt.show()

    def data_3d(self, X, Y, Z):
        archivo = filedialog.askopenfilename(filetypes =[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')]) 
        Matriz = pd.read_excel(archivo)
        P = 'Cod'
        df = pd.DataFrame(Matriz, columns= [X,Y,Z,P])

        aux = pd.DataFrame()

        aux[X] = df[X]
        aux[Y] = df[Y]
        XY = np.array(aux)

        m = df[Z].values.reshape(-1,1)

        lr = LinearRegression()
        lr.fit(XY,m)
        pred = lr.predict(XY)

        colo1 = ['black', #Verde
         'green', #Verde
         'blue',  #Azul
         'red', #Naranja
         'orange'
        ]

        group1 = ['Datos obtenidos', #Verde
         'Datos obtenidos', #Verde
         'Datos obtenidos',  #Azul
         'Datos obtenidos', #Naranja
         'Datos obtenidos'
        ]

        colo2 = ['black',  #Verde
         'darkgreen', #VerdeOscuro
         'darkblue',  #AzulOscuro
         'darkred', #Naranja
         'darkorange'
        ]

        group2 = ['Datos predictivos',  #Verde
         'A', #VerdeOscuro
         'B',  #AzulOscuro
         'C', #Naranja
         'D'
        ]

        #------
	    #Graficar en 3D como tal
	    #------

        fig = plt.figure()
        ax = Axes3D(fig)

        # Creamos una malla, sobre la cual graficaremos el plano
        inicial1, final1 = self.generica(df[X])
        inicial2, final2 = self.generica(df[Y]) 
        xx, yy = np.meshgrid(np.linspace(inicial1-0.5, final1+0.5), np.linspace(inicial2-0.5, final2+0.5))

        # calculamos los valores del plano para los puntos x e y
        nuevoX = (lr.coef_[0][0] * xx)
        nuevoY = (lr.coef_[0][1] * yy) 

        # calculamos los correspondientes valores para z. Debemos sumar el punto de intercepción
        z = (nuevoX + nuevoY + lr.intercept_)

        # Graficamos el plano
        ax.plot_surface(xx, yy, z, alpha=0.2, cmap='hot')

        # Graficamos en azul los puntos en 3D
        ax.scatter(XY[:, 0], XY[:, 1], df[Z].values, c=np.take(colo1, df[P].values), label='Datos obtenidos', s=10)

        # Graficamos en rojo, los puntos que 
        ax.scatter(XY[:, 0], XY[:, 1], pred, c=np.take(colo2, df[P].values), label='Datos predictivos', s=10)
        for i in range(1,5):
            ax.scatter(inicial1-0.5,inicial2-0.5,pred[1],c=colo2[i],label = group2[i],s = 10)

        # con esto situamos la "camara" con la que visualizamos
        ax.view_init(elev=30., azim=65)

        ax.set_xlabel(X)
        ax.set_ylabel(Y)
        ax.set_zlabel(Z)
        ax.legend(loc = 2)
        ax.set_title(Y + ' vs ' + X + Z)
        plt.show()
    
    def generica(self, df):

        mayor = df[0]
        menor = df[0]

        for i in range(0, len(df)):
            if (df[i] > mayor):
                mayor = df[i]
            
            if (df[i] < menor):
                menor = df[i]

        return menor,mayor

main = Tk()
cafe = Interfaz(main)
main.mainloop()
