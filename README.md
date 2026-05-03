# Image Processing Pipeline

A parallel image processing pipeline built with Python, using metaprogramming
and concurrent programming techniques.

## Features

- Automatic filter registration using a custom metaclass (metaprogramming)
- Parallel image processing using Python's multiprocessing module
- 10 built-in image filters
- Easy to extend with new filters

## Project Structure

```
image-processing/
├── inputs/          # Place your images here
├── outputs/         # Processed images will appear here
├── pipeline/
│   ├── base.py      # Metaclass and base pipeline
│   └── filters.py   # Image filters
├── processing/
│   └── worker.py    # Concurrent processing logic
├── utils/
│   └── loader.py    # Image loading and saving
├── main.py          # Entry point
└── requirements.txt
```

## Available Filters

- `grayscale` - Convert image to grayscale
- `blur` - Apply Gaussian blur
- `sharpen` - Sharpen the image
- `edge_detection` - Detect edges
- `brighten` - Increase brightness by 50%
- `darken` - Decrease brightness by 50%
- `increase_contrast` - Increase contrast
- `invert` - Invert pixel colors
- `flip_horizontal` - Flip image horizontally
- `flip_vertical` - Flip image vertically

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt

## Usage

1. Place your images in the `inputs/` folder
2. Configure the filters you want to apply in `main.py`:
```python
STEPS = [
    "grayscale",
    "blur",
    "sharpen",
]
```
3. Run the pipeline:
python main.py
4. Check the `outputs/` folder for results

## Technologies

- Python 3.13
- Pillow
- OpenCV
- NumPy