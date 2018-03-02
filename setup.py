from setuptools import setup, find_packages

setup(
    name='PyGammaRateCalculator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'numpy',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        getBkgAndGammaRate=PyGammaRateCalculator.scripts.getBkgAndGammaRate:cli 
        calCrabPulsarRate=PyGammaRateCalculator.scripts.calCrabPulsarRate:cli
    '''
)
