# Autocomplete SSH hosts for AWS

## Setup autocompletion

To get it working you need to install `bash-completion` and `boto3` python library.

On MacOS X run:

    $ brew install bash-completion

Create symlink to `.bash_autocompletion` file in your home folder:

    $ ln -sf  $(pwd)/.bash_autocompletion ~/

Import `.bash_autocompletion` in your `~/.bashrc`:

    $ echo 'source ~/.bash_autocompletion' >> ~/.bashrc
    $ . ~/.bash.rc

## Installing

The easiest way to install cloud_ssh_config is to use pip:

    $ pip install cloud_ssh_config

or from sources:

    $ git clone https://github.com/DmitriyLyalyuev/cloud_ssh_config.git
    $ cd cloud_ssh_config
    $ python3 setup.py install

## Generating/updating ssh config

Create for ssh `config.d` folder:

    $ mkdir -p ~/.ssh/config.d

To generate or update ssh config for AWS hosts run:

    cloud_ssh_config aws > ~/.ssh/config.d/aws

Use `-h` or `--help` key to get help and options.

## Usage

To test autocompletion enter in terminal:

    $ ssh host_[TAB]


## Supported cloud providers

### AWS

To get it working you need to run:

    $ pip install awscli
    $ aws configure

Enter your credentials to get access to the AWS API.

Or you can use [environment variables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variable-configuration).

### DigitalOcean

Before use it you need register [token](https://cloud.digitalocean.com/account/api/tokens) and run it like:

    $ cloud_ssh_config digitalocean --token place_your_token_here

