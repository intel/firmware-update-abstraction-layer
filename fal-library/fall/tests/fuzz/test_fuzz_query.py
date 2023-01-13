import atheris

with atheris.instrument_imports():
    from fall.firmware_updater import FirmwareUpdater
    from fall.result_constants import QUERY_SUCCESS, UNSUPPORTED_OS_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE

    import sys


@atheris.instrument_func
def TestOneInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data = fdp.ConsumeString(sys.maxsize)
    result = FirmwareUpdater().query(option_type=data)
    if result in [QUERY_SUCCESS, UNSUPPORTED_OS_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE]:
        return

    input_type = str(type(data))
    codepoints = [hex(ord(x)) for x in data]
    sys.stdout.write(f"Input was {input_type}: {data}\nCodepoints: {codepoints}")
    raise


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
