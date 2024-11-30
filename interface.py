import tkinter as tk
from tkinter import ttk
import math
from camada_fisica import camadaFisica
from camada_enlace import CamadaEnlace
##tranformando strings em bits
def string_to_bitstream(input_string):
    bitstream = ''    
    for char in input_string:
        binary_char = format(ord(char), '08b')
        bitstream += binary_char    
    return bitstream
#upadate
def update_canvas():
    canvas.delete("page")
    canvas.create_text(int(canvas.winfo_width()/4),(canvas.winfo_height()/2)+10,text=f"{int(Screen.get())}",font=("Helvetica"),fill="black",tags="page")
#event handlers
def on_next():
    x=Screen.get()
    x=x+1
    Screen.set(x)
    update_canvas()
    draw_sine_wave()

def on_previus():
    x=Screen.get()
    x=x-1
    Screen.set(x)
    update_canvas()
    draw_sine_wave()

def on_selectFisica(event):
    item=CamadaFisicaSelector.get()
    fisica_item.set(str(item))
    draw_sine_wave()

def on_selectPortadora(event):
    item=FisicaPortSelector.get()
    FisicaPort_item.set(str(item))
    draw_sine_wave()
def on_selectEnlace(event):
    item=CamadaEnlaceSelector.get()
    enlace_item.set(str(item))
    draw_sine_wave()
#Set de variaveis bistream,funcao de barulho 
def bitstream_set():
    Bitstream.set(str(Bitstream_textBox.get("1.0", tk.END).strip()))
    draw_sine_wave()

def functset():
    string=textbox.get("1.0", tk.END).strip()
    Noisefunction.set(string)
    noise_type.set(False)
    draw_sine_wave()
##sliders de barulho
def update_Freq(value):
    """ Update the label with the current slider  """
    Freq_var.set("Frequencia")
    Freq_value.set(value)
    noise_type.set(True)
    draw_sine_wave()

def update_Amp(value):
    """ Update the label with the current slider  """
    Amp_var.set("Amplitude")
    Amp_value.set(value)
    noise_type.set(True)
    draw_sine_wave()

def update_Offset(value):
    """ Update the label with the current slider  """
    Offset_var.set("offset")
    Offset_value.set(value)
    noise_type.set(True)
    draw_sine_wave()   
#parsers da funcao de barulho
def parsefunction(x,numeroPontos):
    n=[]
    amp=0
    openbrackets=False
    Sum=False
    alredy=False
    offset=""
    freq=0
    for i in range(len(x)):

        if x[i].isnumeric() and openbrackets==False:
            if amp!=0:
                amp=(10*amp)+int(x[i])
                if x[i-2]=="-":
                    amp=amp*-1
            else:
                amp=int(x[i])
                if i!=0:
                    if x[i-1]=="-" and x[i+1].isnumeric()!=True:
                        amp=amp*-1
        elif x[i]=="c":
            if amp==0:
                amp=1
            function="cos"
        elif x[i]=="e":
            if amp==0:
                amp=1
            function="sen"
        elif x[i]=="(":
            openbrackets=True
        elif x[i]==")" and i!=len(x)-1:
            if freq==0:
                freq=1
            openbrackets=False
            sum=False
            alredy=False
        elif x[i]=="p":
            if x[i-1].isnumeric():
                offset=3.14*int(x[i-1])
            else:
                offset=3.14
        elif x[i].isnumeric()==True and openbrackets==True and (x[i+1]=="x" or x[i+1].isnumeric() )and alredy==False and Sum==False:
            j=1
            freq=int(x[i])
            while x[i+j].isnumeric() :
                alredy=True
                freq=freq*10+int(x[i+j])
                j=j+1
        elif x[i]=='+' and openbrackets==True:
            Sum=True
        elif x[i].isnumeric()==True and Sum==True:
            if offset=="":
                offset=int(x[i])
            else:
                offset=(10*offset)+int(x[i])
        elif( (x[i]=="+" or x[i]=="-") and openbrackets==False) or (i==(len(x)-1)):
            if freq==0:
                freq=1
            n.append({"amp":amp,"freq":freq,"offset":offset,"function":function})
            amp=0
            openbrackets=False
            sum=False
            offset=""
            freq=0
    wave=functionvalue(x=numeroPontos,function=n)
    return wave

