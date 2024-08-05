import os
import json
import uuid
import traceback
from secret_exposure_analysis.core.logger import logger
from secret_exposure_analysis.core.models import Response
from secret_exposure_analysis.support.enums import (
    STDInput,
    MixedTypeEnum,
    ResponseMessage,
)


def run(
    target: str,
) -> Response:
    resp = Response()
    data = None
    file = os.path.join(
        os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        ),
        str(f"{uuid.uuid4()}.json"),
    )
    try:
        os.system(
            STDInput.GITLEAKS.value.format(
                target=target,
                output=file,
            )
        )
        with open(file, "r") as fp:
            data = json.load(fp, strict=False)
        if data:
            resp.success = MixedTypeEnum.SUCCESS.value
            resp.data = data
    except Exception as err:
        resp.message = ResponseMessage.GITLEAKS_MSG.value
        logger.error(err)
        logger.debug(traceback.format_exc())

    return resp
