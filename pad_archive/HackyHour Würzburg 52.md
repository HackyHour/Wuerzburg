# HackyHour Würzburg 52

## Virtual!
 - **When:** December 17<sup>th</sup>, 2020 at 5:00pm :warning: it is the 3<sup>rd</sup> Thursday this month 
 - **Where:** :exclamation: Virtual! :exclamation:
 - **Zoom:** 
   - https://uni-wuerzburg.zoom.us/j/91208057434?pwd=aE9XMng1bzBiRVpMaW5OdTBiZHo0dz09
   - Meeting ID: 912 0805 7434
   - Password: 827471
 - **Info:** [HackyHour Website](http://hackyhour.github.io/Wuerzburg/)
 - :vertical_traffic_light: As long as the covid numbers are high in Würzburg we can not meet in person :cry: That won't keep us from having fun, though! :computer: 

## Topic Suggestions
> Add your :+1: to the end of a line you are interested in
- Figure out how to get multiple output formats (.doc, .tex, .Rmd) with [(R bookdown package & Co)](https://bookdown.org/). :+1: :+1: :+1: 
 - Practice Data Science Skills: [TidyTuesday](https://github.com/rfordatascience/tidytuesday) + TidyVerse
 - [Project Euler](https://projecteuler.net/)
 - [AdventOfCode](https://adventofcode.com/) or [Mathekalender](https://www.mathekalender.de/index.php?&lang=en) :+1: :+1: 
 https://hackmd.io/QI0mcw2zTgSmb_vPI7XQvA
 - Say it challenge (hacker.org) [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis), [LibROSA](https://librosa.github.io/librosa/), [silero](https://pytorch.org/hub/snakers4_silero-models_stt/), [wav2vec 2.0](https://ai.facebook.com/blog/wav2vec-20-learning-the-structure-of-speech-from-raw-audio)

## Maybe another time
 - 3D Modelling, Blender, VR programming (maybe invite Annika K.)
 - [GenForce](https://github.com/genforce/genforce) - *An efficient PyTorch library for deep generative modeling. May the Generative Force (GenForce) be with You.*
 - Tidy Time Series Analysis in R: [tidyverts](https://tidyverts.org/)
 - [A challenge platform](https://ctfd.io/) for data science

## Participants
> Please add your name and indicate if you prefer to join remotely :computer: and if you want to order pizza :pizza: 
 - Markus :computer: :pizza: 
 - Ludmilla
 - Frank (partially) :computer: or :desktop_computer:; no :pizza: for me
 - Rick :computer: :microscope: 
 - Franzi (I will join around 5:30 pm)
 - Hannah

## Advent of Code Coding Dojo

[AdventOfCode](https://adventofcode.com/)
### Day 1

#### Part I
```python
import numpy as np

input = np.loadtxt('input')
for i in range(len(input)):
    for j in range((i + 1), len(input)):
        s = input[i] + input[j]
        if s == 2020:
            print(input[i]*input[j])
```

#### Part II
```python
import numpy as np

input = np.loadtxt('input')
for i in range(len(input)):
    for j in range((i + 1), len(input)):
        for k in range((j+1), len(input)):
            s = input[i] + input[j] + input[k]
            if s == 2020:
                print(input[i]*input[j]*input[k])
```

### Day 2

#### Part I
```python
with open('input') as entry:
    lines = entry.readlines()
    valid = 0
    for l in lines:
        parts = l.split()
        print(parts)
        occurences = parts[0].split('-')
        letter = parts[1][0]
        print(occurences, letter)
        if letter in parts[2]:
            c = parts[2].count(letter)
            if c >= int(occurences[0]) and c <= int(occurences[1]):
                valid += 1
    
    print(valid)        
```

#### Part II
```python
with open('input') as entry:
    lines = entry.readlines()
    valid = 0
    for l in lines:
        parts = l.split()
        print(parts)
        occurences = parts[0].split('-')
        letter = parts[1][0]
        print(occurences, letter)
        if letter == parts[2][int(occurences[0])-1]:
            if letter != parts[2][int(occurences[1])-1]:
                valid += 1
        if letter == parts[2][int(occurences[1])-1]:
            if letter != parts[2][int(occurences[0])-1]:
                valid += 1
    print(valid)
```

### Day 3
#### Part I
```python
with open('input') as entry:
    lines = entry.readlines()
    lines = [l.strip() for l in lines]
    x = 0
    y = 0
    tree = 0
    while y < len(lines)-1:
        x += 3
        x = x%len(lines[0])
        y += 1
        if lines[y][x] == '#':
            tree += 1
    print(tree)
```

- Right 1, down 1.
- Right 3, down 1. (This is the slope you already checked.)
- Right 5, down 1.
- Right 7, down 1.
- Right 1, down 2.

#### Part II
```python
with open('input') as entry:
    lines = entry.readlines()
    lines = [l.strip() for l in lines]
    treeproduct = 1
    xsteps = [1,3,5,7,1]
    ysteps = [1,1,1,1,2]
    for i in range(5):
        x = 0
        y = 0
        tree = 0
        while y < len(lines)-1:
            x += xsteps[i]
            x = x%len(lines[0])
            y += ysteps[i]
            if lines[y][x] == '#':
                tree += 1
        treeproduct *= tree
    print(treeproduct)
```

### Day 4

#### Part I


    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)


```python
with open('input') as entry:
    count  = 0
    line = entry.readline()
    line = line.strip()
    while line:
        pass_dict = {}
        while line != '':
            pairs = line.split()
            for i in range(len(pairs)):
                pair = pairs[i].split(':')
                pass_dict[pair[0]] = pair[1]
            line = entry.readline()
            line = line.strip()
        if 'byr' in pass_dict:
            if 'iyr' in pass_dict:
                if 'eyr' in pass_dict:
                    if 'hgt' in pass_dict:
                        if 'hcl' in pass_dict:
                            if 'ecl' in pass_dict:
                                if 'pid' in pass_dict:
                                     count = count +1
        line = entry.readline()
        line = line.strip()
    print(count)
#     print()
   # pass_dict = {}
   # pass_dict[''] = 
```

#### Part II


    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.


```python=
import re

with open('input') as entry:
    count  = 0
    line = entry.readline()
    line = line.strip()
    while line:
        pass_dict = {}
        while line != '':
            pairs = line.split()
            for i in range(len(pairs)):
                pair = pairs[i].split(':')
                pass_dict[pair[0]] = pair[1]
            line = entry.readline()
            line = line.strip()
        if 'byr' in pass_dict and int(pass_dict['byr'])>=1920 and int(pass_dict['byr'])<=2002:
            if 'iyr' in pass_dict and int(pass_dict['iyr'])>=2010 and int(pass_dict['iyr'])<=2020:
                if 'eyr' in pass_dict and int(pass_dict['eyr'])>=2020 and int(pass_dict['eyr'])<=2030:
                    if 'hgt' in pass_dict:
                        hgt = pass_dict['hgt']
                        number = int(hgt[:-2])
                        unit = hgt[-2:]
                        if (unit == "cm" and number >= 150 and number <= 193) or (unit == 'in' and 59 <= number <= 76):
                            if 'hcl' in pass_dict and re.match('^#[0-9a-f]{6}$',pass_dict['hcl']):
                                if 'ecl' in pass_dict and (pass_dict['ecl'] == 'amb' or pass_dict['ecl'] == 'blu' or pass_dict['ecl'] == 'brn' or pass_dict['ecl'] == 'gry' or pass_dict['ecl'] == 'grn' or pass_dict['ecl'] == 'hzl' or pass_dict['ecl'] == 'oth'):
                                    if 'pid' in pass_dict:
                                        if len(pass_dict['pid']) == 9 and pass_dict['pid'].isnumeric():
                                            count = count +1
        line = entry.readline()
        line = line.strip()
    print(count)
#     print()
   # pass_dict = {}
   # pass_dict[''] = 
```


## Cross Links
 - [previous pad](https://hackmd.io/ye4RC_FWTN2ehxkfT9cusQ)
 - [next pad](https://hackmd.io/hB_NPVCrSY2ROozic3z7wg)
