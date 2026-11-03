"""Fictional banking workflow; no accounts, credentials, storage or network."""
from security_config import AUDIT_LOGGING_ENABLED


def preview_transfer():
    print('DEMO ONLY: previewing a fictional transfer; no money moves.')
    if AUDIT_LOGGING_ENABLED:
        print('AUDIT DEMO: fictional transfer preview requested.')


if __name__ == '__main__':
    preview_transfer()
