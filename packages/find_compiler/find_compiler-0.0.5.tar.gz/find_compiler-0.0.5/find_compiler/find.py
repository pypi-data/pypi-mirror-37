import os
import glob

# Visual Studio by default does not put compiler in PATH. It relies on batch
# scripts to properly set up environment, so there's high chance we will need
# too find C/C++ compiler looking through well-known toolchain folders.
# FIXME: supplying extra paths should probably be merged into "plugins"
msvc_search_path = [
  # Visual Studio 2017:
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\MSVC\\14.15.26726\\bin\\Hostx64\\x64",
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\MSVC\\14.15.26726\\bin\\Hostx64\\x86",
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\MSVC\\14.15.26726\\bin\\Hostx86\\x64",
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\MSVC\\14.15.26726\\bin\\Hostx64\\x86",
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\ClangC2\\14.10.25903\\bin\\HostX64",
  "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise\\VC\\Tools\\ClangC2\\14.10.25903\\bin\\HostX86",
]

def find_match_in_path(name, path=None):
  path = path or os.environ.get('PATH')
  results = []
  paths = path.split(os.pathsep) + msvc_search_path
  for dir in paths:
    matches = glob.glob(os.path.join(dir, name))
    results.extend(matches)
  return results
