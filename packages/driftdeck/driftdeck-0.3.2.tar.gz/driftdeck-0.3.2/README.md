# driftdeck

Drift Deck eats markdown files and spits out beautiful slides directly into your browser.

## How do you use it?

```
$ driftdeck myslides.md
```

Your web browser should open a a new tab at `http://localhost:{SOMEPORT}/1` and display your slides.

## Where can you get it?

### [PyPI][pypi]

```
pip install driftdeck
```

### [Archlinux AUR][aur]

```
pacaur -S python-driftdeck
```

### [Gitlab][gitlab]

```
git clone https://gitlab.com/XenGi/driftdeck
```

## How can you improve it?

You need poetry which you can install with pipsi:

```
pipsi install poetry
```

Then clone the repo, install the dependencies and run it:

```
git clone https://gitlab.com/XenGi/driftdeck
cd driftdeck
poetry install
poetry run driftdeck
```


[pypi]: https://pypi.org/project/driftdeck/
[aur]: https://aur.archlinux.org/packages/python-driftdeck/
[gitlab]: https://gitlab.com/XenGi/driftdeck
