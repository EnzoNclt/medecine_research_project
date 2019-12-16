# medecine_research_project
Medicinal project for the State University Of Telecoms of Saint Petersburg

## Installation
* Clone this repository
* In a dist folder, import your assets and pictures for image recognition
* Create a virtual environment with python virtualenv by the following command:
    
```
    virtualenv --python=/usr/bin/python3 venv
```
* Activate the environment with:
 
For Bash Users:
```
    source venv/bin/activate
```

For Fish Users:
 ```
    source venv/bin/activate.fish
 ```

* Once the environment is enabled, install the following packages:
```
    pip install opencv-python imutils scikit-image
```

## Usage
To compare two separates images and view the result of the comparison using the find_diff.py script, type the following command:
```
    python find_diff_img.py -f path_to_first_image.jpg -s path_to_second_image.jpg
```

To compare one image with a whole folder, to make the SSIM coeficient, use the file_logic.py and type the following command:
```
    python file_logic.py -f path_to_folder -s path_to_image.jpg
```