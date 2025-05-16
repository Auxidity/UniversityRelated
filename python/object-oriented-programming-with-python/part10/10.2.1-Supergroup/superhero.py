class SuperHero:
    def __init__(self, name: str, superpowers: str):
        self.name = name
        # Split the superpowers string into a list, using a comma as the separator
        self.superpowers = superpowers.split(',') if superpowers else []

    def __str__(self):
        if not self.superpowers:  # Check if the list of superpowers is empty
            superpowers_str = "No superpowers"
        else:
            superpowers_str = ", ".join(self.superpowers).strip()
        return f"{self.name}, superpowers: {superpowers_str}"
