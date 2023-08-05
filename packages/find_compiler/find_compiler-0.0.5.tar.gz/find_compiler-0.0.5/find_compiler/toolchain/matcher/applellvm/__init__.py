import re
from utils.subprocess import get_output

_command_candidate_patterns = ['/usr/bin/gcc','/usr/bin/g++', '/usr/bin/clang', '/usr/bin/clang++']
_find_apple_llvm_version='Apple LLVM version ([0-9\.]+)'
_find_apple_llvm_options='\s+--?([A-Za-z0-9#\-\+]+)((([\s,]*)|=)<([^>]+)>)?\s*([^\n]+)'


def _detect_apple_llvm_options(command):
  output = get_output([command, "--help"])
  match = re.findall(_find_apple_llvm_options, output)
  options = []
  for m in match:
    options.append({
      "name": m[0],
      "paremeter": m[4],
      "description": m[5]
    })
  return options

def _detect_apple_llvm_version(command, out=None):
  output = get_output([command, "--version"])
  match = re.search(_find_apple_llvm_version, output)
  if not match:
    if out:
      out.trace("[appl] {} is not Apple LLVM compiler".format(command))
    return None
  return match.group(1)

def _detect_apple_llvm(command, out=None):
  if not command:
    return None

  if command not in _command_candidate_patterns:
    if out:
      out.trace("[appl] {} is not valid command candidate".format(command))
    return None


  version = _detect_apple_llvm_version(command, out)
  if not version:
    return None

  options = _detect_apple_llvm_options(command)

  out.info("[appl] {}: found Apple LLVM compiler version {}".format(command, version))
  meta = {
    "tool": "applellvm",
    "path": command,
    "version": version,
    "options": options
  }
  return meta

def run(command, out=None):
  ret = _detect_apple_llvm(command, out)
  if ret:
    return [ret]
  return None
