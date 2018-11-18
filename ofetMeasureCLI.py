#!/usr/bin/env python
# coding:utf-8
"""
  Author:  Ross Warren <peregrine dot warren at physics dot ox dot ac dot uk>
  Purpose: Run OFET measurements remotely with simple CLI interface
  Created: 17/11/18
"""

import k2636
import time
import click
import pandas as pd
import matplotlib.pyplot as plt

@click.command()
@click.option('--sample', prompt='Please input sample name:', help='Sample name.')
@click.option('--graphic', default=True, help='TRUE or FALSE display measurement in graphic format.')
def main(sample, graphic=True):
    '''Simple program which makes all OFET measurements from CLI.'''
    try:
        print(sample)
        # Set up
        keithley = k2636.K2636()
        begin_measure = time.time()
        # Measurements
        keithley.IVsweep(sample)
        keithley.Output(sample)
        keithley.Transfer(sample)
        # Finish
        keithley.closeConnection()
        finish_measure = time.time()
        print('-------------------------------------------\nAll measurements complete. Total time % .2f mins.'
              % ((finish_measure - begin_measure) / 60))
        if graphic == True:
            plot(sample)

    except ConnectionError:
        print('MEASUREMENT ERROR: Measurement could not be made due to connection issues.')

def plot(sample):
    '''Creates plot of measurements'''
    try:
        df1 = pd.read_csv(str(sample + '-iv-sweep.csv'), '\t')
        df2 = pd.read_csv(str(sample + '-output.csv'), '\t')
        df3 = pd.read_csv(
            str(sample + '-neg-pos-transfer.csv'), '\t')
        df4 = pd.read_csv(
            str(sample + '-pos-neg-transfer.csv'), '\t')
    except FileNotFoundError:
        # If it can't find some data, dont worry :)
        pass

    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    try:
        ax1.plot(df1['Channel Voltage [V]'],
                      df1['Channel Current [A]'] / 1e-6, '.')
        ax1.set_title('I-V sweep')
        ax1.set_xlabel('Channel Voltage [V]')
        ax1.set_ylabel('Channel Current [$\mu$A]')

        ax2.plot(df2['Channel Voltage [V]'],
                      df2['Channel Current [A]'] / 1e-6, '.')
        ax2.set_title('Output curves')
        ax2.set_xlabel('Channel Voltage [V]')
        ax2.set_ylabel('Channel Current [$\mu$A]')

        ax3.semilogy(df3['Gate Voltage [V]'],
                      abs(df3['Channel Current [A]']), '.')
        ax3.set_title('Transfer Curves')
        ax3.set_xlabel('Gate Voltage [V]')
        ax3.set_ylabel('Channel Current [A]')

        ax3.semilogy(df4['Gate Voltage [V]'],
                      abs(df4['Channel Current [A]']), '.')
        ax3.set_title('Transfer Curves')
        ax3.set_xlabel('Gate Voltage [V]')
        ax3.set_ylabel('Channel Current [A]')

        ax4.plot(df3['Gate Voltage [V]'],
                      df3['Gate Leakage [A]'] / 1e-9, '.')
        ax4.set_title('Gate leakage current')
        ax4.set_xlabel('Gate Voltage [V]')
        ax4.set_ylabel('Gate Leakage [nA]')
    except UnboundLocalError:
        pass  # if data isnt there, it cant be plotted
    
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
