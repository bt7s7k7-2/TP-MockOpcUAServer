import asyncio
import logging
from dataclasses import dataclass, field
from random import uniform
from urllib.parse import urlparse

from asyncua import Node, Server

from config import Configuration, VariableDefinition


@dataclass
class ServerInfo:
    server: Server
    ns_ids: dict[int, int] = field(default_factory=lambda: {})


@dataclass
class VariableInfo:
    variable: Node
    definition: VariableDefinition


async def main(config: Configuration):
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)

    variables: list[VariableInfo] = []
    servers: list[ServerInfo] = []

    def get_variable_value(variable_def: VariableDefinition):
        return uniform(variable_def.min, variable_def.max)

    logger.info("Constructing servers...")
    for server_def in config.servers:
        server = Server()
        info = ServerInfo(server)
        servers.append(info)
        logging.root.setLevel(logging.ERROR)
        await server.init()
        logging.root.setLevel(logging.DEBUG)
        uri = urlparse(f"opc.tcp://0.0.0.0:{server_def.port}")._replace(path=server_def.path)
        server.set_endpoint(uri.geturl())

        for i, namespace in enumerate(config.namespaces):
            info.ns_ids[i] = await server.register_namespace(namespace)

        for object_def in server_def.objects:
            node = await server.nodes.objects.add_object(info.ns_ids[object_def.ns], object_def.name)

            for variable_def in object_def.variables:
                variable = await node.add_variable(info.ns_ids[variable_def.ns], variable_def.name, get_variable_value(variable_def))
                variables.append(VariableInfo(variable, variable_def))

    logger.info("Starting servers...")
    for info in servers:
        await info.server.start()

    logger.info(f"Running, {len(variables)} variables across {len(servers)} servers")
    while True:
        await asyncio.sleep(1)

        for info in variables:
            await info.variable.set_value(get_variable_value(info.definition))


if __name__ == "__main__":
    config = Configuration.load("config.json")
    asyncio.run(main(config), debug=True)
