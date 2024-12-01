import tkinter as tk
from tkinter import ttk
import math
import threading
from camada_fisica import camadaFisica


class INTERFACE:
    def __init__(self):
        #criando a janela
        self.root = tk.Tk()

        self.root.title("modulacao")
        self.root.geometry("1000x1000")
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.root.bind("<Configure>", self.on_resize)
        options = ["select an option","NRZ-Polar", "Manchester", "Bipolar"]
        self.CamadaFisicaSelector = ttk.Combobox(self.root, values=options, state='readonly')
        self.CamadaFisicaSelector.bind("<<ComboboxSelected>>", self.on_selectFisica)
        self.CamadaFisicaSelector.set("Select an option")
        self.FisicaPort = ["select an option", "ASK","FSK","8-QAM"]
        self.FisicaPortSelector = ttk.Combobox(self.root, values=self.FisicaPort, state='readonly') 
        self.FisicaPortSelector.bind("<<ComboboxSelected>>", self.on_selectPortadora)
        self.FisicaPortSelector.set("Select an option")
        self.Enlace = ["select an option","Contagem de Caracteres", "Intersecção de bytes", "Bit de paridade", "CRC","Hamming"]
        self.CamadaEnlaceSelector = ttk.Combobox(self.root, values=self.Enlace, state='readonly') 
        self.CamadaEnlaceSelector.bind("<<ComboboxSelected>>", self.on_selectEnlace)
        self.CamadaEnlaceSelector.set("Select an option")
        self.FisicaPort_item=tk.StringVar()
        self.fisica_item=tk.StringVar()
        self.enlace_item=tk.StringVar()
        self.Screen=tk.IntVar()
        self.Bitstream=tk.StringVar()
        self.Bitstream_textBox=tk.Text(width=30,height=1)
        self.Bitstream_sendButton=tk.Button(text="send" ,command=self.bitstream_set)
        self.pagination_button_foward=tk.Button(text=">" ,command=self.page_set_foward)
        self.pagination_button_back=tk.Button(text="<" ,command=self.page_set_back)
        self.sliderErr = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_err)
        self.err_value=tk.DoubleVar()
        self.sliderErr.place(x=int(self.canvas.winfo_width()), y=100) 
        self.draw_center_lines()
        self.draw_sine_wave()
        self.root.mainloop()
    def update_err(self,value):
        """ Update the label with the current slider  """
        self.err_value.set(value)
        self.draw_sine_wave()
    def page_set_foward(self):
        x=self.Screen.get()
        x=x+1
        self.Screen.set(x)
        self.draw_sine_wave()
        self.update_canvas()
    def page_set_back(self):
        x=self.Screen.get()
        x=x-1
        self.Screen.set(x)
        self.draw_sine_wave()
        self.update_canvas()
    def update_canvas(self):
        self.canvas.delete("page")
        self.canvas.create_text(int(self.canvas.winfo_width()/4),(self.canvas.winfo_height()/2)+10,text=f"{int(self.Screen.get())}",font=("Helvetica"),fill="black",tags="page")

    def on_selectEnlace(self,event):
        item=self.CamadaEnlaceSelector.get()
        self.enlace_item.set(str(item))
        print(self.enlace_item.get())
        self.draw_sine_wave()
    def draw_center_lines(self):
        ##dividindo o canvas em 4
        canvas_width = self.canvas.winfo_width()
        canvas_height =self.canvas.winfo_height()    
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        self.canvas.create_line(0, center_y, canvas_width, center_y, fill='black', width=2,tags="center_lines")
        self.canvas.create_line(center_x, 0, center_x, canvas_height, fill='black', width=2,tags="center_lines")

    def bitstream_set(self):
        self.Bitstream.set(str(self.Bitstream_textBox.get("1.0", tk.END).strip()))
        print(self.Bitstream.get())
        self.draw_sine_wave()
    
    def on_resize(self,event):
        canvas_width =  self.root.winfo_width()
        canvas_height = self.root.winfo_height()
        self.canvas.config(width=canvas_width, height=canvas_height)    
        self.draw_sine_wave()
        #retirando os desenhops antigos
        self.canvas.delete("center_lines")
        self.canvas.delete("text")
        self.canvas.delete("page")
        #redrawing
        self.draw_center_lines()
        sliderFreq_x = ((canvas_width) // 2)+10
        sliderFreq_y = 20  
        self.Bitstream_textBox.place(x=(sliderFreq_x+canvas_width/4)-35,y=20)
        self.Bitstream_sendButton.place(x=(sliderFreq_x+canvas_width/4)-35,y=45)
        self.CamadaFisicaSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +90)
        self.CamadaEnlaceSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +230)
        self.FisicaPortSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +160)
        self.canvas.create_text((sliderFreq_x+canvas_width/4)+50, sliderFreq_y +80,text="opções de camada fisica(normal)",font=("Helvetica"),fill="black",tags="text")
        self.canvas.create_text((sliderFreq_x+canvas_width/4)+60, sliderFreq_y +150,text="opções de camada fisica(portadora)",font=("Helvetica"),fill="black",tags="text")
        self.canvas.create_text((sliderFreq_x+canvas_width/4)+25, sliderFreq_y +220,text="opções de camada enlace",font=("Helvetica"),fill="black",tags="text")
        self.canvas.create_text(sliderFreq_x+canvas_width/4, sliderFreq_y - 10,text="Bitstream",font=("Helvetica"),fill="black",tags="text")
        self.pagination_button_back.place(x=0,y=int(self.canvas.winfo_height()/2))
        self.pagination_button_foward.place(x=int(self.canvas.winfo_width()/2)-35,y=(self.canvas.winfo_height()/2))
        self.sliderErr.config(length=int(canvas_width * 0.2  ))
        self.sliderErr.place(x=(int(self.canvas.winfo_width())/2)+10, y=20)         
        self.draw_sine_wave()
    def on_selectFisica(self,event):
        item=self.CamadaFisicaSelector.get()
        self.fisica_item.set(str(item))
        print(self.fisica_item.get())
        self.draw_sine_wave()

    def on_selectPortadora(self,event):
        item=self.FisicaPortSelector.get()
        self.FisicaPort_item.set(str(item))
        print(self.FisicaPort_item.get())
        self.draw_sine_wave()
    def draw_sine_wave(self):
        self.canvas.delete("lines")
        ProtocoloFisica=str(self.fisica_item.get())
        ProtocoloEnlace=str(self.enlace_item.get())
        wave=[]
        bitMessage=self.Bitstream.get()
        ProtocoloFisicaPort=str(self.FisicaPort_item.get())
        Fisica=camadaFisica()
        n=0
        if ProtocoloFisica == "NRZ-Polar":
            wave=Fisica.nrz_polar(bit_stream=bitMessage)
            bitMessage=wave
            n=1
        elif ProtocoloFisica == "Manchester":
            wave=Fisica.manchester(bit_stream=bitMessage)
            bitMessage=wave
        elif ProtocoloFisica == "Bipolar":
            wave=Fisica.bipolar(bit_stream=bitMessage)
            bitMessage=wave
        if  ProtocoloFisicaPort == "ASK":
            wave=Fisica.ask(dig_signal=bitMessage,h=n)
        elif ProtocoloFisicaPort == "FSK":
            wave=Fisica.fsk(dig_signal=bitMessage,h=n)
        elif ProtocoloFisicaPort == "8-QAM":
            wave=Fisica.qam8_modulation(dig_signal=bitMessage)
        
        if wave:
            ##paginacao
            paginacao=self.Screen.get()
            newwave=[]
            for i in range(500):
                if ((500*paginacao)+i)<len(wave):
                    newwave.append(wave[(500*paginacao)+i])
            wave=newwave
            newwave=[]
            
            for i in range(len(wave)):
                newwave.append(i+10)
                newwave.append((wave[i]*100+(self.canvas.winfo_width()/8)))
            wave=newwave
            self.canvas.create_line(wave, fill="blue", width=2,tags="lines")

