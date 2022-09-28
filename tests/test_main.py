import os
import sys
from pathlib import Path

sys.path.append(Path('..').absolute().as_posix() ) 

from analytics_pipeline.main import (
    parse_arguments,
    main
)




def test_main():
    args = None
    main(args)
    assert True == True