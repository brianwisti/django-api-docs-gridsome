import dataclasses as dc
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

import parso
import rich
from rest_framework import serializers
from rich import print
from rich.logging import RichHandler
from rich.pretty import pprint

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__file__)


class ParamSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=2)
    name = serializers.CharField()
    annotation = serializers.CharField()

    def to_representation(self, instance):
        return {
            "prefix": "*" * instance.star_count,
            "name": instance.name.value,
            "annotation": instance.annotation,
        }


class DecoratorSerializer(serializers.Serializer):
    name = serializers.CharField()

    def to_representation(self, instance):
        name = instance.get_code().strip()

        return {
            "name": name,
        }


class FunctionSerializer(serializers.Serializer):
    name = serializers.CharField()
    docstring = serializers.CharField()
    params = ParamSerializer(many=True)
    decorators = serializers.ListField(child=DecoratorSerializer())

    def to_representation(self, instance):
        data = {
            "name": instance.name.value,
            "params": ParamSerializer(instance.get_params(), many=True).data,
        }

        decorators = [d for d in instance.get_decorators()]
        if decorators:
            data["decorators"] = [DecoratorSerializer(d).data for d in decorators]

        if doc_node := instance.get_doc_node():
            data["docstring"] = doc_node.value

        return data


class ClassSerializer(serializers.Serializer):
    name = serializers.CharField()
    docstring = serializers.CharField()
    methods = FunctionSerializer(many=True)
    classes = serializers.ListField()

    def to_representation(self, instance):
        class_serializer = self.__class__
        public_functions = [
            f
            for f in instance.iter_funcdefs()
            if not f.name.value.startswith("_") and not f.name.value.endswith("_")
        ]
        classes = list(instance.iter_classdefs())

        data = {
            "name": instance.name.value,
            "methods": FunctionSerializer(public_functions, many=True).data,
            "classes": class_serializer(classes, many=True).data,
        }

        if doc_node := instance.get_doc_node():
            data["docstring"] = doc_node.value

        decorators = [d for d in instance.get_decorators()]
        if decorators:
            data["decorators"] = [DecoratorSerializer(d).data for d in decorators]
        return data


@dc.dataclass
class ImportedName:
    paths: List[str]
    names: List[str]

    @classmethod
    def viaImportFrom(cls, node: parso.python.tree.ImportFrom):
        paths = [i.value for p in node.get_paths() for i in p]
        names = [n.value for n in node.get_defined_names()]

        return cls(paths, names)


class ModuleSerializer(serializers.Serializer):
    docstring = serializers.CharField()
    functions = FunctionSerializer(many=True)
    classes = serializers.ListSerializer(child=ClassSerializer())

    def to_representation(self, instance):
        public_functions = [
            f for f in instance.iter_funcdefs() if not f.name.value.startswith("_")
        ]
        classes = list(instance.iter_classdefs())
        data = {
            "functions": FunctionSerializer(public_functions, many=True).data,
            "classes": ClassSerializer(classes, many=True).data,
        }

        if doc_node := instance.get_doc_node():
            data["docstring"] = doc_node.value

        return data


def document_module(module_path: Path, library_path: Path):
    log.debug("Generating doc structure for %s", module_path)
    source = module_path.read_text()
    module = parso.parse(source).get_root_node()
    log.debug(module.dump())

    serialized_module = ModuleSerializer(module).data
    library_parent = str(library_path.parent)
    # TODO: make less awful
    package_path = (
        str(module_path)
        .replace(library_parent, "")
        .replace("/", ".")
        .replace(".py", "")
        .replace(".__init__", "")[1:]
    )

    data_path = Path("src/data/module") / f"{package_path}.json"
    log.debug(data_path)
    data_json = json.dumps(serialized_module, indent=2)
    log.debug(data_json)
    data_path.parent.mkdir(exist_ok=True, parents=True)
    data_path.write_text(data_json)
    log.info("Wrote %s info to %s", package_path, data_path)


def find_library(library_name: str) -> Path:
    for sys_path in sys.path:
        p = Path(sys_path)

        if not p.is_dir():
            continue

        for entry in p.iterdir():
            if entry.name == library_name:
                return entry

    raise ValueError(f"{library_name} not found in sys.path!")


def find_modules(library_path: Path) -> List[Path]:
    return [
        m
        for m in library_path.glob("**/*.py")
        if m.stat().st_size > 0 and m.name != "__main__.py"
    ]


def main():
    library_path = find_library("django")
    rich.print(library_path)
    modules = find_modules(library_path)
    log.info("%s non-empty modules found for %s", len(modules), library_path.name)

    for module in modules:
        document_module(module, library_path=library_path)


if __name__ == "__main__":
    main()
