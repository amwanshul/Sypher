import pytest
import os
import ast

# Import the functionality to test
from actions.desktop import _is_safe_code, _execute_generated_code

def test_safe_code():
    code = "print('Hello, world!')"
    safe, msg = _is_safe_code(code)
    assert safe is True
    assert msg == "OK"

def test_safe_pyautogui():
    code = "pyautogui.moveTo(100, 100)"
    safe, msg = _is_safe_code(code)
    assert safe is True
    assert msg == "OK"

def test_blocked_keyword():
    code = "import os"
    safe, msg = _is_safe_code(code)
    assert safe is False
    assert "Blocked operation:" in msg

def test_blocked_ast_dunder_attribute():
    code = "a = x.__class__"
    safe, msg = _is_safe_code(code)
    assert safe is False
    assert "Access to private/dunder attribute '__class__' is not allowed" in msg

def test_blocked_ast_dunder_name():
    code = "a = __import__('os')"
    safe, msg = _is_safe_code(code)
    assert safe is False

def test_blocked_ast_import_direct():
    code = "import sys"
    safe, msg = _is_safe_code(code)
    assert safe is False
    assert "Imports are not allowed" in msg

def test_blocked_ast_import_from():
    code = "from os import path"
    safe, msg = _is_safe_code(code)
    assert safe is False
    assert "Imports are not allowed" in msg

# Test actual execution sandbox
class MockPlayer:
    def write_log(self, text):
        pass
    def confirm_action(self, title, message, default):
        return True

def test_exec_blocks_getattr():
    # getattr is removed from builtins, so this should fail inside exec
    # We use a code block that doesn't trigger AST check for getattr directly since we removed it from AST
    # Wait, the AST no longer blocks getattr. Let's make sure it fails during exec.
    code = "getattr(pyautogui, '__class__')"
    import actions.desktop as ad
    old_req = ad.require_untrusted_execution_approval
    ad.require_untrusted_execution_approval = lambda **kwargs: (True, "")
    try:
        res = _execute_generated_code(code, player=MockPlayer(), reason="test")
        assert "Execution error" in res and "name 'getattr' is not defined" in res
    finally:
        ad.require_untrusted_execution_approval = old_req

def test_exec_blocks_module_leakage():
    # accessing os from pyautogui should raise an error
    code = "pyautogui.os"
    import actions.desktop as ad
    old_req = ad.require_untrusted_execution_approval
    ad.require_untrusted_execution_approval = lambda **kwargs: (True, "")
    try:
        res = _execute_generated_code(code, player=MockPlayer(), reason="test")
        assert "Execution error" in res and "Access to submodule 'os' denied" in res
    finally:
        ad.require_untrusted_execution_approval = old_req

print("Tests written successfully.")

def test_happy_path_os_path():
    code = "res = os.path.join('a', 'b')\nprint(res)"
    import actions.desktop as ad
    old_req = ad.require_untrusted_execution_approval
    ad.require_untrusted_execution_approval = lambda **kwargs: (True, "")
    try:
        res = _execute_generated_code(code, player=MockPlayer(), reason="test")
        assert "a/b" in res or "a\\b" in res
    finally:
        ad.require_untrusted_execution_approval = old_req

def test_happy_path_os_listdir():
    code = "res = os.listdir('.')\nprint('success')"
    import actions.desktop as ad
    old_req = ad.require_untrusted_execution_approval
    ad.require_untrusted_execution_approval = lambda **kwargs: (True, "")
    try:
        res = _execute_generated_code(code, player=MockPlayer(), reason="test")
        assert "success" in res
    finally:
        ad.require_untrusted_execution_approval = old_req

def test_blocked_ctypes():
    code = "ctypes.windll"
    import actions.desktop as ad
    old_req = ad.require_untrusted_execution_approval
    ad.require_untrusted_execution_approval = lambda **kwargs: (True, "")
    try:
        res = _execute_generated_code(code, player=MockPlayer(), reason="test")
        assert "name 'ctypes' is not defined" in res
    finally:
        ad.require_untrusted_execution_approval = old_req
