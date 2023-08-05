import re
from utils.subprocess import get_output

_command_candidate_patterns = ['clang\.exe$']
_clangc2_pattern='clang with Microsoft CodeGen'
_clang_version_pattern='clang with Microsoft CodeGen version (\d\.\d\.\d[^\s]*)'

def _is_it_clangc2(output):
  match = re.search(_clangc2_pattern, output)
  if match:
    return True
  return False

def _is_it_really_clang(command, patterns, out=None):
  for pattern in patterns:
    if re.search(pattern, command):
      output = get_output([command, "--version"])
      if _is_it_clangc2(output):
        return True
      else:
        out.trace("[clg2] {}: It is not ClangC2. Aborting.".format(command))
  return False

def _detect_clang_version(command, out=None):
  output = get_output([command, "--version"])
  match = re.search(_clang_version_pattern, output)
  if not match:
    out.warning("[clg2]  {}: could not find version string".format(command))
    out.debug("[clg2] {}: {}".format(command, output))
    return "unknown"
  return match.group(1)

def _detect_clangc2(command, out=None):
  if not command:
    return None

  if not _is_it_really_clang(command, _command_candidate_patterns, out):
    if out:
      out.trace("[clg2] {} is not ClangC2".format(command))
    return None

  version=_detect_clang_version(command, out)
  out.info("[clg2] {}: found ClangC2 version {}".format(command, version))

  options=[]
  meta = {
    "tool": "clangc2",
    "path": command,
    "version": version,
    "options": options
  }
  return meta


def run(command, out=None):
  ret = _detect_clangc2(command, out)
  if ret:
    return [ret]
  return None
