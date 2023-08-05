# Tensorshow

Tensorshow is a python module for inspecting [TFRecords](https://www.tensorflow.org/api_guides/python/reading_data#file_formats).

Tensorshow can convert a TFRecord to a pandas dataframe.

```python
import tensorshow

# The column labels of `df` are the features of the tf.train.example protobufs.
df = tensorshow.dataframe_from('path/to/tfrecord')
```

Tensorshow can be used as a command line utility. It will convert a tfrecord to an html file on the command line.

```bash
python tensorshow --tfrecord=/Users/joel/train.tfrecord --html_file=Users/joel/out.html
```

Images stored as byte strings will be automatically detected and displayed as images rather than text. The `out.html` file looks like this when you open it with a browser.

![TFRecord displayed as a table](http://www.joellaity.com/img/html_tensorshow_example.png)


Tensorshow can be used in a jupyter notebook to preview a TFRecord. The `head` function will show the first 5 `tf.train.example`s by default and the `random` function will show five random `tf.train.example`s from the tfrecord.

![A preview of a TFRecord in a jupyter notebook](http://www.joellaity.com/img/nb_tensorshow_example.png)
