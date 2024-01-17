# EffectorO Tests

## Running EffectorO

Created a conda environment `effectoro.yml` that can be used to run EffectorO

- Code to create conda environment: `conda env create -f [path/to/]effectoro.yml`

Ran EffectorO on `B_lac-SF5.protein.fasta` to test it and it works

## Running EffectorO Before SignalP

Created programs that would run EffectorO first and then SignalP and vice versa

## Extracting Stuff from Munir

- CRN prediction (BlacSF5_CRN.hmm + get_CRN_seqs.sh)
- WY-Domain prediction (WY_fold.hmm + get_WY_seqs.sh)
- RXLR-EER prediction (whisson_et_al_rxlr_eer_cropped.hmm)
- regex searcher for RXLR and EER (regex_searcher.py)
  - **TODO:** change the name to RXLR-EER_regex_searcher.py

## Refactoring the Website

(12/27/2023)

I noticed that Munir included a `requirements.txt` in the GitHub repo, so I decided to try to produce a venv environment out of it. [This is a website that explains how to create virtual environments through venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/). I created an environment under the `.venv` directory. Unfortunately, while trying to install the requirements text file, I encountered this issue:

```text
  error: subprocess-exited-with-error
  
  × Running setup.py install for scikit-learn did not run successfully.
  │ exit code: 1
  ╰─> [33 lines of output]
      Partial import of sklearn during the build process.
      /tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/setup.py:123: DeprecationWarning:
      
        `numpy.distutils` is deprecated since NumPy 1.23.0, as a result
        of the deprecation of `distutils` itself. It will be removed for
        Python >= 3.12. For older Python versions it will remain present.
        It is recommended to use `setuptools < 60.0` for those Python versions.
        For more details, see:
          https://numpy.org/devdocs/reference/distutils_status_migration.html
      
      
        from numpy.distutils.command.build_ext import build_ext  # noqa
      Traceback (most recent call last):
        File "/tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/sklearn/_build_utils/__init__.py", line 32, in _check_cython_version
          import Cython
      ModuleNotFoundError: No module named 'Cython'
      
      During handling of the above exception, another exception occurred:
      
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "/tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/setup.py", line 303, in <module>
          setup_package()
        File "/tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/setup.py", line 299, in setup_package
          setup(**metadata)
        File "/home/nsanc/ucdavis/michelmorelab/kelsey/nsanc-effectoro/.venv/lib/python3.10/site-packages/numpy/distutils/core.py", line 136, in setup
          config = configuration()
        File "/tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/setup.py", line 180, in configuration
          _check_cython_version()
        File "/tmp/pip-install-vi950ui1/scikit-learn_9b26763f7e0b443184b4b5fe99d78180/sklearn/_build_utils/__init__.py", line 35, in _check_cython_version
          raise ModuleNotFoundError(message)
      ModuleNotFoundError: Please install Cython with a version >= 0.28.5 in order to build a scikit-learn from source.
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: legacy-install-failure

× Encountered error while trying to install package.
╰─> scikit-learn

note: This is an issue with the package mentioned above, not pip.
hint: See above for output from the failure.
```

My hunch is that this issue is caused by the incompatibility between the provided scikit-learn version in the requirements text file and the currently run Python version (3.10.12). Based on previous conversations with Kelsey as well as through emails Kelsey provided of Kyle talking about this issue, the scikit-learn version only works with Python version 3.6. After some Googling, I found out that you need to install Python 3.6 onto your computer and then produce the venv while running in version 3.6. I may do this later, but for now I will stick to using the Conda environment I already created.
