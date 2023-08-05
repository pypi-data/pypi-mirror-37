import re
from utils.subprocess import get_output

# [^a-zA-Z] before g++ patterns is there to exclude clang++ from matching, so that /g++ or \g++.exe can only match.
# it could be done by splitting path, and taking only last part
_command_candidate_patterns = ['gcc(\.exe)?$','gcc-[0-9]{1}[A-Za-z0-9]*(\.exe)?$', '[^a-zA-z]g\+\+(\.exe)?$', '[^a-zA-z]g\+\+-[0-9]{1}[A-Za-z0-9]*(\.exe)?$']
_apple_llvm_pattern='Apple LLVM version ([0-9\.]+)'
_gcc_version_pattern='g(cc|\+\+)[^(]+\([^)]+\)\s+(\d+\.\d+\.\d+)'

def _is_it_clang_in_gcc_clothing(command):
  output = get_output([command, "--version"])
  match = re.search(_apple_llvm_pattern, output)
  if match:
    return True
  return False

def _is_it_really_gnu(command, patterns, out=None):
  for pattern in patterns:
    if re.search(pattern, command):
      if not _is_it_clang_in_gcc_clothing(command):
        return True
      else:
        out.trace("[gnuc] {}: Found Clang in GCC's clothing".format(command))
  return False

def _detect_gcc_version(command, out=None):
  output = get_output([command, "--version"])
  match = re.search(_gcc_version_pattern, output)
  if not match:
    out.warning("[gnuc]  {}: could not find version string".format(command))
    out.debug("[gnuc] {}: {}".format(command, output))
    return "unknown"
  return match.group(2)

def _detect_gcc(command, out=None):
  if not command:
    return None

  if not _is_it_really_gnu(command, _command_candidate_patterns, out):
    if out:
      out.trace("[gnuc] {} is not GNU Compiler".format(command))
    return None

  version=_detect_gcc_version(command, out)
  out.info("[gnuc] {}: found GNU Compiler version {}".format(command, version))

  options=[]
  meta = {
    "tool": "gcc",
    "path": command,
    "version": version,
    "options": options
  }
  return meta
def run(command, out=None):
  ret = _detect_gcc(command, out)
  if ret:
    return [ret]
  return None
