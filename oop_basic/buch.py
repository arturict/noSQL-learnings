class Buch:
    def __init__(self, titel, autor, isbn, preis, erfassuungsZeitpunkt=None, ausleihbar=True, _id=None):
        self._id = _id
        self.titel = titel
        self.autor = autor
        self.isbn = isbn
        self.preis = preis
        self.erfassuungsZeitpunkt = erfassuungsZeitpunkt
        self.ausleihbar = ausleihbar
    
    def __str__(self):
        return f"{self.titel} von {self.autor} - {self.preis} CHF"