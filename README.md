# Load Switching
### [NeoCharge](https://www.getneocharge.com/shop-pages/smart-splitters) smart splitter simulator program.


## Project Description
This program iterates through two directories of profiles and processes them in parallel to each other. dryer_profiles_feeder contains dryer profiles, which are assigned as the primary loads whereas EV_profiles_feeder contains EV profiles as the secondary loads. Each profile is considered "on" at a threshold of 100W. The program implements switching so that the primary and the secondary cannot be on at the same time. In the event that both the primary and the secondary are on, the program prioritizes the primary while deferring the secondary to when the primary is off. This is shown in more detail in the illustration below. This program creates a new directory (switched_data) that contains all the switched outputs from the primaries and the secondaries. 


![illustration](https://user-images.githubusercontent.com/60201315/110606728-54c43680-813f-11eb-9497-92a0c363f417.png)


## Requirements
This program only works on Windows due to the directory convention used.
```
pip install numpy matplotlib
```

### To get the code
```
git clone https://github.com/neighdeen84/Load_Switching_1.git
```


## Usage
```
cd Load_Switching_1
python main.py
```


