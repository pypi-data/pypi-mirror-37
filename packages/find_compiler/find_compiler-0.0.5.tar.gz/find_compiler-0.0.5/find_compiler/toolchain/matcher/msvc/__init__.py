import re
from utils.subprocess import get_output

_command_candidate_patterns = ['\\\\cl.exe$']
_msvc_version_pattern='Microsoft \(R\) C/C\+\+ Optimizing Compiler Version (\d+\.\d+\.\d+) for \s*'

def _detect_msvc_version(command, out=None):
  output = get_output([command])
  match = re.search(_msvc_version_pattern, output)
  if not match:
    out.warning("[msvc]  {}: could not find version string".format(command))
    out.debug("[msvc] {}: {}".format(command, output))
    return "unknown"
  return match.group(1)

def _is_it_really_msvc(command, patterns, out=None):
  for pattern in patterns:
    if re.search(pattern, command):
      return True
  return False


def _detect_msvc(command, out=None):
  if not command:
    return None

  if not _is_it_really_msvc(command, _command_candidate_patterns, out):
    if out:
      out.trace("[clg2] {} is not ClangC2".format(command))
    return None

  version=_detect_msvc_version(command, out)
  out.info("[msvc] {}: found Visual Studio version {}".format(command, version))

  options=[]
  meta = {
    "tool": "msvc",
    "path": command,
    "version": version,
    "options": options
  }
  return meta

def run(command, out=None):
  ret = _detect_msvc(command, out)
  if ret:
    return [ret]
  return None
