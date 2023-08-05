# nonechucks

**nonechucks** is a library for PyTorch that provides wrappers for PyTorch's Dataset and Sampler objects to allow for dropping unwanted or invalid samples dynamically during dataset iteration.

- [Introduction](#Introduction)
- [Examples](#Examples)
- [Installation](#Installation)
- [Contributing](#Contributing)
- [Licensing](#Licensing)

---


<a name="Introduction"/>

## Introduction
What if you have a dataset of 1000s of images, out of which a few dozen images are unreadable because the image files are corrupted? Or what if your dataset is a folder full of scanned PDFs that you have to OCRize, and then run a language detector on the resulting text, because you want only the ones that are in English? Or maybe you have an `AlternateIndexSampler`, and you want to be able to move to `dataset[6]` after `dataset[4]` fails while attempting to load!

PyTorch's data processing module expects you to rid your dataset of any unwanted or invalid samples before you feed them into its pipeline, and provides no easy way to define a "fallback policy" in case such samples are encountered during dataset iteration.    

#### Why do I need it?
You might be wondering why this is such a big deal when you could simply `filter` out samples before sending it to your PyTorch dataset or sampler! Well, it turns out that it can be a huge deal in many cases:
1. When you have a small fraction of undesirable samples in a large dataset, or
2. When your sample-loading operation is expensive, or
3. When you want to let downstream consumers know that a sample is undesirable, or
4. When you want your dataset and sampler to be decoupled.

In such cases, it's either simply too expensive to have a separate step to weed out bad samples, or it's just plain impossible because you don't even know what constitutes as "bad", or worse - both!

**nonechucks** allows you to wrap your existing datasets and samplers with "safe" versions of them, which can fix all these problems for you.



<a name="Examples"/>

## Examples

### 1. Dealing with bad samples
Let's start with the simplest use case, which involves wrapping an existing `Dataset` instance with `SafeDataset`.

#### Create a dataset (the usual way)
Using something like torchvision's <a href='https://pytorch.org/docs/stable/torchvision/datasets.html?highlight=folder#torchvision.datasets.ImageFolder'>ImageFolder</a> dataset class, we can load an entire folder of labelled images for a typical supervised classification task.

```python
import torchvision.datasets as datasets
fruits_dataset = datasets.ImageFolder('fruits/')
```
#### Without nonechucks
Now, if you have a sneaky `fruits/apple/143.jpg` (that is corrupted) sitting in your `fruits/` folder, to avoid the entire pipeline from surprise-failing, you would have to resort to something like this:
```python
for i in range(len(fruits_dataset)):
    try:
        image, fruit = fruits[i]
        # Do something with it
    except IOError:
        # Just skip the bad samples
        continue
```
Not only do you have to put your code inside an extra `try-except` block, but you are also forced to use a for-loop, depriving yourself of PyTorch's built-in `DataLoader`, which means you can't use features like batching, shuffling, and custom samplers for your dataset.

I don't know about you, but not being able to do that kind of defeats the whole point of using a data processing module for me.


#### With nonechucks
You can transform your dataset into a `SafeDataset` with a single line of code.
```python
import nonechucks as nc
fruits_dataset = nc.SafeDataset(fruits_dataset)
```
That's it! Seriously.

And that's not all. You can also use a `DataLoader` on top of this.

### 2. Remove undesirable samples dynamically
For this, we will assume a `PDFDocumentsDataset` class which returns the plaintext versions of PDF files inside a folder.
```python
documents = PDFDocumentsDataset(data_dir='pdf_files/')
```
Without **nonechucks**, you would have to do something like:
```python
# Takes a lifetime or two
en_documents = filter(lambda text: detect_language(text) == 'en', list(documents))
dataloader = torch.utils.data.DataLoader(en_documents, batch_size=4, num_workers=4)
for i_batch, sample_batched in enumerate(dataloader):
    ...
```


<a name="Installation" />

## Installation
To install nonechucks, simply use pip:

`$ pip install nonechucks`

or clone this repo, and build from source with:

`$ python setup.py install`.

<a name="Contributing"/>

## Contributing
All PRs are welcome.

<a name="Licensing"/>

## Licensing

**nonechucks** is [MIT licensed](https://github.com/msamogh/nonechucks/blob/master/LICENSE).
