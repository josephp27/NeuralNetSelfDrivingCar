# CNN Self Driving Car
```
Install required libraries:
    pip install -r requirements.txt

Run:
    python reader32.py  -  Collect screen frames for training data
    python balance_data.py  -  Balances Data frames
    python train_model.py  -  Trains Alexnet model
```

## reader32.py

* Uses Win32 API to grab screen

* 1024x768 Resolution

## reader.py

* Uses OpenCV to grab screen

* 1024x768 Resolution


