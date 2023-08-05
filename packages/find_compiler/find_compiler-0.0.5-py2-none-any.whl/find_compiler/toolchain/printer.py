import yaml
import json

_print_format='{{:{}}}{{:{}}}{{:{}}}'
_allowed_keys = ['path', 'tool', 'version', 'options']

def _fiter_out_meta(meta):
  result = []
  for m in meta:
    result.append({k:v for k,v in m.items() if k in _allowed_keys})
  return result

def _adjust_print_format(meta):
  path_size = 25
  tool_size = 15
  version_size = 10
  for m in meta:
    path_size = max(len(m['path']) + 3, path_size)
    tool_size = max(len(m['tool']) + 3, tool_size)
    version_size = max(len(m['version']) + 3, version_size)
  return _print_format.format(path_size, tool_size, version_size)

def _output_plain(meta):
  fmt = _adjust_print_format(meta)
  if len(meta):
    print(fmt.format('PATH', 'TOOLCHAIN', 'VERSION'))
    for m in meta:
      print(fmt.format(m['path'], m['tool'], m['version']))
  else:
    print("No compilers found.")

def _output_yaml(meta):
  print(yaml.dump(meta, default_flow_style=False))

def _output_json(meta):
   print(json.dumps(meta, sort_keys=True, indent=2, separators=(',', ': ')))

def print_toolchains(meta, output):
  meta = _fiter_out_meta(meta)
  if output == "yaml":
    _output_yaml(meta)
  elif output == "json":
    _output_json(meta)
  else:
    _output_plain(meta)
