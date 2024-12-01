from math import sin, cos, pi
class camadaFisica:
    #Modulação digital
    def __init__(self) -> None:
            pass
    def nrz_polar(self,bit_stream):
        #Se o bit for 1, sinal digital correspondente é 1, e se for 0, sinal digital correspondente é -1
        dig_signal = []
        for bit in bit_stream:
            if bit == "1":
                dig_signal.append(1)
            else:
                dig_signal.append(-1)
        return dig_signal

    def manchester(self,bit_stream):
        #Combina clock com o bit atual a partir de operação xor
        dig_signal = []
        for bit in bit_stream:
            if bit == "0":
                #Faz o xor entre o clock e o bit atual (0)
                dig_signal.append(0)
                dig_signal.append(1)
            else:
                #Faz o xor entre o clock e o bit atual (1)
                dig_signal.append(1)
                dig_signal.append(0)
        return dig_signal

    def bipolar(self,bit_stream):
        #Se o bit for 0, sinal digital correspondente é 0, e se for 1, alterna entre 1 e -1
        dig_signal = []
        flag = 0
        for bit in bit_stream:
            if bit == "1":
                if flag == 0:
                    dig_signal.append(1)
                    flag = 1
                else:
                    dig_signal.append(-1)
                    flag = 0
            else:
                dig_signal.append(0)
        return dig_signal

    #Modulação por portadora
    #Frequência default da portadora: 5kHz
    #Quantidade default de amostras do sinal: 100000
    def ask(self, dig_signal, a1=1,a2=1.5, sample=100,h=0):
        if len(dig_signal)==0:
            return []
        else:
            signal=[]
            for i in range(len(dig_signal)):
                for j in range(sample):
                    if h==0:
                        if dig_signal[i]=='1' or dig_signal[i]==1 or dig_signal[i]==-1:
                            signal.append((sin((2 * pi +j)* 100)*a1))
                        elif dig_signal[i]=='0' or dig_signal[i]==0:
                            signal.append(sin((2 * pi + j)* 100)*a2)
                    else:
                        if dig_signal[i]==-1:
                            signal.append((sin((2 * pi +j)* 100)*a1))
                        elif dig_signal[i]==1:
                            signal.append(sin((2 * pi + j)* 100)*a2)
            return signal    

    def fsk(self,dig_signal, f1=50, f2=100, sample=100,h=0):
        if len(dig_signal)==0:
            return []
        else:
            signal=[]
            for i in range(len(dig_signal)):
                for j in range(sample):
                    if h==0:
                        if dig_signal[i]=='1' or dig_signal[i]==1 or dig_signal[i]==-1:
                            signal.append((sin((2 * pi *j)* f1)))
                        elif dig_signal[i]=='0' or dig_signal[i]==0:
                            signal.append(sin((2 * pi + j)* f2))
                    else:
                        if dig_signal[i]==-1:
                            signal.append((sin((2 * pi *j)* f1)))
                        elif dig_signal[i]==1:
                            signal.append(sin((2 * pi + j)* f2))
            return signal                    
    def qam_mapping(self,dig_signal):
        #Define o mapeamento dos bits para símbolos QAM (8-QAM neste caso)

        symbol_map = {
            ('0', '0', '0'): (1, 1),
            ('0', '0', '1'): (1, -1),
            ('0', '1', '0'): (-1, 1),
            ('0', '1', '1'): (-1, -1),
            ('1', '0', '0'): (1/3, 1/3),
            ('1', '0', '1'): (1/3, -1/3),
            ('1', '1', '0'): (-1/3, 1/3),
            ('1', '1', '1'): (-1/3, -1/3)
        }
        symbols = []
        #Itera sobre o sinal digital em blocos de 3 bits
        for i in range(0, len(dig_signal), 3):
            #Obtém um bloco de 3 bits e mapeia para o símbolo correspondente
            bits = tuple(dig_signal[i:i + 3])
            symbols.append(symbol_map[bits])
        return symbols

    def qam8_modulation(self,dig_signal, sample=100):
        #Troca -1 por 0 para permitir o mapeamento na constelação QAM
        if isinstance(dig_signal,str)!=True:
            sinal=''
            for i in range(len(dig_signal)):
                char=f"{dig_signal[i]}"
                if char=="-1":
                    char="0"
                sinal=sinal+char
            dig_signal=sinal
        symbols=self.qam_mapping(dig_signal)
        signal=[]
        for symbol in symbols:
            for i in range(sample):
                signal.append(symbol[0] * cos(2 * pi+i/2) + symbol[0] * sin(2 * pi +i/2))
        return signal

