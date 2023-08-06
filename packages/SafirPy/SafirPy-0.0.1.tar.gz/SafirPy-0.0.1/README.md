# SFESafirPy

Introduction is on the way.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```sh
python>=3.6.0
matplotlib==2.2.2
numpy==1.15.0
pandas==0.23.3
scipy==1.1.0
seaborn==0.9.0
```

### Installation

#### pip
pip is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python ](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

SafirPy uses Python, and as of Oct 2018 SafirPy only works in Python3. 

1.	If you are using Windows with Python version 3.3 or higher, use the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html?highlight=shebang#python-launcher-for-windows) to use `pip` with Python version 3:
    ```sh
    pip install sfeprapy
    ```
2.	If your system has a `python3` command (standard on Unix-like systems), install with:
    ```sh
    python3 -m pip install sfeprapy
    ```
3.	You can also just use the `python` command directly, but this will use the _current_ version of Python in your environment:
    ```sh
    python -m pip install sfeprapy
    ```

### Usage

In Python, enter the following code will run the time equivalence (Monte Carlo) analysis which will ask for input files directory.
```python
>>> from safirpy import safir_mc_app as app
>>> app.run()
```

## Authors

* License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
