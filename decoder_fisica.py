from math import sin, cos, pi

class camadaFisicaDecoder:
    def _init_(self):
        pass

    def decode(self, Protocolos, sinal):
        bitMessage = sinal
        if Protocolos == "NRZ-Polar":
            wave = self.decode_nrz_polar(sinal)
            bitMessage = wave
        elif Protocolos == "Manchester":
            wave = self.decode_manchester(sinal)
            bitMessage = wave
        elif Protocolos == "Bipolar":
            wave = self.decode_bipolar(sinal)
            bitMessage = wave
        if Protocolos == "ASK":
            wave = self.decode_ask(sinal)
            bitMessage = wave
        elif Protocolos == "FSK":
            wave = self.decode_fsk(sinal)
            bitMessage = wave
        elif Protocolos == "8-QAM":
            wave = self.decode_qam8(sinal)
            bitMessage = wave
        bitMessage=self.bitstream_to_string(bitMessage)
        return bitMessage
    def bitstream_to_string(self,bitstream):
        """
        Converts a bitstream (sequence of bits) into a normal string.

        Parameters:
            bitstream (str): A string representing the bitstream (sequence of 0s and 1s).

        Returns:
            str: The decoded string.

        Raises:
            ValueError: If the bitstream length is not a multiple of 8 or contains invalid characters.
        """
        if len(bitstream) % 8 != 0:
            bitstream=list(bitstream)
            bitstream.pop(-1)
            bitstream="".join(bitstream)
        if len(bitstream) % 8 != 0:
            bitstream=list(bitstream)
            bitstream.pop(-1)
            bitstream="".join(bitstream)
        if not all(bit in '01' for bit in bitstream):
            raise ValueError("Bitstream contains invalid characters. Only '0' and '1' are allowed.")

        # Break the bitstream into chunks of 8 bits and convert each to a character
        byte_chunks = (bitstream[i:i+8] for i in range(0, len(bitstream), 8))
        decoded_string = ''.join(chr(int(byte, 2)) for byte in byte_chunks)
        return decoded_string
    # NRZ-Polar decoding
    def decode_nrz_polar(self, signal):
        # Decodificação corrigida para validar a entrada e processar somente sinais válidos
        if not all(isinstance(x, (int, float)) for x in signal):
            raise ValueError("Sinal contém valores inválidos. Deve ser numérico.")
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
    # FSK decoding function
    def decode_fsk(self, signal, f1=10, f2=200, sample=200):
        """
        Decodes an FSK signal into a bitstream.

        Parameters:
            signal (list or array): The input signal values.
            f1 (int): Frequency representing bit '1'.
            f2 (int): Frequency representing bit '0'.
            sample (int): Number of samples per bit.

        Returns:
            str: The decoded bitstream.
        """
        bit_stream = ""
        freq = []

        # Loop through the signal in chunks of 'sample' size
        for j in range(len(signal) // sample):
            bitFreq = []

            # Analyze the current sample chunk
            for i in range(sample):
                s = signal[i + j * sample]
                if -0.3 < s < 0.3:
                    bitFreq.append(i)

            # Calculate the average position of zero crossings or "active indices"
            if bitFreq:
                avg_position = sum(bitFreq) / len(bitFreq)
            else:
                avg_position = sample  # Default value for no crossings detected

            freq.append(avg_position)

        # Determine bit values based on the frequency threshold
        for avg in freq:
            if avg <= 95:  # Adjust threshold if necessary for your specific signal
                bit_stream += "0"
            else:
                bit_stream += "1"

        print(f"{bit_stream}")
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