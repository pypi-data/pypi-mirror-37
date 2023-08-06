# pygeek-stellar

![pygeek-stellar-logo](resources/pygeek-stellar-logo.png)

**pygeek-stellar** is a CLI Python tool to manage Stellar accounts and interact with the Stellar network. With this tool you can check account balances, check transactions history, send payments and a lot more.. everything using the terminal like a true geek! It requires Python 3.7.


## Installing

You can install from Pypi using: 

```bash
pip3.7 install -U pygeek-stellar
```

## How to use

After installing the **pygeek-stellar** package from Pypi you can simple type the following command on the terminal to start the CLI tool:

```bash
pygeek-stellar
```

## Tests


To run the test suite the Nose package is used. If you want to run the unit tests you can type the following command at the root directory of the project:   

```bash
python3.7 setup.py test
```

or

```bash
nosetests -v
```

## Warning

This tool is still in development mode so it is using the Stellar Testnet by default.

## Security

The used Stellar accounts addresses and correspondent account seeds can be stored in a symmetrically encrypted configuration file. If you do not want to save the account seed on the file, the tool will only ask for it when you want to submit operations that require the private key to the Stellar network.
This tool uses the Fernet module from the python cryptography package (https://cryptography.io/en/latest/#) to encrypt the configuration file.

## How to contribute
Here are some ideas on how you can contribute to this project:

- Clone this repository and submit a pull request that fixes a bug or adds a new feature.
- Create issue tickets for potential improvements.
- Donate Lumens to the following Stellar address: `GBLHVU7EJMSUW72PINTRBRIHT55ZQ7HXFAXELG2JG53X4VAZSHZKLEY6`.

