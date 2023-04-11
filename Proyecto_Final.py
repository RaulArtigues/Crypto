#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:53:51 2022

@author: raulartiguesfemenia
"""

#Instalamos y cargamos las librerias necesarias

#!pip install pykrakenapi
#!pip install tk
#!pip install mplfinance

import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from tkinter import messagebox

############################################################
#Cargamos la api
api = krakenex.API()
k = KrakenAPI(api)


#Leemos los datos 

data1= k.get_ohlc_data("ETHUSD", interval=1440, ascending = True)
data2= k.get_ohlc_data("BTCUSD", interval=1440, ascending = True)
data3= k.get_ohlc_data("LTCUSD", interval=1440, ascending = True)
data4= k.get_ohlc_data("USDTUSD", interval=1440, ascending = True)
data5= k.get_ohlc_data("USDCUSD", interval=1440, ascending = True)
data6= k.get_ohlc_data("DOGEUSD", interval=1440, ascending = True)


#Convertimos la tupla a DataFrame
df1= pd.DataFrame(data1[0])
df2= pd.DataFrame(data2[0])
df3= pd.DataFrame(data3[0])
df4= pd.DataFrame(data4[0])
df5= pd.DataFrame(data5[0])
df6= pd.DataFrame(data6[0])


#Creamos un único dataframe
dfFinal= pd.DataFrame()
dfFinal["ETH"]= df1.close
dfFinal["BTC"]= df2.close
dfFinal["LTC"]= df3.close
dfFinal["USDT"]= df4.close
dfFinal["USDC"]= df5.close
dfFinal["DOGE"]= df6.close


#Etablecemos período de tiempo
fecha_inicio= datetime.now()- timedelta(days=719)
fecha_hoy= datetime.now()

lista_fechas = [fecha_inicio + timedelta(days=d) for d in range((fecha_hoy - fecha_inicio).days + 1)]
dfFinal["Fecha"]= lista_fechas

############################################################

#Creamos la pestaña general
window = Tk()
window.title("PROYECTO FINAL PYTHON") 
window.geometry('1000x1000')
window.configure(background='#440c29')

#Estilo de las distintas pestañas
style = ttk.Style()
settings = {"TNotebook.Tab": {"configure": {"padding": [10, 1],
                                            "background": "#fdd57e"
                                           },
                              "map": {"background": [("selected", "#C70039"), 
                                                     ("active", "#fc9292")],
                                      "foreground": [("selected", "#ffffff"),
                                                     ("active", "#000000")]}}}  
style.theme_create("mi_estilo", settings=settings)
style.theme_use("mi_estilo")

#Definicmos las pestañas
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Inicio') 
tab_control.add(tab2, text='Cotizaciones')
tab_control.add(tab3, text='Indicadores')

############################################################

#Etiquetas de inicio
label1= Label(tab1, text="Comparador de cryptomonedas", font=("Verdana Bold",30))
label1.pack(anchor=CENTER)


label2= Label(tab1, text="Cryptomonedas disponibles")
label2.pack(anchor=CENTER)


#Tabla donde se encuentran las distintas cryptos
tv = ttk.Treeview(tab1, columns=("col1", "col2"))
tv.column("#0", width=150)
tv.column("col1", width=90, anchor=CENTER)
tv.column("col2", width=150, anchor=CENTER)
 
 
tv.heading("#0", text="Nombre", anchor=CENTER)
tv.heading("col1", text="Nomenclatura", anchor=CENTER)
tv.heading("col2", text="Valor de hoy en $", anchor=CENTER)
 
tv.insert("",END,text="Ethereum", values=("ETH","1097,93"))
tv.insert("", END, text="Bitcoin", values=("BTC","15623,11"))
tv.insert("", END, text="Litecoin", values=("LTC","60,30"))
tv.insert("", END, text="Tether", values=("USDT","0,99"))
tv.insert("", END, text="USD coin", values=("USDC","1,00"))
tv.insert("", END, text="Dogecoin", values=("DOGE","0,07"))
 
tv.pack(side='top') 

#Segundo pestaña. Plot de las distintas cryptos
label3= Label(tab2, text="Elección de las cryptosmonedas")
label3.pack(anchor=CENTER)


#Creamos los chechobox para la elecciones de las monedas
Asid1_state = BooleanVar()
Asid1_state.set(False)
Asid1 = Checkbutton(tab2, text='ETH', var=Asid1_state) 
Asid1.pack(anchor=CENTER)

Asid2_state = BooleanVar()
Asid2_state.set(False)
Asid2 = Checkbutton(tab2, text='BTC', var=Asid2_state) 
Asid2.pack(anchor=CENTER)

Asid3_state = BooleanVar()
Asid3_state.set(False)
Asid3 = Checkbutton(tab2, text='LTC', var=Asid3_state) 
Asid3.pack(anchor=CENTER)

Asid4_state = BooleanVar()
Asid4_state.set(False)
Asid4 = Checkbutton(tab2, text='USDT', var=Asid4_state) 
Asid4.pack(anchor=CENTER)

Asid5_state = BooleanVar()
Asid5_state.set(False)
Asid5 = Checkbutton(tab2, text='USDC', var=Asid5_state) 
Asid5.pack(anchor=CENTER)

Asid6_state = BooleanVar()
Asid6_state.set(False)
Asid6 = Checkbutton(tab2, text='DOGE', var=Asid6_state) 
Asid6.pack(anchor=CENTER)


#Función para plotear el gráfico con las cotizaciones de las monedas elegidas
def cotizacion():


    #Función para plotear el gráfico de las criptos
    def visu(cripto, cripto_ext):
        
        plot1.plot(dfFinal.Fecha,dfFinal[cripto], label=cripto_ext) 
        plot1.set_xlabel("Meses")
        plot1.set_ylabel("Valores de la criptomoneda")
        plot1.spines['bottom'].set_linestyle("--")
        plot1.spines['bottom'].set_linewidth(1)
        plot1.spines["bottom"].set_color('#404040')
        plot1.legend(fontsize=12, shadow=True, facecolor="Bisque",title="Cryptomoneda") 

    if (Asid1_state.get()==0 and Asid2_state.get()==0 and Asid3_state.get()==0 and
        Asid4_state.get()==0 and Asid5_state.get()==0 and Asid6_state.get()==0):
        messagebox.showinfo('Error','Selecciona una o más cryptos')
    
    else:    
        try:
            
            #Creamos la figura
            fig= Figure(figsize = (10, 10), 
                 dpi = 100) 
            plot1 = fig.add_subplot(111)            
    
            #En este apratado pleatmos la/las monedas elegidas
            if (Asid1_state.get()==1) :
                visu('ETH','Ethereum')
        
            if (Asid2_state.get()==1) :
                visu('BTC','Bitcoin')
        
            if (Asid3_state.get()==1) :
                visu('LTC','Litecoin')
        
            if (Asid4_state.get()==1) :
                visu('USDT','Tether')
        
            if (Asid5_state.get()==1) :
                visu('USDC','USD coin')
        
            if (Asid6_state.get()==1) :
                visu('DOGE','Dogecoin')

            #Creamos el gráfico en Tkinter
            canvas = FigureCanvasTkAgg(fig,master = window)   
            canvas.draw() 
            canvas.get_tk_widget().pack() 
            toolbar = NavigationToolbar2Tk(canvas,window) 
            toolbar.update() 
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0) 
            def Limpiar1():
                canvas.get_tk_widget().destroy()
                btn2.destroy()
        
    #Boton y función para eliminar los resultados anteriores
            btn2 = Button(tab2, text="BORRAR", command=Limpiar1)
            btn2.pack(anchor=CENTER) 
            
        except:
            messagebox.showinfo('Error','Selecciona una o más cryptos')
   
#Boton para ejectuar la elección   
btn1 = Button(tab2, text="Ejecutar", command= cotizacion)
btn1.pack(anchor=CENTER)   

############################################################

#Tercera pestaña. Plot de las medias móviles y RSI de las distitnas cryptos
label4= Label(tab3, text="Elige una crypto")
label4.pack(anchor=CENTER)

combo= ttk.Combobox(tab3,state="readonly", 
                    values=["ETH","BTC","LTC","USDT","USDC","DOGE"])
combo.pack(anchor=CENTER) 
combo.current(None) 

############################################################
#Media móvil de la crypto selecciona mediante el combobox

def grafica():
    try:
        fig= Figure(figsize = (20, 20), 
                 dpi = 100) 
        ax= fig.subplots(1,3)  
    
        n=30
        seleccion= str(combo.get())
        dat=pd.Series(dfFinal[seleccion]).rolling(window =n).mean().iloc[n-1:].values

        fecha_inicio= datetime.now()- timedelta(days=719)
        fecha_hoy= datetime.now()
    
        datos1=[]
        contador=0
        for i in range(720):
            if i>=720-n:
                contador +=1
                if contador==1:
                    datos1.insert(0,None)
                else:
                    datos1.insert(1,None)     
            else:
                datos1.append(dat[i])

        lista_fechas = [fecha_inicio + timedelta(days=d) for d in range((fecha_hoy - fecha_inicio).days + 1)]
        dfFinal["Fecha"]= lista_fechas 

############################################################
        def rsi(periods = 14, ema = True):

            close_delta = dfFinal[seleccion].diff()

            up = close_delta.clip(lower=0)
            down = -1 * close_delta.clip(upper=0)
    
            if ema == True:
                ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
                ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
            else:
                ma_up = up.rolling(window = periods, adjust=False).mean()
                ma_down = down.rolling(window = periods, adjust=False).mean()
        
            rsi1= ma_up / ma_down
            rsi1= 100 - (100/(1 + rsi1))
        
######################### Gráfico de RSI ##################################
            ax[1].plot(dfFinal.Fecha, rsi1, color = 'tab:red')
            ax[1].set_title(f"RSI: {seleccion}" )
            ax[1].set_xlabel("Fecha")
            ax[1].set_ylabel(f"RSI de {seleccion}")

        rsi()

    ################# Gráfico de las medias móviles ###########################
        ax[0].plot(dfFinal.Fecha, datos1, color = 'tab:green')
        ax[0].set_title(f"Media movil de: {seleccion}" )
        ax[0].set_xlabel("Fecha")
        ax[0].set_ylabel(f"Media móvil de {seleccion}")
    
    ################# Gráfico de las medias móviles junto a sus valores#########
        ax[2].plot(dfFinal.Fecha, datos1, color = 'tab:green', label="Media móvil")
        ax[2].plot(dfFinal.Fecha, dfFinal[seleccion], color = 'tab:purple', label="Valor crypto")
        ax[2].set_title(f"Media movil y valor de: {seleccion}" )
        ax[2].set_xlabel("Fecha")
        ax[2].set_ylabel(f"Media móvil y valor de {seleccion}")
        ax[2].legend()

    ##################### Imprimir los 3 gráficos en tkinter ##################3
        canvas = FigureCanvasTkAgg(fig,master = window)   
        canvas.draw() 
        canvas.get_tk_widget().pack() 
        toolbar = NavigationToolbar2Tk(canvas,window) 
        toolbar.update() 
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
    
        def Limpiar1():
            canvas.get_tk_widget().destroy()
            btn2.destroy()
        
    #Boton y función para eliminar los resultados anteriores
        btn2 = Button(tab3, text="BORRAR", command=Limpiar1)
        btn2.pack(anchor=CENTER) 
    
    except:
        messagebox.showinfo('Error','Selecciona una crypto')      

btn3 = Button(tab3, text="Plotear", command= grafica)
btn3.pack(anchor=CENTER)   

#Ejecutar la pestaña
tab_control.pack(expand=1,fill='both')
window.mainloop()

