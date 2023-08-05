import itertools
import random

import base64
import fleep

from IPython.display import HTML
from io import BytesIO
import pandas as pd
from PIL import Image
import tensorflow as tf

styling = """
<head>
<style>

body {
  font-family: sans-serif;
  font-size: 16px;
  font-weight: 400;
  text-rendering: optimizeLegibility;
}

table {border: none;}
 
th {
  background:#FFFFFF;
  font-size:23px;
  font-weight: 200;
  padding:24px;
  text-align:left;
  vertical-align:middle;
  border:none;
}

  
tr {
  border:none;
  font-size:16px;
  font-weight:bold;
}
 
tr:hover td {
  background:#E0FFFF;
}
 
 
tr:nth-child(odd) td {
  background:#EBEBEB;
}
 
tr:nth-child(odd):hover td {
  background:#E0FFFF;
}

 
td {
  background:#FFFFFF;
  padding:20px;
  text-align:left;
  vertical-align:middle;
  font-weight:300;
  font-size:18px;
  border:none;
}

</style>
</head>
"""


def _feature_to_list(feat):
    kind = feat.WhichOneof("kind")
    if kind == "float_list":
        return list(feat.float_list.value)
    elif kind == "int64_list":
        return list(feat.int64_list.value)
    elif kind == "bytes_list":
        return list(feat.bytes_list.value)
    else:
        assert false


def _example_to_dict(example_str):
    example = tf.train.Example()
    example.ParseFromString(example_str)
    d = dict(example.features.feature)
    return {k: _feature_to_list(v) for k, v in d.items()}


def _image_to_base64(img_str, thumbnail_size=(128, 128)):
    with BytesIO() as img_buffer:
        img_buffer.write(img_str)
        img = Image.open(img_buffer)
        img_buffer.seek(0)
        img.thumbnail(thumbnail_size, Image.ANTIALIAS)
        with BytesIO() as thumb_buffer:
            img.save(thumb_buffer, format="JPEG")
            return str(base64.b64encode(thumb_buffer.getvalue()))[2:-1]


def _image_formatter(thumbnail_size=(128, 128)):

    def fmt_fn(img):
        return (
            f'<img src="data:image/jpeg;base64,{_image_to_base64(img[0], thumbnail_size=thumbnail_size)}">'
        )

    return fmt_fn


def _cols_with_images(df):
    res = []
    for k in df.keys():
        if isinstance(df[k][0][0], bytes):
            info = fleep.get(df[k][0][0])
            if info.type_matches("raster-image"):
                res.append(k)

    return res


def dataframe_from(tfrecord_path, limit=None):
    if limit is None or limit < 0:
        # 2**63 bytes is ~9 exabytes, so limit is essentially infinite.
        limit = 1 << 63

    record_it = tf.python_io.tf_record_iterator(tfrecord_path)
    rows = [
        _example_to_dict(record_str) for _, record_str in zip(range(limit), record_it)
    ]
    return pd.DataFrame(rows)


def sample_dataframe_from(tfrecord_path, limit=None):
    if limit is None or limit < 0:
        return dataframe_from(tfrecord_path, limit=limit)

    record_it = tf.python_io.tf_record_iterator(tfrecord_path)
    running_sample = list(itertools.islice(record_it, limit))
    num_seen_so_far = limit
    for x in record_it:
        num_seen_so_far += 1
        idx_to_replace = random.randrange(num_seen_so_far)
        if idx_to_replace < limit:
            running_sample[idx_to_replace] = x

    rows = [_example_to_dict(record_str) for record_str in running_sample]
    return pd.DataFrame(rows)


def head(tfrecord_path, limit=5, thumbnail_size=(128, 128)):
    df = dataframe_from(tfrecord_path, limit=limit)
    pd.set_option("display.max_colwidth", -1)
    html_all = df.to_html(
        formatters={
            col: _image_formatter(thumbnail_size) for col in _cols_with_images(df)
        },
        escape=False,
    )
    return HTML(html_all)


def sample(tfrecord_path, limit=5, thumbnail_size=(128, 128)):
    df = sample_dataframe_from(tfrecord_path, limit=limit)
    pd.set_option("display.max_colwidth", -1)
    html_all = df.to_html(
        formatters={
            col: _image_formatter(thumbnail_size) for col in _cols_with_images(df)
        },
        escape=False,
    )
    return HTML(html_all)


def html_file_from(
    tfrecord_path, outfile, limit=None, random=False, thumbnail_size=(128, 128)
):
    if random:
        df = sample_dataframe_from(tfrecord_path, limit=limit)
    else:
        df = dataframe_from(tfrecord_path, limit=limit)
    pd.set_option("display.max_colwidth", -1)
    with open(outfile, "w+") as f:
        f.write(styling)
        df.to_html(
            buf=f,
            formatters={
                col: _image_formatter(thumbnail_size) for col in _cols_with_images(df)
            },
            escape=False,
        )
