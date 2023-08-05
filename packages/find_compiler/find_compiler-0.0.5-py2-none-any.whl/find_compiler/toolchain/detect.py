from find_compiler.find import find_match_in_path

def detect_toolchains(out):
  tools = []

  # FIXME: supplying those preliminary patterns should probably be merged into "plugins"
  for f in ['clang', 'clang.exe', 'clang++', 'clang++.exe', 'clang-*', 'clang++-*', 'gcc', 'gcc-*', 'g++', 'g++-*', 'cl.exe']:
    tools.extend(find_match_in_path(f))
  return tools
