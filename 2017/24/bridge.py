import a_star


class Bridge(a_star.State):
    def __init__(self, used_components, unused_components, available_port=0) -> None:
        self.used_components = used_components
        self.unused_components = unused_components
        self.strength = sum([c.strength() for c in used_components])
        self.available_port = available_port
        self.length = len(self.used_components)

    def __lt__(self, other):
        return self.strength < other.strength

    def is_complete(self):
        return not len(self.unused_components)

    def is_valid(self):
        if not len(self.used_components):
            return True
        return self.available_port in self.used_components[-1]

    def __repr__(self) -> str:
        return "--".join([c.__repr__() for c in self.used_components])

    def all_possible_next_states(self):
        for _i, u in enumerate(self.unused_components):
            if self.available_port in u:
                new_available_port = (
                    u.pin_a if self.available_port == u.pin_b else u.pin_b
                )
                yield Bridge(
                    [*self.used_components, u],
                    [c for c in self.unused_components if c is not u],
                    available_port=new_available_port,
                )
