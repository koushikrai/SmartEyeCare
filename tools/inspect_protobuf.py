import google
import google.protobuf as p
import sys
print('Python exe:', sys.executable)
print('protobuf package file:', getattr(p, '__file__', None))
print('protobuf version (pkg):', end=' ')
try:
    import pkg_resources
    print(pkg_resources.get_distribution('protobuf').version)
except Exception as e:
    print('pkg_resources not available or distribution not found:', e)
print('has runtime_version:', 'runtime_version' in dir(p))
print('dir filtered:', [k for k in dir(p) if 'runtime' in k.lower() or 'version' in k.lower()])
# try to import runtime_version symbol
try:
    from google.protobuf import runtime_version
    print('Imported runtime_version:', runtime_version)
except Exception as e:
    print('Failed to import runtime_version:', e)
