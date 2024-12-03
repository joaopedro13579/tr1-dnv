from camada_fisica import camadaFisica
import decoder

class tester:
    def __init__(self):
        self.decode=decoder.camadaFisicaDecoder()
        self.coder=camadaFisica()
    def test(self,var="0"):
        num=self.coder.nrz_polar(var)
        if self.decode.decode_nrz_polar(num)==var:
            self.nrz_polar=True
        else:
            self.nrz_polar=False
        num=self.coder.manchester(var)
        if self.decode.decode_manchester(num)==var:
            self.manchester=True
        else:
            self.manchester=False
        num=self.coder.bipolar(var)
        if self.decode.decode_bipolar(num)==var:
            self.bipolar=True
        else:
            self.bipolar=False
        num=self.coder.ask(var)
        if self.decode.decode_ask(num)==var:
            self.ask=True
        else:
            self.ask=False
        num=self.coder.fsk(var)
        if self.decode.decode_fsk(num)==var:
            self.fsk=True
        else:
            self.fsk=False
        num=self.coder.qam8_modulation(var)
        if self.decode.decode_qam8(num)==var+"0" or self.decode.decode_qam8(num)==var:
            self.qam=True
        else:
            self.qam=False
    