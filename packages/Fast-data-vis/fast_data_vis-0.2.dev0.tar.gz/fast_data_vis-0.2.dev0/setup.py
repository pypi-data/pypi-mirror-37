from distutils.core import setup
import setuptools

setup(
    name='fast_data_vis',
    version='0.2dev',
    install_requires=['fast_data_vis', 'pandas', 'matplotlib', 'wordcloud', 'plotly'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    url=''
)