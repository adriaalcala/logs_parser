# LOG PARSER
This tool has two goals:
1. Parse a log file to get a list of hostnames connected to the given host during the given period
2. Run indefinitely and output once every hour:
    * a list of hostnames connected to a given (configurable) host during the last hour
    * a list of hostnames received connections from a given (configurable) host during the last hour
    * the hostname that generated most connections in the last hour

## How to use
This tool it's very simple to use and only `Python3.8` is required. To see the instructions to run just execute `python main.py -h`,
this instruction will output

![general help] (general_help.png)

To see the instruction for the first goal just execute `python main.py input_file connected -h`

![connected help] (connected_help.png)

And for the second goal `python main.py input_file unlimited -h`

![unlimited hep] (unlimited_help.png)

### Try it
In this repository there is an example file, that can be used to check the tool, this sample file is located in `data/sample.txt`.

To check the first goal you can run

`python main.py data/sample.txt connected 1565647309932 1565733461781 Jovaun`

and for the second

`python main.py data/sample.txt unlimited  Douaa Chabria -i 1565647309932`

## The logs
By default this tool writes the output in stdout and in log file name `logs/info_logs.log` using a RotatingFileHandler with a backup count of 5
and max size of 10**6 bytes. This can be changed using the following environment variables:
* LOGS_DIR
* MAX_BYTES
* BACKUP_COUNT

## The output
An example of output for the first goal is:

![connected output] (connected_output.png)

And an example of output for the second goal is:

![unlimited output] (unlimited_output.png)

## The checks
There are some dependencies to run the tests, the easier way to install it is using pipenv with `pipenv install --dev`. Once the dependencies are
installed, run `pipenv run nox` will run the following sessions:
* lint, which check all code using `flake8`.
* safety, which scan dependencies for insecure packages.
* mypy, for type-check.
* tests, run tests using `pytest`.
* pytype, another type-check complementary to mypy.
* coverage, check the test coverage (now fails if is under than 100%)
* docs, builds the sphinx docs.


## Assumptions
* The second goal only need to parse a file indefinitely. If this assumption was wrong can be fixed adding another argument and in the code breaks when the file is finished if it's the desired behaviour.

## Improvements
* A datetime parser could be implemented instead of using timestamps to make the script easier to use.