def num(x,function):
    table=[]
    for i in range(x):
        if function["offset"]=="":
            function["offset"]=0
        if function["function"]=="cos":
            y=math.cos((i*function["freq"]/100)+function["offset"])*function["amp"]*10

            table.append(y)
        else:
            y=math.sin((i*function["freq"]/100)+function["offset"])*function["amp"]*10
            table.append(y)
    return table    

def functionvalue(x,function):
    Table=[]
    results=[]
    result=0
    Results=[]
    for i in range(len(function)):
        table=num(x,function=function[i])
        Table.append(table)
    for i in range(x):
        result=0
        for j in range(len(Table)):

            result=Table[j][i]+result
        results.append(result)
        
    for i in range(len(results)):
        Results.append(results[i])
    return Results
##resize 
def on_resize(event):
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    canvas.config(width=canvas_width, height=canvas_height)    
    draw_sine_wave()
    #retirando os desenhops antigos
    canvas.delete("center_lines")
    canvas.delete("text")
    canvas.delete("page")
    #redrawing
    draw_center_lines()
    slider_length = canvas_width * 0.2  
    sliderFreq.config(length=int(slider_length))
    sliderFreq_x = ((canvas_width) // 2)+10
    sliderFreq_y = 20  
    sliderFreq.place(x=sliderFreq_x, y=sliderFreq_y+20)
    labelFreq.place(x=sliderFreq_x, y=sliderFreq_y+5) 
    sliderAmp.config(length=int(slider_length))
    sliderFreq_x = ((canvas_width) // 2)+10
    sliderFreq_y = 20  
    sliderAmp.place(x=sliderFreq_x, y=sliderFreq_y+80)
    Amp.place(x=sliderFreq_x, y=sliderFreq_y+65)  
    slideOffset.config(length=int(slider_length))
    sliderFreq_x = ((canvas_width) // 2)+10
    sliderFreq_y = 20  
    slideOffset.place(x=sliderFreq_x, y=sliderFreq_y+140)
    Offset.place(x=sliderFreq_x, y=sliderFreq_y+125) 
    textbox.place(x=sliderFreq_x,y=sliderFreq_y+190)
    sendButton.place(x=sliderFreq_x,y=sliderFreq_y+220)
    Bitstream_textBox.place(x=(sliderFreq_x+canvas_width/4)-35,y=20)
    Bitstream_sendButton.place(x=(sliderFreq_x+canvas_width/4)-35,y=45)
    CamadaFisicaSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +90)
    CamadaEnlaceSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +230)
    FisicaPortSelector.place(x=(sliderFreq_x+canvas_width/4)-35, y=sliderFreq_y +160)
    canvas.create_text((sliderFreq_x+canvas_width/4)+50, sliderFreq_y +80,text="opções de camada fisica(normal)",font=("Helvetica"),fill="black",tags="text")
    canvas.create_text((sliderFreq_x+canvas_width/4)+60, sliderFreq_y +150,text="opções de camada fisica(portadora)",font=("Helvetica"),fill="black",tags="text")
    canvas.create_text((sliderFreq_x+canvas_width/4)+25, sliderFreq_y +220,text="opções de camada enlace",font=("Helvetica"),fill="black",tags="text")
    canvas.create_text(sliderFreq_x+canvas_width/4, sliderFreq_y - 10,text="Bitstream",font=("Helvetica"),fill="black",tags="text")
    update_canvas()
    prevBox.place(x=0,y=int(canvas.winfo_height()/2))
    nextBox.place(x=int(canvas.winfo_width()/2)-35,y=(canvas.winfo_height()/2))

def draw_center_lines():
    ##dividindo o canvas em 4
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()    
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    canvas.create_line(0, center_y, canvas_width, center_y, fill='black', width=2,tags="center_lines")
    canvas.create_line(center_x, 0, center_x, canvas_height, fill='black', width=2,tags="center_lines")

def draw_sine_wave():
    canvas.delete("line")
    ##desenhando o barulho
    if noise_type.get()==True:
        ##sliders 
        freq=int(Freq_value.get())
        amp=int(Amp_value.get())
        Offset=int(Offset_value.get())
        amplitude = 100*amp/45
        frequency = 0.05*(freq)/20 
        offset = canvas.winfo_height() // 2
        widht=canvas.winfo_width() 
        if offset==0:
            offset=200
            widht=150
        points = []
        NoiseAmp=[]
        for x in range(int ((widht/2)-20)):
            y = (amplitude * math.sin((frequency * (x))+Offset)*canvas.winfo_height()/1000 + offset )-canvas.winfo_height()/4
            n=x+10
            noiseamp=(amplitude * math.sin((frequency * (x))+Offset))
            NoiseAmp.append(noiseamp)
            points.append((n, y))
    else:
        #funcao
        offset = canvas.winfo_height() // 2
        widht=canvas.winfo_width() 
        if offset==0:
            offset=200
            widht=150
        points = []
        NoiseAmp=[]
        primalWave=parsefunction(x=Noisefunction.get(),numeroPontos=int ((widht/2)-50,))  
        for x in range((int ((widht/2)-50))):
                y = ((primalWave[x]*canvas.winfo_height()/1000 + offset))-canvas.winfo_height()/4
                noiseamp=(primalWave[x])
                NoiseAmp.append(noiseamp)
                n=(x+10)
                points.append((n, y))
    canvas.create_line(points, fill='blue', smooth=True,tags="line")
    ##desenhando o sinal inadulterado
    bitMessage=str(Bitstream.get())
    flag=0
    for i in range(len(bitMessage)):
        if bitMessage[i]!="0" and bitMessage[i]!="1":
            flag=1
    if flag==1:
        bitMessage=string_to_bitstream(bitMessage)
    ProtocoloFisica=str(fisica_item.get())
    ProtocoloEnlace=str(enlace_item.get())
    wave=[]
    ProtocoloFisica=str(fisica_item.get())
    ProtocoloEnlace=str(enlace_item.get())
    ProtocoloFisicaPort=str(FisicaPort_item.get())

    wave=[]
    n=0
    Enlace=CamadaEnlace()
    #selecionando os protocolos
    if ProtocoloEnlace == "Contagem de Caracteres":
        bitMessage=Enlace.contagem_de_char(bitMessage)
    elif ProtocoloEnlace == "Intersecção de bytes":
        bitMessage=Enlace.enquadrar_insercao_bytes(bitMessage)
    elif ProtocoloEnlace == "Bit de paridade":
        bitMessage=Enlace.adicionar_bit_deParidade(bitMessage)
    elif ProtocoloEnlace == "CRC":
        bitMessage=Enlace.crc16(bitMessage)
    elif ProtocoloEnlace == "Hamming":
        bitMessage=Enlace.adicionar_hamming(bitMessage)
        n=1
    Fisica=camadaFisica()
    if ProtocoloFisica == "NRZ-Polar":
        wave=Fisica.nrz_polar(bit_stream=bitMessage)
        bitMessage=wave
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
    Wave = []

    WaveAmp=wave.copy()
    for i in range(len(WaveAmp)):
        WaveAmp[i]=WaveAmp[i]*100
    for i in range(len(wave)):
        Wave.append([i, wave[i]])
    wave = Wave.copy()
    Wave.clear()
    if wave:
        ##paginacao
        page=Screen.get()
        Wave=[wave[i:i + int((canvas.winfo_width()/8)-50)] for i in range(0, len(wave), int((canvas.winfo_width()/8)-50))]
        if page<len(Wave):
            for j in range(len(Wave[page])):
                Wave[page][j][0] = j * 5 + 10
                Wave[page][j][1] = int(Wave[page][j][1] * 50 + int(canvas.winfo_height() / 4) * 3)
            canvas.create_line(Wave[page], fill="red", width=2, tags="line")
    ##desenhando o sinal adulterado pelo barulho
    reciever = []
    offset = canvas.winfo_height() // 2
    widht=canvas.winfo_width() 
    if offset==0:
        offset=200
        widht=150
    if WaveAmp!=[]:
        while len(NoiseAmp)<len(WaveAmp):
            NoiseAmp=NoiseAmp+NoiseAmp
        for x in range(int((len(WaveAmp))/2)):
            y = ((NoiseAmp[x]+WaveAmp[x])*canvas.winfo_height()/2000 + offset)+canvas.winfo_height()/5
            n=x+10+canvas.winfo_width() // 2
            reciever.append((n, y))
        if len(reciever)>canvas.winfo_width()/2:
            reciever=[reciever[i:i + int((canvas.winfo_width()/2))] for i in range(0, len(reciever), int((canvas.winfo_width()/2)))]
            op=[]
            ##paginacao
            if page>=len(reciever):
                page=-1
            for i in range(len(reciever[page])):
                y=reciever[page][i][1]
                n=i+10+canvas.winfo_width() // 2
                op.append((n,y))
            reciever[page]=op

            canvas.create_line(reciever[page], fill='blue', smooth=True,tags="line")
        else:
            canvas.create_line(reciever, fill='blue', smooth=True,tags="line")
#criando a janela
root = tk.Tk()
root.title("modulacao")

root.geometry("1000x1000")

canvas = tk.Canvas(root, width=400, height=300, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

#criando o resize
root.bind("<Configure>", on_resize)

#criandoa caixas de texto e botoes
width=int(canvas.winfo_width())
sliderFreq = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_Freq)
sliderFreq.place(x=width, y=20)
Freq_var = tk.StringVar()
Freq_var.set("Frequencia")
labelFreq = tk.Label(root, textvariable=Freq_var)
labelFreq.place(x=(canvas.winfo_width()/2)+100, y=20)
sliderAmp = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_Amp)
sliderAmp.place(x=width, y=20)
Amp_var = tk.StringVar()
Amp_var.set("Amplitude")
Amp = tk.Label(root, textvariable=Amp_var)
Amp.place(x=(canvas.winfo_width()/2)+100, y=20)
slideOffset = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_Offset)
slideOffset.place(x=width, y=20)
Offset_var = tk.StringVar()
Offset_var.set("Offset")
Offset = tk.Label(root, textvariable=Offset_var)
Offset.place(x=(canvas.winfo_width()/2)+100, y=20)
Amp_value=tk.DoubleVar()
Freq_value=tk.DoubleVar()
Offset_value=tk.DoubleVar()
Noisefunction=tk.StringVar()
textbox=tk.Text(width=30,height=1)
sendButton=tk.Button(text="send",command=functset)
noise_type=tk.BooleanVar()
noise_type.set(True)
Bitstream=tk.StringVar()
Bitstream_textBox=tk.Text(width=30,height=1)
Bitstream_sendButton=tk.Button(text="send" ,command=bitstream_set)
options = ["select an option","NRZ-Polar", "Manchester", "Bipolar"]
CamadaFisicaSelector = ttk.Combobox(root, values=options, state='readonly')
CamadaFisicaSelector.bind("<<ComboboxSelected>>", on_selectFisica)
CamadaFisicaSelector.set("Select an option")
fisica_item=tk.StringVar()
enlace_item=tk.StringVar()
Enlace = ["select an option","Contagem de Caracteres", "Intersecção de bytes", "Bit de paridade", "CRC","Hamming"]
CamadaEnlaceSelector = ttk.Combobox(root, values=Enlace, state='readonly') 
CamadaEnlaceSelector.bind("<<ComboboxSelected>>", on_selectEnlace)
CamadaEnlaceSelector.set("Select an option")
FisicaPort_item=tk.StringVar()
FisicaPort = ["select an option", "ASK","FSK","8-QAM"]
FisicaPortSelector = ttk.Combobox(root, values=FisicaPort, state='readonly') 
FisicaPortSelector.bind("<<ComboboxSelected>>", on_selectPortadora)
FisicaPortSelector.set("Select an option")
Screen=tk.IntVar()
Screen.set(0)
nextBox=tk.Button(text=">",command=on_next)
prevBox=tk.Button(text="<",command=on_previus)
#iniciacao do loop
draw_center_lines()
draw_sine_wave()
root.mainloop()
