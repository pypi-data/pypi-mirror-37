# [NA-Birds](http://dl.allaboutbirds.org/nabirds) dataset wrapper

For more deatils to see how to use this library take a look at [nabirds/display.py](nabirds/display.py).

## Annotation and Image Loading

Here is some example code how to load images and use the predefined train-test split.

```python
# replace NAB_Annotations with CUB_Annotations to load CUB200-2011 annotations
from nabirds import NAB_Annotations, Dataset

annot = NAB_Annotations("path/to/nab/folder")

train_data = Dataset(annot.train_uuids, annot)
test_data = Dataset(annot.test_uuids, annot)

print("Loaded {} training and {} test images".format(len(train_data), len(test_data)))
```

## Dataset Iteration
```python
import matplotlib.pyplot as plt

# either access the images directly
im, parts, label = test_data[100]
plt.imshow(im)
plt.show()

# or iterate over the dataset
for im, parts, label in train_data:
    plt.imshow(im)
    plt.show()

```

## Working with Part Annotations
Both datasets (NAB and CUB) have part annotations. Each annotation has for each of the predefined parts the location of this part and a boolean (`0` or `1`) value whether this part is visible. A [`Dataset`](nabirds/dataset/__init__.py#L5) instance returns besides the image and the class label this information:

```python

im, parts, label = train_data[100]

print(parts)
# array([[  0, 529, 304,   1],
#        [  1, 427, 277,   1],
#        [  2, 368, 323,   1],
#        [  3,   0,   0,   0],
#        [  4, 449, 292,   1],
#        [  5, 398, 502,   1],
#        [  6, 430, 398,   1],
#        [  7,   0,   0,   0],
#        [  8, 365, 751,   1],
#        [  9,   0,   0,   0],
#        [ 10,   0,   0,   0]])

```
### Visible Parts

In order to filter by only visible parts use the [`utils.visible_part_locs`](nabirds/dataset/utils.py#L28) function. It returns the indices and the x-y positions of the visible parts:

```python
from nabirds import utils

idxs, xy = utils.visible_part_locs(parts)

print(idxs)
# array([0, 1, 2, 4, 5, 6, 8])
print(xy)
# array([[529, 427, 368, 449, 398, 430, 365],
#        [304, 277, 323, 292, 502, 398, 751]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
```

### Uniform Parts
In case you don't want to use the ground truth parts, you can generate parts uniformly distributed over the image. Here you need to pass the image as well as the ratio, which tells how many parts will be extracted (ratio of `1/5` extracts 5 by 5 parts, resulting in 25 parts). In case of uniform parts all of them are visible.


```python
from nabirds import utils

parts = utils.uniform_parts(im, ratio=1/3)
idxs, xy = utils.visible_part_locs(parts)

print(idxs)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8])
print(xy)
# array([[140, 420, 700, 140, 420, 700, 140, 420, 700],
#        [166, 166, 166, 499, 499, 499, 832, 832, 832]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
```

### Crop Extraction
From the locations we can also extract some crops. Same as in [`utils.uniform_parts`](nabirds/dataset/utils.py#L9) you have to give a ratio with which the crops around the locations are created:

```python
from nabirds import utils

part_crops = utils.visible_crops(im, parts, ratio=0.2)

fig = plt.figure(figsize=(16,9))
n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in enumerate(part_crops, 1):
    ax = fig.add_subplot(rows, cols, j)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
```


### Random Crops
In some cases randomly selected crops are desired. Here you can use the [`utils.random_select`](nabirds/dataset/utils.py#L68) function. As optional argument you can also pass a `rnd` argument, that can be an integer (indicating a random seed) or a `numpy.random.RandomState` instance. Additionally, you can also determine the number of crops that will be selected (default is to select random number of crops).

```python
from nabirds import utils

rnd_idxs, rnd_xy, rnd_part_crops = utils.random_select(idxs, xy, part_crops)

fig = plt.figure(figsize=(16,9))

n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in zip(rnd_idxs, rnd_part_crops):
    ax = fig.add_subplot(rows, cols, j + 1)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
```


### Revealing of the Parts
In order to create a single image, that consist of the given parts on their correct location use [`utils.reveal_parts`](nabirds/dataset/utils.py#L57) function. It requires again besides the original image and the locations the ratio with which the parts around the locations should be revealed:

```python

plt.imshow(reveal_parts(im, xy, ratio=0.2))
plt.show()

plt.imshow(reveal_parts(im, rnd_xy, ratio=0.2))
plt.show()
```


## Hierarchies
Hierachy file is currently only loaded. Code for proper processing is needed!
