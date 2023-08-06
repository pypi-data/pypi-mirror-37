"""
Implementation of image classifier using exif meta data

@author Sangkeun Kim
@url https://github.com/sisobus/exif_utils
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import piexif
from . import utils
from datetime import datetime
from dateutil.relativedelta import relativedelta


def classify(directory_path, dest_directory_path='./out'):
    directory_path = os.path.abspath(directory_path)
    assert os.path.exists(directory_path)

    dest_directory_path = os.path.abspath(dest_directory_path)
    if not os.path.exists(dest_directory_path):
        utils._exec("mkdir {}".format(dest_directory_path))
    filepaths = utils.get_image_filepaths(directory_path)
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        exif_dict = piexif.load(filepath)
        try:
            dt = exif_dict['Exif'][36867]
            dt = dt.decode("utf-8")
            tt = dt.split()[1]
            hour = int(tt.split(":")[0])
            dt = dt.split()[0].replace(":", "-")
            if hour < 3:
                from_dt = datetime.strptime(dt, "%Y-%m-%d")
                to_dt = from_dt - relativedelta(days=1)
                dt = to_dt.strftime("%Y-%m-%d")
            dt_path = os.path.join(dest_directory_path, dt)
            if not os.path.exists(dt_path):
                utils._exec("mkdir {}".format(dt_path))
            utils._exec(
                "mv {} {}".format(
                    filepath, os.path.join(dt_path, filename)))
            print ("classify complete {}".format(filepath))
        except Exception as e:
            e = e
            print ("datetime is not exists in {}".format(filepath))


if __name__ == '__main__':
    classify("./tmp", "./out")
