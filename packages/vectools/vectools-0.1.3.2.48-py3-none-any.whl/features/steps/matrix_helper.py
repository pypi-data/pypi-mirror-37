from behave import *
from mock import *
import sys
import numpy as np
import tempfile
from io import StringIO
import shlex, subprocess
import sys


use_step_matcher("parse")


def show_diffs(command, captured_output, subprocess_output, expected_output):
    print("command ------------------------------------------------------------")
    print(command)

    print("captured_output ----------------------------------------------------")
    print(captured_output)

    print("subprocess_output --------------------------------------------------")
    print(subprocess_output)
    print(subprocess_output.__dict__)
    print(subprocess_output.stderr.stderr.decode('UTF-8').strip())

    print("expected_output ----------------------------------------------------")
    print(expected_output)


@given("we use vectools {}")
def step_impl(context, operation):
    """
    :param context: behave.runner.Context
    :param argument:
    :param value:
    :return:
    """
    context.mock_sys.append("./vectools")
    context.mock_sys.append(operation)


@given("argument {} with the value {}")
def step_impl(context, argument, value):
    """
    :param context: behave.runner.Context
    :param argument:
    :param value:
    :return:
    """
    context.mock_sys.append(argument)
    context.mock_sys.append(value)


@given("the argument {}")
def step_impl(context, value):
    """
    :param context: behave.runner.Context
    :param value:
    :return:
    """
    context.mock_sys.append(value)

@given("the file {} containing the following text")
def step_impl(context, file_name):
    """
    :type context: behave.runner.Context
    :param file_name:
    :return:
    """
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(bytes(context.text, 'UTF-8'))
    tf.flush()
    tf.close()

    # So we can delete the file when done.
    setattr(context, file_name, tf.name)
    context.tmp_files.append(tf.name)
    context.mock_sys.append(tf.name)


@given("the following text passed via STDIN")
def step_impl(context):
    """
    :type context: behave.runner.Context
    :return:
    """
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(bytes(context.text, 'UTF-8'))
    tf.flush()
    tf.close()

    # So we can delete the file when done.
    # setattr(context, tf.name, tf.name)
    context.tmp_files.append(tf.name)
    context.mock_sys.append("cat %s | " % tf.name)

@when('we run the operation vectools {}')
def step_impl(context, function):
    """
    :type context: behave.runner.Context
    :param function:
    :return:
    """
    cli_args = ["./vectools", function] + sys.argv[1:]
    context.cli_command = " ".join(cli_args)
    context.run_subprocess = subprocess.run(
        context.cli_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out_txt = context.run_subprocess.stdout.decode('UTF-8').strip()
    # The STDOUT is captured by behave in the variable context.stdout_capture
    print(out_txt)


@when('we run the command')
def step_impl(context):
    """
    :type context: behave.runner.Context
    :return:
    """

    context.cli_command = " ".join(context.mock_sys)

    context.run_subprocess = subprocess.run(
        context.cli_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    out_txt = context.run_subprocess.stdout.decode('UTF-8').strip()

    # The STDOUT is captured by behave in the variable context.stdout_capture
    print(out_txt)


@then('we expect the output')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected_output = context.text.strip()
    captured_output = context.stdout_capture.getvalue().strip()
    assert captured_output == expected_output, show_diffs(
        context.cli_command,
        captured_output,
        context.run_subprocess,
        expected_output)


@then('we expect the error')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected_output = context.text.strip()
    # captured_output = context.stdout_capture.getvalue().strip()
    captured_error = context.run_subprocess.stderr.decode('UTF-8').strip()
    # captured_output = context.stderr_capture.getvalue().strip()

    assert captured_error == expected_output, show_diffs(
        context.cli_command,
        captured_error,
        context.run_subprocess,
        expected_output)



@given("parameter {} = {}")
def step_impl(context, key, value):
    """
    :param key:
    :param value:
    :type context: behave.runner.Context
    """
    sys.argv.append(key)
    values = value.split()
    sys.argv.extend(values)


@given("a matrix as STDIN")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    matrix = []
    rows = context.text.split("\n")
    for i in rows:
        matrix.append(i.replace(" ", "\t"))
    context.text_matrix = "\n".join(matrix)


@given("the placeholder -")
def step_impl(context):
    sys.argv.extend(["-"])


@given("a matrix")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    matrix = []
    rows = context.text.split("\n")
    for i in rows:
        matrix.append(i.split(" "))
    matrix = np.array(matrix)
    context.matrix = matrix


@then("we expect the matrix")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    matrix, matrix2 = [], []

    output = context.stdout_capture.getvalue().rstrip()

    rows = output.split("\n")
    for i in rows:
        matrix.append(i.split())

    rows = context.text.split("\n")
    for i in rows:
        matrix2.append(i.split())

    assert matrix == matrix2, matrix2


@given("last parameter {}")
def step_impl(context, param):
    """
    :type context: behave.runner.Context
    """
    sys.argv.append(param)


@given("the file {} containing")
def step_impl(context, file_name):
    """
    :type context: behave.runner.Context
    """
    matrix = []
    rows = context.text.split("\n")
    for i in rows:
        matrix.append(i.split(" "))

    matrix = np.array(matrix)

    text = context.text.replace(" ", "\t")

    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(bytes(text, 'UTF-8'))
    tf.close()

    setattr(context, file_name, tf.name)

    context.tmp_files.append(tf.name)


@given("file {} as parameter")
def step_impl(context, file_name):
    """
    :type context: behave.runner.Context
    """
    sys.argv.append(getattr(context, file_name))


@given("file parameter {} = {}")
def step_impl(context, key, file_name):
    """
    :param key:
    :param file_name:
    :type context: behave.runner.Context
    """
    # context.parser.parse_args(key, value)

    sys.argv.append(key)
    sys.argv.append(getattr(context, file_name))

    # print(sys.argv)

