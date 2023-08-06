# space-diff

## Description
__space-diff__ is a tool that highlights inconsistencies in word segmentation within spaced texts (such as training corpora) for any spaceless orthography.

This tool is Pure Python and requires Python 3.6+

## Installation
```
pip install space-diff
```

## Usage/Tutorial
Included in this repository are two sample corpora of segmented traditional Chinese which will be used in this tutorial for ease in following along. (Adapted from [Universal Dependencies' Chinese corpora](https://github.com/UniversalDependencies/UD_Chinese-GSD/tree/master).) The following instructions assume that you have __space-diff__ installed already, as well as the sample corpora.

### Command line usage
You can simply call the tool at the command line as follows:
```
$ space-diff [-h] [-d] corp [corp ...]
```
with the optional `-h | --help` argument, the optional `-d | --digits` argument, and one or more corpus file of segmented text.

#### Using the sample data
By running:
```
$ space-diff sample_corp_a.txt sample_corp_b.txt
```
you will see the that the program updates you as it processes, and then ultimately prints a human-readable summary of its findings. Here's a sample:

![Image of sample output](https://github.com/smithnlp/space-diff/blob/master/sample_output.png)

This output allows manual review each instance of segmentation inconsistency, where you can note which ones are errors and which are inherent variation. The idea is to then fix those that are actual errors in your corpora before training (a segmenter) on that data.

#### Using your own data
For your own data, just pass the files and their paths if necessary, separated by spaces to __space-diff__ and optionally save the output to wherever you'd like.
```
$ space-diff ~/path/to/thisfile.txt ~/path/to/another.txt ~/path/to/third.txt > ~/Desktop/seg_inconsistency.txt
```

#### Excluding digits
By default, the tool considers strings like `12`, `712`, `1 20`, and `1220` as inconsistent segmentations of a 'multi-character' token `12`. If you wish to declutter the output with numerical cases like this, pass __space-diff__ the flag `-d` to ignore digits in its searching.
```
$ space-diff -d sample_corp_a.txt sample_corp_b.txt
```
or
```
$ space-diff sample_corp_a.txt sample_corp_b.txt --digits
```

## License
GNU GPLv3 - see LICENSE file for details.

## Contact
Blake Perry Smith
perry.smithb@gmail.com
