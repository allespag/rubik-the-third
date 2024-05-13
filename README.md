# rubik-the-third (42 project)

## Overview

This project was developed as a part of a school project in 2022. The objective of the project, was to design a program capable of solving a Rubik's Cube as efficiently as possible, aiming for both speed and minimal moves.

The notation used for a move is the one used globally (`F` `R` `U` `B` `L` `D` for Front / Right / Up / Back / Left / Down). 

```shell
$ python __main__.py  "B' D2 R2 B' U2 R' B D' U2 R' L' B2 L' F2 B' U' F D' R' F2 U' D' R D' R'"

Loading: rubik/move_tables/edges_orientation.pickle
Loading: rubik/move_tables/corners_orientation.pickle
Loading: rubik/move_tables/UD_slice_permutation.pickle
Loading: rubik/move_tables/exact_UD_slice_permutation.pickle
Loading: rubik/move_tables/corners_permutation.pickle
Loading: rubik/move_tables/not_UD_slice_permutation.pickle
Loading: rubik/pruning_tables/cubies_orientation.pickle
Loading: rubik/pruning_tables/edges_orientation_UD_slice_permutation.pickle
Loading: rubik/pruning_tables/corner_cubies_permutation_exact_UD_slice_pruning.pickle
Loading: rubik/pruning_tables/edges_permutation.pickle

Solving: B' D2 R2 B' U2 R' B D' U2 R' L' B2 L' F2 B' U' F D' R' F2 U' D' R D' R'

Reaching G1 with <U, D, L, R, F, B> ...
Sequence to G1: U L B' L F2 U2 B' D L F

Reaching G2 with <U, D, L2, R2, F2, B2> ...
Sequence to G2: D' R2 D' F2 L2 D R2 F2 D' F2 R2 F2

In 0.03s
U L B' L F2 U2 B' D L F D' R2 D' F2 L2 D R2 F2 D' F2 R2 F2 (22 moves)
```

> ⚠️ Please, note that revisiting the code in 2024 may feel peculiar, as there would likely be numerous changes I'd make if I were to work on it today.

## How to run ?

### Prerequisites

You have `python3.10` and [you're able to create a virtual env](https://docs.python.org/3/library/venv.html)

### Setup

```shell
$ source setup.sh
```

### Usage

```shell
$ python __main__.py --help

usage: rubik [-h] [--random RANDOM] [--perf] [--quiet] [sequence]

positional arguments:
  sequence

options:
  -h, --help            show this help message and exit
  --random RANDOM, -r RANDOM
  --perf, -p
  --quiet, -q
```

## Benchmark

I also created a benchmarking script to assess the performance of my Rubik's Cube solver. It solves multiple cubes, recording statistics like solution length and solve time, aiding in optimization efforts.

```shell
$ python benchmark.py --iter 100 --length 50 --seed "some_random_seed"

Benchmark |████████████████████████████████████████| 100/100 [100%] in 50.3s (1.99/s) 
       time taken  solution length
count  100.000000        100.00000
mean     0.304501         23.81000
std      0.347664          1.17804
min      0.011057         20.00000
25%      0.093276         23.00000
50%      0.178263         24.00000
75%      0.380164         25.00000
max      1.714931         26.00000
```

See `python benchmark.py --help` for details.

## Tests

Some unit tests can be found in `rubik/tests`. Use `pytest rubik/tests`.