#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# sudoku_matrix.py module testings
from sudoku_matrix import *

# get stats
from statistics import mean

# get chronometer
from timeit import timeit

# session start
print("\n--- BEGIN TEST SESSION ---")


# -------------------------- MODULE FUNCTION DEFS ----------------------


# main test
def test_main (level=1, qty=20):
    # grid generation test
    matrix = SudokuMatrix()
    # stats data inits
    data = list()
    print("\n" + "-" * 60)
    print("\nTesting: {}".format(matrix.__class__.__name__))
    print("\nGeneration complexity level:", level)
    print()
    # let's make some tests
    for n in range(qty):
        # generate grid
        t = timeit(lambda:matrix.generate(level), number=1)
        print("[LERS2] grid generated in: {:0.6f} sec".format(t))
        # add to stats data
        data.append(t)
        # reveal answer
        matrix.reveal()
        # verify: erroneous grid?
        if not matrix.verify_correct():
            print(matrix)
            print("\n[ERROR] incorrect grid!")
            return
        # end if
    # end for
    print("\n[TOTAL] nb of generated grids:", qty)
    print(
        "\n[STATS] average grid generation time: {:0.6f} sec"
        .format(mean(data))
    )
    print("\n[SUCCESS] all grids have been tested OK.")
# end def


# detailed testing of shuffle algorithms
def test_shuffle (algo=2, qty=10):
    print("\n" + "-" * 60)
    print("\nTesting shuffle algorithms\n")
    matrix = SudokuMatrix()
    matrix.generate()
    matrix.reveal()
    print(">>> GENUINE matrix:")
    print(fancy_grid(matrix))
    print(
        "matrix is correct: {}"
        .format(matrix.verify_correct())
    )
    # force shuffling
    for i in range(qty):
        print(
            "\n({}): shuffling matrix with algo_shuffle_{}()"
            .format(i + 1, algo)
        )
        exec("matrix.algo_shuffle_{}()".format(algo))
        print(fancy_grid(matrix))
        ok = matrix.verify_correct()
        print("matrix is correct: {}".format(ok))
        if not ok:
            print("\n[ERROR] matrix is INCORRECT!")
            return
        # end if
    # end for
# end def


# trying with Euler's latin square
def test_euler_latin_square ():
    print("\n" + "-" * 60)
    print("\nTrying with Euler's latin square (module function):\n")
    data = euler_latin_square()
    print(fancy_grid(data))
    print(
        "\ngenerated grid in {:0.6f} sec"
        .format(timeit(euler_latin_square, number=1))
    )
    print(
        "\nverified grid in {:0.6f} sec"
        .format(timeit(lambda:is_correct_grid(data), number=1))
    )
    print("\ngrid is correct:", is_correct_grid(data))
# end def


# trying with LERS2 Sudoku grid module's function
def test_lers2_module ():
    print("\n" + "-" * 60)
    print("\nTrying with LERS2 Sudoku grid (module function):\n")
    data = lers2_sudoku_grid()
    print(fancy_grid(data))
    print(
        "\ngenerated grid in {:0.6f} sec"
        .format(timeit(lers2_sudoku_grid, number=1))
    )
    print(
        "\nverified grid in {:0.6f} sec"
        .format(timeit(lambda:is_correct_grid(data), number=1))
    )
    print("\ngrid is correct:", is_correct_grid(data))
# end def


# ----------------------------- NOW TESTING -------------------------

test_main(level=4, qty=20)

#~ test_shuffle(algo=4, qty=5)

#~ test_euler_latin_square()

#~ test_lers2_module()

print("\n--- END OF TEST SESSION ---")
