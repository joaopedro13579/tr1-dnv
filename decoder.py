from math import sin, cos, pi
from camada_fisica import camadaFisica
class camadaFisicaDecoder:
    def __init__(self):
        pass
    def decode(self,Protocolos,sinal):
        bitMessage=sinal
        if Protocolos == "NRZ-Polar":
            wave=self.decode_nrz_polar(sinal)
            bitMessage=wave
            n=1
        elif Protocolos == "Manchester":
            wave=self.decode_manchester(sinal)
            bitMessage=wave
        elif Protocolos == "Bipolar":
            wave=self.decode_bipolar(sinal)
            bitMessage=wave
        if  Protocolos == "ASK":
            wave=self.decode_ask(sinal)
            bitMessage=wave
        elif Protocolos == "FSK":
            wave=self.decode_fsk(sinal)
            bitMessage=wave
        elif Protocolos == "8-QAM":
            wave=self.decode_qam8(sinal)
            bitMessage=wave
        return bitMessage

    # NRZ-Polar decoding
    def decode_nrz_polar(self, signal):
        sinal=[]
        for i in signal:
            sinal.append(int(i))
        signal=sinal
        return "".join("1" if x > 0 else "0" for x in signal)

    # Manchester decoding
    def decode_manchester(self, signal):
        bit_stream = ""
        for i in range(0, len(signal), 2):
            if signal[i] < signal[i + 1]:  # Low-to-high
                bit_stream += "0"
            else:  # High-to-low
                bit_stream += "1"
        return bit_stream

    # Bipolar decoding
    def decode_bipolar(self, signal):
        bit_stream = ""
        for x in signal:
            if x == 0:
                bit_stream += "0"
            else:
                bit_stream += "1"
        return bit_stream

    # ASK decoding
    def decode_ask(self, signal, a1=1, a2=1.5, sample=100):
        bit_stream = ""
        for i in range(0, len(signal), sample):
            amplitude = max(signal[i:i + sample])
            if abs(amplitude - a1) < abs(amplitude - a2):
                bit_stream += "1"
            else:
                bit_stream += "0"
        return bit_stream


    # FSK decoding
    def decode_fsk(self, signal, f1=50, f2=100, sample=200):
        bit_stream = ""
        bitFreq=[]
        freq=[]
        for j in range(int(len(signal)/sample)):
            for i in range(sample):
                s=signal[i+j*sample]
                if s>-0.3 and s<0.3:
                    bitFreq.append(i)
            freq.append(bitFreq)
            bitFreq=[]
        for frequencia in freq:
            bit=sum(frequencia)/100

            if bit<=34:
                bit_stream="1"+bit_stream
            else:
                bit_stream="0"+bit_stream
        return bit_stream



    # 8-QAM decoding
    def decode_qam8(self, signal, sample=200):
        symbols=[(1, 1),(1, -1),(-1, 1),(-1, -1),(1 / 3, 1 / 3),(1 / 3, -1 / 3),(-1 / 3, 1 / 3),(-1 / 3, -1 / 3)]
        sinal=signal
        sinais=[]
        bit=[]
        for j in range(int(len(sinal)/sample)):
            for i in range(sample):
                bit.append(sinal[i+sample*j])
            sinais.append(str(bit))
            bit=[]

        signal=[]
        functions=[]
        for symbol in symbols:
            for i in range(sample):
                signal.append(symbol[0] * cos(2 * pi+i/2) + symbol[1] * sin(2 * pi +i/2))
            functions.append(signal)
            signal=[]

        symbol_map = {
            str(functions[0]): "000",
            str(functions[1]): "001",
            str(functions[2]): "010",
            str(functions[3]): "011",
            str(functions[4]): "100",
            str(functions[5]): "101",
            str(functions[6]): "110",
            str(functions[7]): "111"
        }
        bit_stream=""
        for bit in sinais:
            bit_stream=bit_stream+symbol_map[bit]
        return bit_stream
