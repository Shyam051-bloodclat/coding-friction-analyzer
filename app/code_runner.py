
import ast
import traceback
import inspect


def analyze_code(code, problem):

    try:
        tree = ast.parse(code)

    except SyntaxError as e:

        return {
            "status": "Syntax Error",
            "error_type": "SyntaxError",
            "problem": e.msg,
            "explanation": (
                "What went wrong: Python could not understand your code.\n\n"
                "Why: There is a syntax mistake in your program.\n\n"
                "How to fix: Check the indicated line for missing brackets, "
                "colons, quotes, or incorrect indentation."
            ),
            "line": e.lineno
        }

    namespace = {}

    try:
        exec(code, namespace)

    except Exception as e:

        error_trace = traceback.extract_tb(e.__traceback__)
        line = error_trace[-1].lineno

        return {
            "status": "Runtime Error",
            "error_type": type(e).__name__,
            "problem": str(e),
            "explanation": get_error_explanation(type(e).__name__),
            "line": line
        }

    function_name = problem["function_name"]

    if function_name not in namespace:

        functions = []

        for name, value in namespace.items():

            if callable(value) and not name.startswith("__"):
                functions.append(name)

        if len(functions) > 0:

            return {
                "status": "Function Error",
                "error_type": "Incorrect Function Name",
                "problem": "The required function was not found.",
                "explanation": (
                    "What went wrong: The required function name is incorrect.\n\n"
                    "Required function: "
                    + function_name
                    + "\n\n"
                    "Your function: "
                    + ", ".join(functions)
                    + "\n\n"
                    "How to fix: Rename your function to "
                    + function_name
                    + "."
                ),
                "line": None
            }

        return {
            "status": "Function Error",
            "error_type": "Missing Function",
            "problem": "Required function was not found.",
            "explanation": (
                "What went wrong: The required function is missing.\n\n"
                "How to fix: Create a function named "
                + function_name
                + "."
            ),
            "line": None
        }

    student_function = namespace[function_name]

    expected_arguments = len(problem["test_cases"][0]["input"])

    try:

        signature = inspect.signature(student_function)

        actual_arguments = 0

        for parameter in signature.parameters.values():

            if parameter.kind in (
                parameter.POSITIONAL_ONLY,
                parameter.POSITIONAL_OR_KEYWORD
            ):
                actual_arguments += 1

    except Exception:

        actual_arguments = expected_arguments

    if actual_arguments != expected_arguments:

        return {
            "status": "Function Error",
            "error_type": "Incorrect Parameters",
            "problem": "The function has an incorrect number of parameters.",
            "explanation": (
                "What went wrong: Your function has the wrong number of parameters.\n\n"
                "Required parameters: "
                + str(expected_arguments)
                + "\n\n"
                "Your parameters: "
                + str(actual_arguments)
                + "\n\n"
                "How to fix: Check the function definition and use the correct number of parameters."
            ),
            "line": None
        }

    operation = None
    operation_line = None

    for node in ast.walk(tree):

        if isinstance(node, ast.Sub):

            operation = "subtraction"
            operation_line = getattr(node, "lineno", None)

        elif isinstance(node, ast.Add):

            operation = "addition"
            operation_line = getattr(node, "lineno", None)

        elif isinstance(node, ast.Mult):

            operation = "multiplication"
            operation_line = getattr(node, "lineno", None)

    results = []
    failed_tests = []

    for test in problem["test_cases"]:

        inputs = test["input"]
        expected = test["expected"]

        try:

            actual = student_function(*inputs)

            test_result = {
                "input": inputs,
                "expected": expected,
                "actual": actual
            }

            results.append(test_result)

            if actual != expected:

                failed_tests.append(test_result)

        except Exception as e:

            error_trace = traceback.extract_tb(e.__traceback__)
            line = error_trace[-1].lineno

            return {
                "status": "Runtime Error",
                "error_type": type(e).__name__,
                "problem": str(e),
                "explanation": get_error_explanation(type(e).__name__),
                "line": line
            }

    if len(failed_tests) == 0:

        return {
            "status": "Correct",
            "explanation": "All test cases passed successfully.",
            "results": results
        }

    explanation = "Your code does not produce the expected output."
    correction = None

    if problem["function_name"] == "add" and operation == "subtraction":

        explanation = (
            "What went wrong: You used subtraction instead of addition.\n\n"
            "Why: The question asks you to calculate the sum of two numbers.\n\n"
            "How to fix: Replace subtraction with addition."
        )

        correction = (
            "def add(a, b):\n"
            "    return a + b"
        )

    elif problem["function_name"] == "subtract" and operation == "addition":

        explanation = (
            "What went wrong: You used addition instead of subtraction.\n\n"
            "Why: The question asks you to calculate the difference between two numbers.\n\n"
            "How to fix: Replace addition with subtraction."
        )

        correction = (
            "def subtract(a, b):\n"
            "    return a - b"
        )

    elif problem["function_name"] == "multiply" and operation != "multiplication":

        explanation = (
            "What went wrong: The multiplication operation is missing or incorrect.\n\n"
            "Why: The question asks you to calculate the product of the two numbers.\n\n"
            "How to fix: Use the * operator."
        )

        correction = (
            "def multiply(a, b):\n"
            "    return a * b"
        )

    elif problem["function_name"] == "square":

        explanation = (
            "What went wrong: The function is not returning the square correctly.\n\n"
            "Why: The square of a number is the number multiplied by itself.\n\n"
            "How to fix: Multiply the number by itself."
        )

        correction = (
            "def square(n):\n"
            "    return n * n"
        )

    elif problem["function_name"] == "check_even_odd":

        explanation = (
            "What went wrong: The even/odd condition is incorrect.\n\n"
            "Why: A number is even when it is completely divisible by 2.\n\n"
            "How to fix: Check whether n % 2 == 0."
        )

        correction = (
            "def check_even_odd(n):\n"
            "    if n % 2 == 0:\n"
            "        return \"Even\"\n"
            "    else:\n"
            "        return \"Odd\""
        )

    return {
        "status": "Wrong Answer",
        "error_type": "Wrong Answer",
        "problem": "One or more test cases failed.",
        "explanation": explanation,
        "line": operation_line,
        "correction": correction,
        "results": results,
        "failed_tests": failed_tests
    }


