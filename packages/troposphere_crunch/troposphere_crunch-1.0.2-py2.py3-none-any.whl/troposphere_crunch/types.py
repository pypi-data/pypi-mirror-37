import os
from dataclasses import dataclass, field
from typing import Collection, Container, List

from troposphere.constants import US_WEST_2


@dataclass
class Stack:
    module: Container
    output_dir: str
    capabilities: Collection = tuple()  # noqa
    region: str = US_WEST_2
    parameters: List[dict] = field(default_factory=list)

    @property
    def name(self) -> str:
        '''
        Convert python module path name to a Cloudformation-friendly string
        which is regionalized

        ex. "aws_klardotsh.iam" with default region becomes "us-west-2-iam"
        '''

        return '{}-{}'.format(
            self.region,
            self.module.__name__.split('.', 1)[1].replace('.', '-'),
        )

    @property
    def json_filename(self) -> str:
        return os.path.join(
            self.output_dir,
            f'{self.name}.json',
        )
