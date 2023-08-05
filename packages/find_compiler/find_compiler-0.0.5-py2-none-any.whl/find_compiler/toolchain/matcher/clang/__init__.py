import re
from utils.subprocess import get_output

_command_candidate_patterns = ['clang(\.exe)?$','clang-[A-Za-z0-9]*[0-9]+(\.exe)?$', 'clang\+\+(\.exe)?$', 'clang\+\+-[A-Za-z0-9]*[0-9]+(\.exe)?$']
_apple_llvm_pattern='Apple LLVM version ([0-9\.]+)'
_clangc2_pattern='clang with Microsoft CodeGen'
_clang_version_pattern='clang version (\d\.\d\.\d[^\s]*)'

def _is_it_different_clang(output, patterns):
  for pattern in patterns:
    match = re.search(pattern, output)
    if match:
      return True
  return False

def _is_it_really_clang(command, patterns, out=None):
  for pattern in patterns:
    if re.search(pattern, command):
      output = get_output([command, "--version"])
      if not _is_it_different_clang(output, [_apple_llvm_pattern, _clangc2_pattern]):
        return True
      else:
        out.trace("[clng] {}: It is not vanilla Clang (e.g. Apple, or ClangC2). Aborting.".format(command))
  return False

def _detect_clang_version(command, out=None):
  output = get_output([command, "--version"])
  match = re.search(_clang_version_pattern, output)
  if not match:
    out.warning("[clng]  {}: could not find version string".format(command))
    out.debug("[clng] {}: {}".format(command, output))
    return "unknown"
  return match.group(1)

def _detect_clang(command, out=None):
  if not command:
    return None

  if not _is_it_really_clang(command, _command_candidate_patterns, out):
    if out:
      out.trace("[clng] {} is not Clang".format(command))
    return None

  version=_detect_clang_version(command, out)
  out.info("[clng] {}: found Clang version {}".format(command, version))

  options=[]
  meta = {
    "tool": "clang",
    "path": command,
    "version": version,
    "options": options
  }
  return meta


def run(command, out=None):
  ret = _detect_clang(command, out)
  if ret:
    return [ret]
  return None
