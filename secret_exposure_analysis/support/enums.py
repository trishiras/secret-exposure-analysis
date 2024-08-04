from enum import Enum


class MixedTypeEnum(Enum):
    # Boolean constants
    SUCCESS = True

    # String constants
    OUTPUT = "output"
    TMP = "tmp"


class ResponseMessage(Enum):
    GITLEAKS_MSG = "GITLEAKS did not return any response"


class STDInput(Enum):
    GITLEAKS = "gitleaks detect --source {target} --config /usr/src/app/config/config.toml --report-format json --report-path {output}"
