# Resize and Crop

## Description

Resize and crop an image to fit the specified size.

## Installation

```python
pip install resize-and-crop
```

or

```python
pipenv install resize-and-crop
```

## Methods

1. resize_and_crop(path, size, crop_origin) - Resize the image located at path, into the size specified, cropping the image starting at the crop_origin.
2. resized_image_file(image_field, format, dimensions, crop_origin) - Returns a new image file that has the resized image. Can be used to save to a Django ImageField.

## Usage

```python
from resize_and_crop import resize_and_crop

image = resize_and_crop("/path/to/image", (200,200), "middle")
```

```python
from django.db import models
from resize_and_crop.utils import resized_image_file

class ExampleModel(models.Model):
	image = models.ImageField(upload_to="images/")
	thumbnail = models.ImageField(upload_to="thumbnails/")

	def save(self, *args, **kwargs):
		if self.image and not self.thumbnail:
			self.thumbnail = resized_image_file(
				self.image,
				"jpeg",
				(200, 200),
			)
		return super().save(*args, **kwargs)
```
