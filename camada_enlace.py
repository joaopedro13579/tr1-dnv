import base64

class CamadaEnlace:
    def __init__(self):
        # Definição de constantes para flags e polinômio CRC
        self.FLAG = '1110111'
        self.ESC = '1101111'
        self.CRC16_POLY = 0x1021  # Polinômio CRC-16-CCITT

    def xor(self, a, b):
        # Realiza operação XOR bit a bit entre duas strings binárias
        return ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(a, b))

    def transmitir(self, quadro, enquadramento='insercao_bytes', deteccao_erro='crc', correcao_erro='hamming'):
        # Método principal para transmissão de dados
        # Aplica enquadramento, detecção de erro e correção de erro 
        metodos_enquadramento = {
            'insercao_bytes': self.enquadrar_insercao_bytes,
            'contagem_char': self.contagem_de_char
        }
        metodos_deteccao_erro = {
            'crc': self.adicionar_deteccao_erro,
            'paridade': self.adicionar_bit_deParidade,
            'crc16': lambda x: x + self.crc16(x)
        }
        metodos_correcao_erro = {
            'hamming': self.adicionar_correcao_erro,
            'none': lambda x: x
        }

        quadro_enquadrado = metodos_enquadramento[enquadramento](quadro)
        quadro_com_deteccao = metodos_deteccao_erro[deteccao_erro](quadro_enquadrado)
        quadro_com_correcao = metodos_correcao_erro[correcao_erro](quadro_com_deteccao)
        return base64.b64encode(quadro_com_correcao.encode()).decode()

    def receber(self, quadro, enquadramento='insercao_bytes', deteccao_erro='crc', correcao_erro='hamming'):
        # Método principal para recepção de dados
        # Aplica correção de erro, verifica erros e desenquadra o quadro recebido
        metodos_desenquadramento = {
            'insercao_bytes': self.desenquadrar_insercao_bytes,
            'contagem_char': self.desenquadrar_contagem_char
        }
        metodos_verificacao_erro = {
            'crc': self.verificar_erro,
            'paridade': self.verificar_paridade,
            'crc16': self.verificar_crc16
        }
        metodos_correcao_erro = {
            'hamming': self.corrigir_erro,
            'none': lambda x: x
        }

        quadro_decodificado = base64.b64decode(quadro.encode()).decode()
        quadro_corrigido = metodos_correcao_erro[correcao_erro](quadro_decodificado)
        quadro_verificado = metodos_verificacao_erro[deteccao_erro](quadro_corrigido)
        quadro_desenquadrado = metodos_desenquadramento[enquadramento](quadro_verificado)
        return quadro_desenquadrado

    def enquadrar(self, quadro):
        # Método genérico de enquadramento (usa inserção de bytes por padrão)
        return self.enquadrar_insercao_bytes(quadro)

    def desenquadrar(self, quadro):
        # Método genérico de desenquadramento (usa inserção de bytes por padrão)
        return self.desenquadrar_insercao_bytes(quadro)

    def enquadrar_insercao_bytes(self, quadro):
        # Enquadra o quadro usando o método de inserção de bytes
        resultado = self.FLAG
        for char in quadro:
            if char in (self.FLAG, self.ESC):
                resultado += self.ESC
            resultado += char
        resultado += self.FLAG
        return resultado

    def desenquadrar_insercao_bytes(self, quadro):
        # Desenquadra o quadro que foi enquadrado por inserção de bytes
        if not (quadro.startswith(self.FLAG) and quadro.endswith(self.FLAG)):
            raise ValueError("Quadro inválido: flags de início/fim ausentes")
        
        resultado = ""
        i = 1
        while i < len(quadro) - 1:
            if quadro[i] == self.ESC:
                i += 1
            resultado += quadro[i]
            i += 1
        return resultado

    def crc16(self, data):
        # Calcula o CRC-16 para os dados fornecidos
        crc = 0xFFFF  # Valor inicial
        for char in data:
            crc ^= (ord(char) << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ self.CRC16_POLY
                else:
                    crc <<= 1
            crc &= 0xFFFF  # Garante valor de 16 bits
        return format(crc, '016b')  # Retorna como string binária de 16 bits

    def adicionar_deteccao_erro(self, quadro):
        # Adiciona CRC ao quadro para detecção de erro
        crc = self.crc16(quadro)
        return f"{quadro}|{crc}"

    def verificar_erro(self, quadro):
        # Verifica se há erro no quadro usando CRC
        dados, crc_recebido = quadro.rsplit("|", 1)
        crc_calculado = self.crc16(dados)
        if crc_calculado == crc_recebido:
            return dados
        else:
            raise ValueError("Erro de CRC detectado")

    def adicionar_correcao_erro(self, quadro):
        # Adiciona código de Hamming para correção de erro
        return self.adicionar_hamming(quadro)

    def corrigir_erro(self, quadro):
        # Corrige erros usando o código de Hamming
        return self.corrigir_hamming(quadro)

    def adicionar_hamming(self, dados):
        # Adiciona bits de paridade Hamming aos dados
        resultado = ""
        for char in dados:
            codigo = self._calcular_hamming(ord(char))
            resultado += ''.join(map(lambda x: chr(x + 48), codigo))
        return resultado

    def corrigir_hamming(self, quadro):
        # Corrige erros usando o código de Hamming
        resultado = ""
        for i in range(0, len(quadro), 12):
            codigo = [ord(c) - 48 for c in quadro[i:i+12]]
            if len(codigo) == 12:
                byte_corrigido = self._corrigir_hamming(codigo)
                resultado += chr(byte_corrigido)
            else:
                resultado += ''.join(map(chr, [c + 48 for c in codigo[4:]]))
        return resultado

    def _calcular_hamming(self, byte):
        # Calcula os bits de paridade Hamming para um byte
        b = [int(bit) for bit in f"{byte:08b}"]
        p1 = b[0] ^ b[1] ^ b[3] ^ b[4] ^ b[6]
        p2 = b[0] ^ b[2] ^ b[3] ^ b[5] ^ b[6]
        p3 = b[1] ^ b[2] ^ b[3] ^ b[7]
        p4 = b[4] ^ b[5] ^ b[6] ^ b[7]
        return [p1, p2, p3, p4] + b

    def _corrigir_hamming(self, codigo):
        # Corrige um possível erro em um código Hamming
        p1, p2, p3, p4 = codigo[:4]
        b = codigo[4:]
        s1 = p1 ^ b[0] ^ b[1] ^ b[3] ^ b[4] ^ b[6]
        s2 = p2 ^ b[0] ^ b[2] ^ b[3] ^ b[5] ^ b[6]
        s3 = p3 ^ b[1] ^ b[2] ^ b[3] ^ b[7]
        s4 = p4 ^ b[4] ^ b[5] ^ b[6] ^ b[7]
        s = s1 + 2*s2 + 4*s3 + 8*s4
        if 0 < s <= 8:
            b[s-1] ^= 1
        return int(''.join(map(str, b)), 2)

    def contagem_de_char(self, input_string, max_size=16):
        # Implementa o método de contagem de caracteres para enquadramento
        if not all(char in '01' for char in input_string):
            raise ValueError("Input deve conter apenas '0' e '1'")
        length = len(input_string)
        if length <= max_size:
            binary_length = format(length, '08b')
            result = '0' + binary_length + input_string
        else:
            chunks = [input_string[i:i+max_size] for i in range(0, length, max_size)]
            result = '1' + format(len(chunks), '08b')
            for chunk in chunks:
                result += format(len(chunk), '08b') + chunk
        return result

    def adicionar_bit_deParidade(self, input_string):
        # Adiciona um bit de paridade à string de entrada
        if not all(char in '01' for char in input_string):
            raise ValueError("Input deve conter apenas '0' e '1'")
        num_ones = input_string.count('1')
        parity_bit = '0' if num_ones % 2 == 0 else '1'
        result = input_string + parity_bit
        return result

    def verificar_paridade(self, quadro):
        # Verifica a paridade do quadro
        data = quadro[:-1]
        parity_bit = quadro[-1]
        
        count_ones = data.count('1')
        
        if (count_ones % 2 == 0 and parity_bit == '0') or (count_ones % 2 == 1 and parity_bit == '1'):
            return data
        else:
            raise ValueError("Verificação de paridade falhou")

    def verificar_crc16(self, quadro):
        # Verifica o CRC-16 do quadro
        data = quadro[:-16]
        received_crc = quadro[-16:]
        
        calculated_crc = self.crc16(data)
        
        if calculated_crc == received_crc:
            return data
        else:
            raise ValueError("Verificação CRC16 falhou")

    def desenquadrar_contagem_char(self, quadro):
        # Desenquadra o quadro que foi enquadrado pelo método de contagem de caracteres
        if quadro[0] == '0':  # Chunk único
            length = int(quadro[1:9], 2)
            return quadro[9:9+length]
        else:  # Múltiplos chunks
            num_chunks = int(quadro[1:9], 2)
            result = ""
            index = 9
            for _ in range(num_chunks):
                chunk_length = int(quadro[index:index+8], 2)
                index += 8
                result += quadro[index:index+chunk_length]
                index += chunk_length
            return result
