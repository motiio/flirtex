from dataclasses import asdict, dataclass


@dataclass
class BaseEntity:
    def model_dump(self, exclude: set[str] | None = None):
        if exclude is None:
            exclude = set()

        data = {key: value for key, value in asdict(self).items() if key not in exclude}

        for attr_name in dir(self):
            if isinstance(getattr(self.__class__, attr_name, None), property):
                value = getattr(self, attr_name)
                if attr_name not in exclude:
                    data[attr_name] = value

        return data
