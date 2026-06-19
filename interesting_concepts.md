# Interesting Python Concepts

This file collects Python concepts from the book that are worth remembering.

## Imports, `sys.path`, `sys.modules`, and Reloading Modules

When you write:

```python
import mymod
```

Python does two related but separate things:

1. It looks for and loads the module.
2. It defines a variable named `mymod` in the current namespace.

For a module named `mymod`, Python searches for a file such as `mymod.py` in several directories. Those directories are stored in the list:

```python
sys.path
```

You can inspect it with:

```python
import sys

print(sys.path)
```

If Python finds `mymod.py` in one of those directories, it loads the file and stops searching.

### `sys.path`

`sys.path` is a list of strings representing the directories where Python looks for modules.

There are several ways to modify `sys.path`, including:

- Setting the `PYTHONPATH` environment variable.
- Creating `.pth` files inside the Python installation's `site-packages` directory.
- Modifying `sys.path` directly from Python code.

Example:

```python
import sys

sys.path.append("/path/to/my/modules")
```

After doing that, Python will also search that directory when importing modules.

### Modules Are Loaded Only Once

Python normally loads a module only the first time it is imported.

For example:

```python
import mymod
import mymod
import mymod
```

The module file is only loaded and executed the first time. The later imports just reuse the already loaded module.

This is especially important when different modules import the same dependency. For example, if a program imports both `pandas` and `scipy`, and both of them import `numpy`, Python does not load `numpy` twice. It loads it the first time and then reuses it.

### `sys.modules`

Python keeps track of loaded modules in:

```python
sys.modules
```

`sys.modules` is a dictionary:

- The keys are module names.
- The values are the actual module objects.

Example:

```python
import sys
import math

print("math" in sys.modules)
```

This prints:

```text
True
```

because `math` has already been imported.

So when Python sees:

```python
import mymod
```

it roughly follows this logic:

```text
Is "mymod" already in sys.modules?
Yes -> reuse the existing module object and define the name mymod.
No  -> search for it in sys.path, load it, store it in sys.modules, and define the name mymod.
```

### Reloading a Module During Development

This behavior is useful because most programs do not need to reload the same module again and again.

However, it can be confusing during interactive development.

Suppose `mymod.py` contains:

```python
def greet():
    print("Hello")
```

Then, in an interactive Python session:

```python
import mymod

mymod.greet()
```

Output:

```text
Hello
```

Now imagine you edit `mymod.py`:

```python
def greet():
    print("Hello, changed")
```

If you run this again in the same Python session:

```python
import mymod
mymod.greet()
```

Python may still print:

```text
Hello
```

because `mymod` was already loaded and stored in `sys.modules`.

To force Python to reload the module, use `importlib.reload`:

```python
import importlib
import mymod

importlib.reload(mymod)
```

After that, Python reads `mymod.py` again.

### Key Takeaway

`import` normally loads a module only once, but it can define the requested variable name many times.

In short:

```text
import mymod
```

means:

```text
Find mymod.py.
Load it if it has not already been loaded.
Store it in sys.modules.
Define the name mymod.
```

And:

```python
importlib.reload(mymod)
```

means:

```text
Reload mymod.py even though it was already imported.
```

This is useful in interactive development, but it is rarely needed in normal production code.

## The `if __name__ == "__main__"` Pattern

One of the most common lines in Python is:

```python
if __name__ == "__main__":
```

This line checks whether a Python file is being run directly or imported as a module by another file.

When Python loads a module, it executes the code in that file from top to bottom. This means that a module does not only define functions, classes, or variables. Any top-level code in the file also runs.

For example:

```python
# mymod.py

print("This always runs")

def hello():
    print("Hello")

if __name__ == "__main__":
    print("This only runs when mymod.py is executed directly")
```

If you run the file directly:

```bash
python mymod.py
```

the output is:

```text
This always runs
This only runs when mymod.py is executed directly
```

But if another file imports it:

```python
import mymod
```

the output is only:

```text
This always runs
```

The code inside the `if __name__ == "__main__"` block does not run when the file is imported.

### The `__name__` Variable

`__name__` is a special variable automatically set by Python.

Its value depends on how the file is being used:

