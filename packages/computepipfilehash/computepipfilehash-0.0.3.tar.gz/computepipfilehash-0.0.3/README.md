# Compute dependency hashes from Pipfile.lock

This is a small tool to compute **sha256** hashes from the Pipfile.lock file.
The `Pipfile.lock` file should exists in the current directory.

## Example usage

```
computepipfilehash
```

If you have locally build wheels in the `./localwheels/` directory, then you
can generate a new requirements file from it.

```
computepipfilehash --wheel-hashes
```

Both the above commands will print the output in the STDOUT.
