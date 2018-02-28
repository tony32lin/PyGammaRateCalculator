import numpy as np
import pandas as pd
import click
@click.command()
@click.option('--pulsar_si','-p',multiple=True,type=float)
@click.option('--nebula_si','-n',multiple=True,type=float)
@click.option('--emin','-e',multiple=True,type=float)
@click.option('--ofname','-o',nargs=1,type=str)
@click.option('--e0','-k',nargs=1,default=150,type=float)
@click.option('--irf','-f',nargs=2,multiple=True,type=click.Tuple([float,click.Path(exists=True)]))
def cli(pulsar_si,nebula_si,emin,ofname,e0,irf):
    #check if both pulsar_si nebula_si and Emin are at least one value
    if(len(pulsar_si) ==0 or len(nebula_si) ==0 or len(emin) ==0):
        click.echo(cli.get_help(click.Context(cli)) )
        raise click.Abort()
    if(len(irf) == 0):
        click.echo(cli.get_help(click.Context(cli)) )
        raise click.Abort()
       
    if(ofname is None):
        click.echo(cli.get_help(click.Context(cli)) )
        raise click.Abort()
    norm_P2 = 7.1e-14 *10000*np.power(e0/1000,-3.0) # MAGIC A&A @150GeV
    norm_nebula = 3.10e-11*10000*np.power(e0/1000,-2.5)#TeV^-1 m^-2 s^-1 @ 1TeV 
    # As loading ROOT takes time, I move import here.
    import PyGammaRateCalculator.scripts.getExpRateDF as c
    emin_TeV = [e/1000 for e in emin]
    df_l = []
    for ze,irfname in irf:
        df = c.getExpRateDF(irfname,ze,
                            emin_TeV,pulsar_si,nebula_si,norm_P2,norm_nebula,E0=e0/1000)
        df_l.append(df)
    df = pd.concat(df_l)
    df['E0'] = df['E0']*1000
    df['EPrimeMin'] = df['EPrimeMin']*1000
    df.to_csv(ofname,index=False)

if __name__ == '__main__':
   cli()