- If the file is run directly, `__name__` is set to `"__main__"`.
- If the file is imported, `__name__` is set to the module's name.

So this condition:

```python
if __name__ == "__main__":
```

means:

```text
Only run the code below if this file is the main program being executed.
Do not run it if this file is being imported.
```

### Why This Is Useful

This pattern lets a file work in two different ways:

- As a reusable module that can be imported.
- As a script that can be executed directly.

Example:

```python
# calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print(add(2, 3))
    print(subtract(10, 4))
```

If another file imports `calculator`, it can use the functions without running the test code:

```python
import calculator

print(calculator.add(5, 7))
```

But if `calculator.py` is run directly:

```bash
python calculator.py
```

then the code inside the `if __name__ == "__main__"` block runs.

### Common Uses

This pattern is often used to:

- Run quick tests or demonstrations when the file is executed directly.
- Start an interactive command-line program.
- Keep reusable function definitions separate from executable script logic.
- Avoid running script code when a module is imported.
- Prevent issues in some multiprocessing code, especially on Windows.

Although it is possible to use this condition multiple times in one file, it is usually written once, near the end of the module.

A common structure is:

```python
def main():
    print("Program starts here")

if __name__ == "__main__":
    main()
```

This keeps the program organized:

- `main()` contains the main logic.
- The `if __name__ == "__main__"` block decides whether to run it.

### Key Takeaway

```python
if __name__ == "__main__":
```

means:

```text
If this file is being run directly, execute this block.
If this file is being imported, ignore this block.
```

## `__all__`

`__all__` is a module-level variable that contains a list of strings.

It tells Python which names should be exported when another file uses:

```python
from module import *
```

Example:

```python
__all__ = ["greet", "User"]

def greet():
    print("Hello")

class User:
    pass

def internal_function():
    pass
```

With this definition:

```python
from module import *
```

Python imports `greet` and `User`, but not `internal_function`.

### Key Takeaway

`__all__` is not special syntax for creating a list of strings.
It is a normal variable name that Python recognizes when using wildcard imports.

## Modules vs. Packages

Python uses the terms **module**, **package**, and **distribution package** for
related but different concepts.

### Modules

A module is a single Python file with a `.py` extension:

```text
first.py
```

It can be imported and its attributes can be accessed through the module name:

```python
import first

print(first.x)
```

Modules are useful for separating reusable functions, classes, constants, and
other code from the main program.

### Python Packages

A Python package is a directory that groups related modules:

```text
mypackage/
├── __init__.py
├── first.py
├── second.py
└── third.py
```

The package directory must be somewhere Python can find it, normally in the
current project, in the environment's installed packages, or in another
directory listed in `sys.path`.

A module inside the package can be imported in different ways:

```python
from mypackage import first

print(first.x)
```

Alternatively:

```python
import mypackage.first

print(mypackage.first.x)
```

The first form binds the shorter name `first` in the current file. The second
form keeps the complete name `mypackage.first`.

### The `__init__.py` File

When Python imports a regular package, it executes the package's
`__init__.py` file:

```python
import mypackage
```

The file can be empty, perform package initialization, or expose selected
objects from internal modules:

```python
# mypackage/__init__.py
from .first import x
```

The leading dot means that `first` is imported relative to the current
package. After this, users can access `x` directly:

```python
import mypackage

print(mypackage.x)
```

Modern Python also supports namespace packages, which can exist without an
`__init__.py` file. Nevertheless, regular packages commonly include it because
it makes the package boundary explicit and allows its public interface to be
defined.

### Distribution Packages

The word **package** is also used for a distribution: a project that can be
built, installed with `pip`, and optionally published on PyPI.

A distribution package wraps the importable Python package together with
metadata and supporting files:

```text
mypackage-project/
├── pyproject.toml
├── README.md
├── LICENSE
├── tests/
└── mypackage/
    ├── __init__.py
    └── first.py
```

It can describe:

- The project name and version.
- The author and license.
- Supported Python versions.
- Runtime and development dependencies.
- Build-system configuration.
- Tests and installation information.

Historically, Python projects put much of this configuration in `setup.py`.
Modern projects normally use `pyproject.toml`, although some older projects
still contain `setup.py`.

