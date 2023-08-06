# SwiftAce

You can use this tool to reproduce Anaconda environments with easy.

Installation:

```
pip install swiftace
```

Usage:

1. To capture and upload an anaconda environment, run the following command on the terminal:

```
swiftace save-env
```

The environment details will be uploaded and an ID will be generated. Copy it and keep it safe.

2. To reproduce the environment, run the following command on the terminal (with `ENV_ID` replaced by the environment ID, and `env_name` replaced by the target environment's name)

```
swiftace load-env ENV_ID -n env_name
```
