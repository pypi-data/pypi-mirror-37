name = "bi_s3"

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import sys
if sys.version_info >= (3,0):
    from bi_s3.bi_s3 import S3BI
else:
    from bi_s3 import S3BI
