# pictory

Simple tool to organize pictures and videos in lickable directories

## Installation

Simply use `pip`

```
pip install pictory
```

or `pipenv`

```
pipenv install pictory
```

## Usage

`python pictory.py <path>`

## End result

from
```
20130907_200910.jpg
20131102_231549.jpg
VID_20180106_230942390.mp4
VID_20180202_211303150.mp4
20130629_005059.jpg
20131022_155432_9.jpg
20131027_242914.jpg
VID_20150328_165952.mp4
VID_20150328_170016.mp4
VID_20150329_130832.mp4
```

to
```
├───images
│   └───2013
│       ├───June
│       │       20130629_005059.jpg
│       │
│       ├───November
│       │       20131102_231549.jpg
│       │
│       ├───October
│       │       20131022_155432_9.jpg
│       │       20131027_242914.jpg
│       │
│       └───September
│               20130907_200910.jpg
│
└───videos
    ├───2015
    │   └───March
    │           VID_20150328_165952.mp4
    │           VID_20150328_170016.mp4
    │           VID_20150329_130832.mp4
    │
    └───2018
        ├───February
        │       VID_20180202_211303150.mp4
        │
        └───January
                VID_20180106_230942390.mp4
```
