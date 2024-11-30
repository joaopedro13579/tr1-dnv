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
    def ask(self, dig_signal, f=10000, sample=1000,h=0):
        if len(dig_signal)==0:
            return []
        if len(dig_signal)>=400:
            Signal=[]
            part_length = len(dig_signal) // 6

            # Calculate any remaining characters after dividing into 4 parts
            remainder = len(dig_signal) % 6

            # Initialize a list to store the 4 parts
            parts = []
            start = 0

            for i in range(6):
                # If there are remaining characters, add one extra to the current part
                end = start + part_length + (1 if i < remainder else 0)

                # Append the current part to the list of parts
                parts.append(dig_signal[start:end])

                # Update the start index for the next part
                start = end
            for i in range(len(parts)):
                dig_signal=parts[i]
                #Calcula o número de amostras por bit, baseado no número total de amostras e no comprimento do sinal digital
                samples_per_bit = sample // len(dig_signal)
                signal = []
                if h==1:
                    n=100
                else:
                    n=1
                #Modula a onda portadora com base nos bits de dados
                for bit in dig_signal:
                    for j in range(samples_per_bit):
                        #Calcula o tempo atual como uma fração do número total de amostras
                        time = j / sample

                        #Se o bit é 1, adiciona uma onda senoidal à lista de sinais
                        if bit == 1:
                            signal.append(sin(2 * pi * f * time)*19000000000*len(dig_signal)*n)
                        else:
                            #Se o bit é 0, adiciona zero à lista de sinais (amplitude zero para o bit 0)
                            signal.append(0)
                Signal=Signal+signal
            return Signal

        else:    
            #Calcula o número de amostras por bit, baseado no número total de amostras e no comprimento do sinal digital
            samples_per_bit = sample // len(dig_signal)
            signal = []

            #Modula a onda portadora com base nos bits de dados
            for bit in dig_signal:
                for j in range(samples_per_bit):
                    #Calcula o tempo atual como uma fração do número total de amostras
                    time = j / sample

                    #Se o bit é 1, adiciona uma onda senoidal à lista de sinais
                    if bit == 1:
                        signal.append(sin(2 * pi * f * time)*190000000000*len(dig_signal))
                    else:
                        #Se o bit é 0, adiciona zero à lista de sinais (amplitude zero para o bit 0)
                        signal.append(0)

            #Retorna o sinal modulado
            return signal

    def fsk(self,dig_signal, f1=1000, f2=10000, sample=1000,h=0):
        if len(dig_signal)==0:
            return []
        if len(dig_signal)>100:
            Signal=[]
            part_length = len(dig_signal) // 6

            # Calculate any remaining characters after dividing into 4 parts
            remainder = len(dig_signal) % 6

            # Initialize a list to store the 4 parts
            parts = []
            start = 0

            for i in range(6):
                # If there are remaining characters, add one extra to the current part
                end = start + part_length + (1 if i < remainder else 0)

                # Append the current part to the list of parts
                parts.append(dig_signal[start:end])

                # Update the start index for the next part
                start = end
            for i in range(len(parts)):
                dig_signal=parts[i]
                #Calcula o número de amostras por bit, baseado no número total de amostras e no comprimento do sinal digital
                samples_per_bit = sample // len(dig_signal)
                signal = []
                if h==1:
                    n=10
                else:
                    n=1
                #Itera sobre cada bit no sinal digital
                for bit in dig_signal:
                    #Para cada bit, gera uma sequência de amostras
                    for j in range(samples_per_bit):
                        #Calcula o tempo atual como uma fração do número total de amostras
                        time = j / sample

                        #Se o bit é 1, usa a frequência f2 para gerar a onda senoidal
                        if bit == 1:
                            signal.append(sin(2 * pi * f2 * time)*190000000000*len(dig_signal)*n)
                        else:
                            #Se o bit é 0, usa a frequência f1 para gerar a onda senoidal
                            signal.append(sin(2 * pi * f1 * time)*190000000000*len(dig_signal)*n)
                Signal=Signal+signal
            return Signal

        else:
            #Calcula o número de amostras por bit, baseado no número total de amostras e no comprimento do sinal digital
            samples_per_bit = sample // len(dig_signal)
            signal = []

            #Itera sobre cada bit no sinal digital
            for bit in dig_signal:
                #Para cada bit, gera uma sequência de amostras
                for j in range(samples_per_bit):
                    #Calcula o tempo atual como uma fração do número total de amostras
                    time = j / sample

                    #Se o bit é 1, usa a frequência f2 para gerar a onda senoidal
                    if bit == 1:
                        signal.append(sin(2 * pi * f2 * time)*170000000000*len(dig_signal))
                    else:
                        #Se o bit é 0, usa a frequência f1 para gerar a onda senoidal
                        signal.append(sin(2 * pi * f1 * time)*170000000000*len(dig_signal))

            #Retorna o sinal modulado
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

    def qam8_modulation(self,dig_signal, sample=500):
        #Troca -1 por 0 para permitir o mapeamento na constelação QAM
        if isinstance(dig_signal,str)!=True:
            sinal=''
            for i in range(len(dig_signal)):
                char=f"{dig_signal[i]}"
                if char=="-1":
                    char="0"
                sinal=sinal+char
            dig_signal=sinal
        if len(dig_signal)>500:
            Signal=[]
            part_length = len(dig_signal) // 6

            # Calculate any remaining characters after dividing into 4 parts
            remainder = len(dig_signal) % 6

            # Initialize a list to store the 4 parts
            parts = []
            start = 0

            for i in range(6):
                # If there are remaining characters, add one extra to the current part
                end = start + part_length + (1 if i < remainder else 0)

                # Append the current part to the list of parts
                parts.append(dig_signal[start:end])

                # Update the start index for the next part
                start = end
            for i in range(len(parts)):
                dig_signal=parts[i]
                if (int(len(dig_signal))%3!=0):
                    while (int(len(dig_signal))%3!=0):
                        dig_signal=dig_signal+"0"
                        print("numero nao multiplo de 3")
                dig_signal = [0 if x == -1 else x for x in dig_signal]
                #Mapeia o sinal digital para símbolos QAM usando a função qam_mapping
                symbols = self.qam_mapping(dig_signal)
                if symbols!=[]:
                #Calcula o número de amostras por símbolo
                    samples_per_symbol = sample // len(symbols)
                else:
                    samples_per_symbol =0
                signal = []
                #Gera o sinal modulador para cada símbolo
                for symbol in symbols:
                    I, Q = symbol
                    for j in range(samples_per_symbol):
                        #Calcula o tempo atual como uma fração do número total de amostras
                        time = j / sample
                        #Calcula o valor do sinal modulador para a amostra atual
                        signal.append(I * cos(2 * pi * time) + Q * sin(2 * pi * time))
                Signal=Signal+signal
            return Signal

        else:
            if (int(len(dig_signal))%3!=0):
                while (int(len(dig_signal))%3!=0):
                    dig_signal=dig_signal+"0"
                    print("numero nao multiplo de 3")
            dig_signal = [0 if x == -1 else x for x in dig_signal]

            #Mapeia o sinal digital para símbolos QAM usando a função qam_mapping
            symbols = self.qam_mapping(dig_signal)
            if symbols!=[]:
            #Calcula o número de amostras por símbolo
                samples_per_symbol = sample // len(symbols)
            else:
                samples_per_symbol =0
            signal = []

            #Gera o sinal modulador para cada símbolo
            for symbol in symbols:
                I, Q = symbol
                for j in range(samples_per_symbol):
                    #Calcula o tempo atual como uma fração do número total de amostras
                    time = j / sample
                    #Calcula o valor do sinal modulador para a amostra atual
                    signal.append(I * cos(2 * pi * time) + Q * sin(2 * pi * time))

            #Retorna o sinal modulado
            return signal

