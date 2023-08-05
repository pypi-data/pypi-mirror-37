cmsbooklet
==========

Introduction
------------

cmsbooklet is a tool meant to facilitate the typesetting of olympic problems. It is designed to work well with [CMS](https://github.com/cms-dev/cms), the Contest Management System.

Dependencies
------------

Ensure that you have the texlive suite installed, and check that the `latexmk` command is available (on some distros you have to install it explicitly but on the serious ones, like ArchLinux, it's installed by default with the standard texlive package).

Installation
------------

To install the `cmsbooklet` command, we recommend that you use a Python *virtual environment*. So, ensure that you have the `virtualenv` command available. You can install it by typing:

* `sudo apt-get install python3-virtualenv` on **Ubuntu 18.04**.
* `sudo pacman -S python-virtualenv` on **Arch Linux**.

Then run:

```bash
$ python3 -m venv ~/my_venv
```

Where `my_venv` can be anything you want. Then activate it:

```bash
$ source ~/my_venv/bin/activate
```

You should now see that the command line prompt has changed to something like:

```bash
(my_venv) $
```

Now you can freely install cmsbooklet by issuing this command:

```bash
(my_venv) $ pip install cmsbooklet
```

Usage
-----

Once installed, you can use the `cmsbooklet` command like this: put yourself in a directory where a `contest.yaml` file is present, then run the following command.

```bash
(my_venv) $ cmsbooklet -t cms-contest -l italian contest.yaml
```

Further options
---------------

// TODO
cmsbooklet supports these flags:
  - `--keep`: keeps working files
