import os
import typing


class Fork:
    def __init__(self, **paths_to_bools: bool):
        self.paths: list[str] = [
            key for key, value in paths_to_bools.items() if value is True
        ]

        if not self.paths:
            raise ValueError("No paths evaluated to True")

    def __call__(self, **paths_to_values: typing.Any) -> typing.Any:
        for path in self.paths:
            try:
                value = paths_to_values[path]
                if callable(value):
                    value = value()

                return value
            except KeyError:
                pass

        raise ValueError("No available path to a value")

    @staticmethod
    def get_env_var(*args):
        def get_env_var():
            return os.environ.get(*args)

        return get_env_var
