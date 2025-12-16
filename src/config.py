from msgspec import Struct
import msgspec


class VariableDefinition(Struct):
    ns: int
    name: str
    min: float
    max: float


class ObjectDefinition(Struct):
    ns: int
    name: str
    variables: list[VariableDefinition]


class ServerDefinition(Struct):
    port: int
    path: str
    objects: list[ObjectDefinition]


class Configuration(Struct):
    namespaces: list[str]
    servers: list[ServerDefinition]

    @staticmethod
    def load(path: str):
        with open(path, "rb") as file:
            return msgspec.json.decode(file.read(), type=Configuration)


if __name__ == "__main__":
    with open("config-schema.json", "wb") as file:
        file.write(msgspec.json.encode(msgspec.json.schema(Configuration)))
