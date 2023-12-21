from typer.core import TyperGroup


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, _):
        return self.commands.keys()
