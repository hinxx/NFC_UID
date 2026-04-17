if __package__:
    from .nfc_uid import main
else:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from nfc_uid.nfc_uid import main


if __name__ == "__main__":
    raise SystemExit(main())
