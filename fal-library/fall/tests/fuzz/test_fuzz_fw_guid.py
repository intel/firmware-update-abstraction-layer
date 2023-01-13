import atheris

with atheris.instrument_imports():
  from fall.firmware_updater import FirmwareUpdater
  from fall.result_constants import INPUT_VALIDATION_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE, \
      UNABLE_FIND_MATCHING_PLATFORM, UPGRADE_CHECK_FAILURE, INSTALL_FAILURE
  import sys


@atheris.instrument_func
def TestOneInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data = fdp.ConsumeString(4000)
    result = FirmwareUpdater().update(path_to_update_package='/etc/environment', capsule_release_date='2022-01-01',
                                      bios_vendor='Intel Corp.', guid=data, autofill_platform_info=True)
    if result in [INPUT_VALIDATION_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE, UNABLE_FIND_MATCHING_PLATFORM,
                  UPGRADE_CHECK_FAILURE, INSTALL_FAILURE]:
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
