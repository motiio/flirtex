from enum import Enum

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.DEV, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.DEV, self.PRODUCTION)

    @property
    def get_env_log_level(self) -> str:
        if self in (self.LOCAL, self.DEV):
            return "DEBUG"
        elif self == self.TESTING:
            return "INFO"
        elif self == self.PRODUCTION:
            return "ERROR"

        return "ERROR"
