from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Thing(Element):
    pass


class Pile(Element):

    def __init__(self):
        super().__init__()
        self.name = None
        self.type = None
        self.capacity = 0
        self.items = []

    def init(self):
        for key, val_type in self.attributes.items():
            if key == "type":
                self.type = val_type.get("val")
            elif key == "enormity":
                cap = val_type.get("val")
                self.capacity = int(cap) if cap.isdigit() else cap
            else:
                self.name = key

        for child in self.children:
            if isinstance(child, Thing) and child.data:
                self.items.append(child.data.strip().replace("\n", ""))

        if not self.capacity and len(self.items):
            self.capacity = len(self.items)

    def diagnostics(self):
        d = []
        if not self.name:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                "Give a name to your pile like: <pile veryNicePile ...>"
            ))
        elif not self.type:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                f"What type of things wil go on this pile? eg: <pile {self.name} type=int ...>"
            ))
        elif not self.capacity:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                f"A pile must have a enormity: <pile {self.name} enormity=20 />"
            ))
        elif isinstance(self.capacity, int) and self.capacity < len(self.items):
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                f"How can {len(self.items)} items go on a pile with an enormity of {self.capacity}?!?!"
            ))
        return d

    def to_c(self, mapped_c):
        c = f"{self.type} {self.name}[{self.capacity}]"
        if self.items and isinstance(self.capacity, int):
            c += " = {" + ", ".join(self.items) + "}"
        mapped_c.add(
            c + ";\n",
            self
        )

        if self.items and not isinstance(self.capacity, int):
            i = 0
            for item in self.items:
                mapped_c.add(
                    f"{self.name}[{i}] = {item};\n",
                    self
                )
                i += 1
