import logging
import sys

from lermontovization import transfiguration

if __name__ == '__main__':


    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        # filename="hw_8_walk_log_4.txt",
    )

    logger.debug('Интерпретатор:')
    logger.debug(sys.executable)
    