from setuptools import setup, find_packages

setup(
    name='etf_analysis_tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'yfinance',
        'matplotlib',
        'seaborn',
    ],
    include_package_data=True,
    description='A Python package for analyzing and optimizing ETF portfolios based on financial and ESG data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/etf-analysis-tools',
    author= 'Paula Palermo, Eitan Razuri Olazo, Daniele Boschetti',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
