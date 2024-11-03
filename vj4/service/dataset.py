import collections
import copy
import io
import json
import logging
from enum import Enum
from zipfile import ZipFile

from vj4.service import bus
from vj4.model.adaptor import problem
from vj4.model import fs

_logger = logging.getLogger(__name__)

_memory_limit_in_kb = 1024 * 1024
_time_limit_in_ms = 15000
input_path_prefix = "Input/"
output_path_prefix = "Output/"


class ValidatorType(Enum):
    FileValidator = 1
    LineValidator = 2
    WordValidator = 3
    FloatValidator = 4
    CustomValidator = 5


class DatasetError(Exception):
    pass


def _get_config(zip):
    try:
        with zip.open("Config.json") as f:
            return json.load(f)
    except KeyError:
        raise DatasetError("Config.json not found.")
    except json.JSONDecodeError:
        raise DatasetError("Failed to parse Config.json.")


def _validate_validator_type(zip: ZipFile, config) -> None:
    if "ValidatorType" not in config:
        raise DatasetError("ValidatorType not found.")
    if config["ValidatorType"] not in [vt.value for vt in ValidatorType]:
        raise DatasetError("Invalid ValidatorType.")
    if config["ValidatorType"] == ValidatorType.CustomValidator.value:
        if "ValidatorSourceCode" not in config:
            raise DatasetError(
                "ValidatorType is CustomValidator but ValidatorSourceCode is null or whitespace."
            )
        if "ValidatorLanguage" not in config:
            raise DatasetError(
                "ValidatorType is CustomValidator but ValidatorLanguage is null or whitespace."
            )
        if not zip.getinfo(config["ValidatorSourceCode"]):
            raise DatasetError(
                f"ValidatorType is CustomValidator but ValidatorSourceCode file not found. ValidatorSourceCode file is {config['ValidatorSourceCode']}."
            )

    if config["ValidatorType"] == ValidatorType.FloatValidator.value:
        if "Epsilon" not in config:
            raise DatasetError("ValidatorType is FloatValidator but Epsilon is null.")
        if not isinstance(config["Epsilon"], float):
            raise DatasetError("Epsilon must be a float.")


def _is_power_of_two(n: int) -> bool:
    return n != 0 and (n & (n - 1)) == 0


def _validate_testcases(zip: ZipFile, config) -> None:
    input_files = [f for f in zip.namelist() if f.startswith(input_path_prefix)]
    output_files = [f for f in zip.namelist() if f.startswith(output_path_prefix)]

    # remove the folder entry
    input_files = [f for f in input_files if f != input_path_prefix]
    output_files = [f for f in output_files if f != output_path_prefix]

    if len(input_files) == 0:
        raise DatasetError("No input files found in Input folder.")
    if len(output_files) == 0:
        raise DatasetError("No output files found in Output folder.")
    if len(input_files) != len(output_files):
        raise DatasetError(
            f"Not the same number of Input/Output files. {len (input_files)} Input files and {len(output_files)} Output files."
        )

    if "MemoryLimit" not in config:
        raise DatasetError("MemoryLimit is missing.")

    if "TimeLimit" not in config:
        raise DatasetError("TimeLimit is missing.")

    memory_limit = config.get("MemoryLimit")

    if not isinstance(memory_limit, int):
        raise DatasetError("MemoryLimit is not a number.")

    time_limit = config.get("TimeLimit")

    if not isinstance(time_limit, int):
        raise DatasetError("TimeLimit is not a number.")

    if memory_limit <= 0:
        raise DatasetError("MemoryLimit must be greater than 0.")

    if time_limit <= 0:
        raise DatasetError("TimeLimit must be greater than 0.")

    if memory_limit > _memory_limit_in_kb:
        raise DatasetError(f"MemoryLimit must be less than {_memory_limit_in_kb}kb.")

    if time_limit > _time_limit_in_ms:
        raise DatasetError(f"TimeLimit must be less than {_time_limit_in_ms}ms.")

    if not _is_power_of_two(memory_limit):
        raise DatasetError("MemoryLimit must be a power of two.")

    if "TestCases" not in config:
        raise DatasetError("TestCases is missing.")

    if not isinstance(config["TestCases"], list):
        raise DatasetError("TestCases must be an array.")

    if len(config["TestCases"]) != len(input_files):
        raise DatasetError(
            "TestCases length must be the same as the number of input files."
        )

    total_score = 0

    for testcase in config["TestCases"]:
        if "Input" not in testcase:
            raise DatasetError("Input is missing in a testcase.")
        if "Output" not in testcase:
            raise DatasetError("Output is missing in a testcase.")
        input_file = f"{input_path_prefix}{testcase['Input']}"
        output_file = f"{output_path_prefix}{testcase['Output']}"

        if input_file not in input_files:
            raise DatasetError(f"Input file {input_file} not found.")
        if output_file not in output_files:
            raise DatasetError(f"Output file {output_file} not found.")

        score = testcase.get("Score")

        if score is None:
            raise DatasetError("Score is missing in a testcase.")

        if not isinstance(score, int):
            raise DatasetError("Score must be an integer.")

        if score < 0:
            raise DatasetError("Score must be greater than or equal to 0.")

        total_score += score

    if total_score != 100:
        raise DatasetError("Total score must be 100.")

    if "Samples" in config:
        if not isinstance(config["Samples"], list):
            raise DatasetError("Samples must be an array.")

        for sample in config["Samples"]:
            if not isinstance(sample, int):
                raise DatasetError("Sample Number must be an integer.")

            if sample < 0 or sample >= len(input_files):
                raise DatasetError(
                    "Sample Number must be in the range of 0 to the number of testcases."
                )


async def _validate_dataset(domain_id, pid, zip):
    config = _get_config(zip)
    _validate_validator_type(zip, config)
    _validate_testcases(zip, config)
    memory_limit = config.get("MemoryLimit")
    time_limit = config.get("TimeLimit")
    await problem.edit(
        domain_id,
        pid,
        memory_limit_kb=memory_limit,
        time_limit_ms=time_limit,
        dataset_status=None,
    )
    if "Samples" not in config:
        return
    samples = []
    for sample in config["Samples"]:
        input_file = f"{input_path_prefix}{config['TestCases'][sample]['Input']}"
        output_file = f"{output_path_prefix}{config['TestCases'][sample]['Output']}"
        input_data = zip.read(input_file)
        output_data = zip.read(output_file)
        samples.append(
            {
                "input": input_data.decode(),
                "output": output_data.decode(),
            }
        )
    await problem.edit(domain_id, pid, samples=samples)


async def _on_problem_data_change(e):
    value = e["value"]
    domain_id = value["domain_id"]
    pid = value["pid"]
    pdoc = await problem.get(domain_id, pid)
    pdata = await problem.get_data(pdoc)
    data = await fs.get(pdata["_id"])
    bytes = await data.read()
    zip = ZipFile(io.BytesIO(bytes))
    try:
        await _validate_dataset(domain_id, pid, zip)
    except DatasetError as e:
        _logger.error(e.args[0])
        await problem.edit(
            domain_id,
            pid,
            dataset_status=e.args[0],
        )
    finally:
        zip.close()
        data.close()


def init():
    bus.subscribe(_on_problem_data_change, ["problem_data_change"])