def get_error_explanation(error_type):

    if error_type == "ZeroDivisionError":

        return (
            "What went wrong: Your code tried to divide a number by zero.\n\n"
            "Why: Division by zero is not allowed in Python.\n\n"
            "How to fix: Check the denominator before performing the division."
        )

    elif error_type == "NameError":

        return (
            "What went wrong: Your code used a name that Python does not know.\n\n"
            "Why: The variable or function may not have been defined yet, "
            "or its name may be misspelled.\n\n"
            "How to fix: Check the spelling and make sure the variable or function is defined."
        )

    elif error_type == "TypeError":

        return (
            "What went wrong: Your code used an operation with an incompatible data type.\n\n"
            "Why: Python cannot perform that operation with the given types.\n\n"
            "How to fix: Check the types of the values you are using."
        )

    elif error_type == "IndexError":

        return (
            "What went wrong: Your code tried to access a list position that does not exist.\n\n"
            "Why: The requested index is outside the valid range of the list.\n\n"
            "How to fix: Check the list length and make sure the index is valid."
        )

    elif error_type == "KeyError":

        return (
            "What went wrong: Your code tried to access a dictionary key that does not exist.\n\n"
            "Why: The requested key is not present in the dictionary.\n\n"
            "How to fix: Check the key name before accessing it."
        )

    elif error_type == "AttributeError":

        return (
            "What went wrong: Your code tried to use an attribute or method that does not exist.\n\n"
            "Why: The object may not support that attribute or method.\n\n"
            "How to fix: Check the object's type and the spelling of the attribute or method."
        )

    else:

        return (
            "What went wrong: The program produced a runtime error.\n\n"
            "How to fix: Check the error message and the line where the error occurred."
        )

