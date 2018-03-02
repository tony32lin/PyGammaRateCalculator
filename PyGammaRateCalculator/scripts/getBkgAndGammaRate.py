import numpy as np
import pandas as pd

import click

@click.command()
@click.argument('anasum_file',nargs=1,type=click.Path(exists=True))
@click.argument('output_file',nargs=1,type=str)
@click.option('--ecut','-e',multiple=True,type=float)
def cli(anasum_file,output_file,ecut):
    from PyGammaRateCalculator.utils.anasum_handling import getElevationBkgRate 
    if(len(ecut) == 0):
        click.echo(cli.get_help(click.Context(cli)) )
        raise click.Abort()
    ecut = [e/1000 for e in ecut]
    df = getElevationBkgRate(anasum_file,ecut)
    df['Ecut'] = df['Ecut']*1000
    df.to_csv(output_file,index=False)

if __name__ == '__main__':
   cli()
