import sys
try:
  import bz2
except ImportError:
  try:
    import bz2file
    # Polyfill compress/decompress if missing in bz2file
    if not hasattr(bz2file, 'compress'):
      def compress(data, compresslevel=9):
        comp = bz2file.BZ2Compressor(compresslevel)
        return comp.compress(data) + comp.flush()
      bz2file.compress = compress
    if not hasattr(bz2file, 'decompress'):
      def decompress(data):
        dec = bz2file.BZ2Decompressor()
        return dec.decompress(data)
      bz2file.decompress = decompress

    sys.modules['bz2'] = bz2file
  except ImportError:
    pass
