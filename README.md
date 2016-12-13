# confidential-debt-simplification

During development run `sudo -H pip3 install -e .` to add **utils** as a package.
Then you can use it on other parts of the project with `import utils` or `from utils import crypto`.

The `-e` flag means editable, it adds the package as a symbolic link to this project folder so that changes are automatically reflected.

The `-H` flag for sudo is recommended by **pip** when using `sudo`, so that **pip** knows the Home folder of the user.