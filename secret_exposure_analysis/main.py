import os
import json
from argparse import Namespace
from secret_exposure_analysis.services import gitleaks
from secret_exposure_analysis.core.logger import logger
from secret_exposure_analysis.core.input import parse_args
from secret_exposure_analysis.support.enums import MixedTypeEnum


class SecretExposureAnalysis(object):
    def __init__(
        self,
        arguments: Namespace,
    ):
        self.data = {}
        self.target = arguments.target
        self.output_via = arguments.output_via
        self.webhook = arguments.webhook
        self.output_file_path = arguments.output_file_path

    def run(self):

        logger.info(
            f"Started generating secret exposure analysis report for target :- {self.target}"
        )

        if self.webhook:
            logger.info(f"Webhook URL :- {self.webhook}")

        if self.output_file_path:
            logger.info(f"Output file path :- {self.output_file_path}")

        output_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.OUTPUT.value,
        )
        tmp_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        )
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        gitleaks_response = gitleaks.run(
            target=self.target,
        )

        if gitleaks_response.success:
            self.data = gitleaks_response.data
        else:
            logger.error(gitleaks_response.message)

        with open(self.output_file_path, "w") as fp:
            json.dump(self.data, fp, indent=4, default=str)

        logger.info(
            f"Finished generating secret exposure analysis report for target :- {self.target}"
        )


def main():

    arguments, unknown = parse_args()

    secret_exposure_analysis = SecretExposureAnalysis(arguments=arguments)
    secret_exposure_analysis.run()
