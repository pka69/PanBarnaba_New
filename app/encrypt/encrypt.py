from string import printable


def cleanString(input_text):
    output = ''.join(char for char in input_text if char in printable)
    output = output.replace("  ", " ").strip()
    return output


def removeAccents(input_text):
    strange ='ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
    ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
    translator = str.maketrans(strange, ascii_replacements)
    return input_text.translate(translator)


class Encryptor():
    def __init__(self, to_encrypt, encrypt_key):
        self.key = cleanString(encrypt_key)
        self.to_encrypt = cleanString(removeAccents(to_encrypt)).lower()
        return

    def convert(self, input_text):
        raise NotImplementedError("Please Implement this method")

    def getEncrypted(self):
        return self.convert(self.to_encrypt)

    @classmethod
    def isCorrect(cls, encrypt_key, to_encrypt, to_check):
        encryptor = cls(to_encrypt, encrypt_key)
        encrypt = encryptor.getEncrypted()
        check = encryptor.convert(to_check)
        return encrypt == check


class Sylabowy(Encryptor):
    GADERYPOLUKI = [
        'GADERYPOLUKI',
        'POLITYKARENU',
        'MOTYLECUDAKI',
        'KONIECMATURY',
        'KACEMINUTOWY',
        'KULARYMINETO',
        'HUDEKAROLINY',
        'KALINOWEBUTY',
    ]

    def __init__(self, to_encrypt, encrypt_key):
        if encrypt_key != removeAccents(encrypt_key):
            raise ValueError("Wrong key - no accents accepted")
        if (len(encrypt_key) % 2) != 0:
            raise ValueError("Wrong key - length must be even")
        if any([encrypt_key.count(item) > 1 for item in encrypt_key]):
            raise ValueError("Wrong key - any letter shoudn't be repeated")
        super().__init__(to_encrypt, encrypt_key)
        self.key2 = ''.join([self.key[item + self.corresponding(item)] for item in range(len(self.key))])
        self.translator = str.maketrans(self.key.lower(), self.key2.lower())
        return

    def getKey(self):
        result = ''
        for i in range(len(self.key)):
            result += self.key[i]
            if i % 2 == 1:
                result += "-"
        return result[:-1]

    def convert(self, input_text):
        output = cleanString(removeAccents(input_text)).lower().translate(self.translator)
        return output

    def convertCaseSensitive(self, input_text):
        result = cleanString(removeAccents(input_text)).lower().translate(self.translator)
        output = ''
        for i in range(len(input_text)):
            output += result[i].upper() if input_text[i].isupper() else result[i]
        return output

    def corresponding(self, number):
        return -1 if (number % 2) == 1 else 1


class Divider(Encryptor):
    def __init__(self, to_encrypt, encrypt_key=''):
        super().__init__(to_encrypt, 'abcdefghijklmnoqprstuvwyz')
        self.key2 = [
            str(self.key.index(item) % 5 + 1) + "/" + str(self.key.index(item) // 5 + 1) for item in
            self.key
        ]

    def convert(self, input_text):
        output = ''
        for item in cleanString(removeAccents(input_text)).lower():
            if item in self.key:
                output += self.key2[self.key.index(item)] + " " 
            else:
                output += item + " "
        return output[:-1]  


class Brownie(Encryptor):
    def __init__(self, to_encrypt, encrypt_key=''):
        super().__init__(to_encrypt, 'abcdefghijklmnoprstuwyz')
        self.key2 = to_encrypt

    def convert(self, input_text):
        return cleanString(removeAccents(input_text)).lower().replace("  ", " ")

class Kaczor(Encryptor):
    KACZOR = [
        'klmn    ',
        'ab      ',
        'cdefghij',
        'z       ',
        'op      ',
        'rstuwy  '
    ]

    def __init__(self, to_encrypt, encrypt_key=''):
        super().__init__(to_encrypt, 'abcdefghijklmnopqrstuvwyz')
        self.key2 = {}
        for item in self.KACZOR:
            for i, char in enumerate(item, 1):
                if char != " ": self.key2[char] = '{}{}'.format(item[0], i)

    def convert(self, input_text):
        output = ''
        for item in cleanString(removeAccents(input_text)).lower():
            output += self.key2.get(item, item) + " "
        return output[:-1]

KEYS = {
    'gaderypoluki': Sylabowy,
    'brownie': Brownie,
    'divider': Divider,
    'kaczor': Kaczor,
}


def isCorrect(key, encrypt_key, to_encrypt, to_check):
    return KEYS[key].isCorrect(encrypt_key, to_encrypt, to_check)

def getEncryptor(key, encrypt_key, to_encrypt):
    return KEYS[key](to_encrypt, encrypt_key)