The distribution name used by `pip` and PyPI does not have to be identical to
the package name used by `import`. For example:

```powershell
pip install distribution-name
```

could install a package that is imported as:

```python
import package_name
```

### Poetry and PyPI

[PyPI](https://pypi.org/) is the Python Package Index. It hosts distribution
packages that tools such as `pip` can download and install.

[Poetry](https://python-poetry.org/) is one tool for creating projects,
managing dependencies, building distributions, and publishing them to PyPI.
A minimal workflow is:

```powershell
poetry new mypackage
cd mypackage
poetry build
poetry publish
```

- `poetry new` creates a new project and package structure.
- `poetry build` produces installable distribution files.
- `poetry publish` uploads those files to PyPI after authentication.

Before publishing, `pyproject.toml` should be reviewed to ensure that the
version, description, license, dependencies, and other metadata are correct.
The chosen PyPI distribution name must also be available and should be
specific enough to avoid conflicts with existing projects.

### Key Takeaway

```text
Module               = one .py file
Python package       = a directory of importable Python modules
Distribution package = an installable or publishable project containing code
                       and project metadata
```

In short, modules and Python packages organize code, while distribution
packages make that code installable and shareable.

## Búsqueda de atributos: ICPO

Cuando se accede a un atributo con `objeto.atributo`, Python lo busca siguiendo
el orden **ICPO**:

1. **I — Instance (instancia):** atributos guardados directamente en el objeto.
2. **C — Class (clase):** atributos definidos en la clase del objeto.
3. **P — Parents (clases padre):** atributos heredados de las clases padre.
4. **O — Object:** atributos proporcionados por la clase base `object`.

```python
class Animal:
    tipo = "animal"               # P: clase padre


class Perro(Animal):
    sonido = "guau"               # C: clase


perro = Perro()
perro.nombre = "Toby"             # I: instancia

print(perro.nombre)               # I -> "Toby"
print(perro.sonido)               # C -> "guau"
print(perro.tipo)                 # P -> "animal"
print(perro.__str__())            # O -> método heredado de object
```

La ruta de búsqueda del ejemplo es:

```text
perro -> Perro -> Animal -> object
   I        C        P         O
```

Si el atributo no existe en ninguno de esos lugares, Python produce un
`AttributeError`:

```python
print(perro.edad)
# AttributeError: 'Perro' object has no attribute 'edad'
```

Un atributo de instancia puede ocultar otro con el mismo nombre definido en
la clase:

```python
class Perro:
    sonido = "guau"


perro = Perro()
perro.sonido = "ladrido"

print(perro.sonido)               # "ladrido": atributo de la instancia
print(Perro.sonido)               # "guau": atributo de la clase
```

**ICPO** se aplica a atributos (`objeto.algo`), mientras que **LEGB** se aplica
a nombres de variables escritos directamente (`algo`).

## Referencias y garbage collector

### Conteo de referencias

Python cuenta cuantas referencias apuntan a cada objeto. En CPython, cuando el
contador llega a cero, el objeto normalmente se elimina de inmediato.

```python
a = [1, 2, 3]
b = a                  # El mismo objeto tiene dos referencias

del a                  # Queda la referencia b; el objeto sigue existiendo
del b                  # Quedan cero referencias; se libera el objeto
```

`del` elimina un nombre o atributo, no destruye directamente el objeto:

```python
del objeto.atributo
```

### Garbage collector

El garbage collector complementa el conteo de referencias detectando ciclos
que ya no son accesibles:

```python
class MyClass:
    pass


a = MyClass()
a.obj = a              # Referencia circular
del a                   # El ciclo queda inaccesible
```

Se ejecuta automaticamente cuando se acumulan suficientes objetos rastreados.
Normalmente no hay que gestionarlo manualmente, pero el modulo `gc` permite
controlarlo:

```python
import gc

gc.collect()            # Ejecuta una recoleccion ahora
gc.disable()            # Desactiva la recoleccion automatica
gc.enable()             # La vuelve a activar
```

En resumen: el conteo de referencias gestiona los casos normales; el garbage
collector elimina principalmente ciclos de referencias inaccesibles.
