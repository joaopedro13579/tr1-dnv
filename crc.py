def crc32(self, data: str) -> str:
        # Adiciona zeros ao final da string de dados
        polynomial = "10000010000001100000010000100001"
        data_str = data
        data = data + '0' * (len(polynomial) - 1)
        
        # Converte os dados e o polinômio em listas de inteiros
        data = list(map(int, data))
        polynomial = list(map(int, polynomial))
        
        # Realiza a divisão polinomial
        for i in range(len(data) - len(polynomial) + 1):
            if data[i] == 1:
                for j in range(len(polynomial)):
                    data[i + j] ^= polynomial[j]
        
        # O resto da divisão é a CRC
        crc = ''.join(map(str, data[-(len(polynomial) - 1):]))
        return data_str+crc
