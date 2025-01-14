from camadaFisica import camada_fisica
from decoder_fisica import camadaFisicaDecoder
def bitstream_to_string(bitstream):
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
def string_to_bitstream(input_string):
        """
        Converte uma string em um bitstream (sequência de bits).

        Parâmetros:
            input_string (str): A string de entrada para conversão.

        Retorna:
            str: Uma string representando o bitstream.
        """
        try:
            # Codifica a string em bytes ASCII
            ascii_bytes = input_string.encode('ascii')
            # Converte cada byte em uma sequência binária de 8 bits
            bitstream = ''.join(f'{byte:08b}' for byte in ascii_bytes)
            return bitstream
        except UnicodeEncodeError as e:
            print(f"Erro: A string contém caracteres não ASCII. {e}")
            raise
decoder=camadaFisicaDecoder()
camadafisica=camada_fisica.camadaFisica()
word="ola mundo"
word=string_to_bitstream(word)
nrz=camadafisica.nrz_polar(word)
man=camadafisica.manchester(word)
bip=camadafisica.bipolar(word)
asf=camadafisica.ask(word)
fsk=camadafisica.fsk(word)
qam=camadafisica.qam8_modulation(word)

Dnrz=bitstream_to_string(decoder.decode_nrz_polar (nrz))  
Dman=bitstream_to_string(decoder.decode_manchester(man)) 
Dbip=bitstream_to_string(decoder.decode_bipolar   (bip)) 
Dasf=bitstream_to_string(decoder.decode_ask       (asf)) 
Dfsk=bitstream_to_string(decoder.decode_fsk       (fsk))
Dqam=bitstream_to_string(decoder.decode_qam8      (qam))
print(word)
print(f"nrz:{Dnrz}")
print(f"man:{Dman}")
print(f"bip:{Dbip}")
print(f"ask:{Dasf}")
print(f"fsk:{Dfsk}")
print(f"qam:{Dqam}")