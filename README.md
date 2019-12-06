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
To use the find_diff.py script, type the following command:
```
    python find_diff_img.py -f first_image.jpg -s second_image.jpg
```