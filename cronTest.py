# test file for cron job inside container
import time
import logging

logging.basicConfig(filename='/app/background.log',
                    filemode='a', level=logging.DEBUG,
                    format="%(message)s")

for i in range(5):
    time.sleep(1)
    logging.info(f"Log {i}")
