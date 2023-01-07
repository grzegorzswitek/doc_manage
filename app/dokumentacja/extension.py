class Plural:
    def __init__(self, ile, jeden, dwa_trzy_cztery, wiele, *args, **kwargs):
        self.jeden = jeden
        self.dwa_trzy_cztery = dwa_trzy_cztery
        self.wiele = wiele

        try:
            self.ile = int(ile)
        except ValueError:
            raise ValueError("Należy podać liczbę")

        self.bezwzgledna = abs(self.ile)

    def __str__(self):
        if self.bezwzgledna == 1:
            return f"{self.ile} {self.jeden}"

        if self.bezwzgledna % 100 in range(12, 15):
            return f"{self.ile} {self.wiele}"

        if str(self.bezwzgledna)[-1] in ("2", "3", "4"):
            return f"{self.ile} {self.dwa_trzy_cztery}"

        return f"{self.ile} {self.wiele}"
