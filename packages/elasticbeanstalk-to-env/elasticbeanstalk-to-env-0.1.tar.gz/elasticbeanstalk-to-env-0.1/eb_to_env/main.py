#!/usr/bin/env python
# -*- coding: future_fstrings -*-
from __future__ import print_function
import click
import boto3
import json
import sys
import os.path

def write_env_file(output, config):
    click.echo(f'updating file "{output}" with new config')
    with open(output, 'w') as f:
        for key in config.keys():
            f.write(f'{key}="{config[key]}"\n')

def load_env_file(input):
    
    d = {}
    with open(input) as f:
        for line in f:
            (key, val) = line.split("=")
            d[key] = val.replace('"', '').strip('\n')
    if len(d) > 0:
        return d
    else:
        return  None
    

def load_eb_config(app, env):
    
    """Pulls environment variables out of an ElasitcBeanstalk application envrionment and outputs a .env file"""
    eb = boto3.client("elasticbeanstalk", region_name="us-east-1")
    try:
        environ = eb.describe_configuration_settings(ApplicationName=app, EnvironmentName=env)
    except:
        click.echo("Invalid Application or Envrionment specified, try again")
        quit()

    if len(environ['ConfigurationSettings']) > 1:
        print('too many environments, exiting...')
        quit()
    eb_config = {}
    for cfg in environ["ConfigurationSettings"][0]["OptionSettings"]:
        if cfg["Namespace"] == "aws:elasticbeanstalk:application:environment":
            #output.write(str.encode(f'''{cfg['OptionName']}="{cfg['Value']}"\n'''))
            eb_config[cfg['OptionName']] = cfg['Value']

    return eb_config


@click.command()
@click.option('--application', required=True, help="ElasticBeanstalk Application Name")
@click.option('--environment', required=True, help="ElasticBeanstalk Environment Name")
@click.option('--output', default="-", type=click.Path(writable=True, allow_dash=True), help="output file to write")
def cli(application, environment, output):

    eb_config = load_eb_config(application, environment)
    if os.path.isfile(output):
        file_config = load_env_file(output)

        replace_file = False
        if type(file_config) is dict:
            eb_keys = eb_config.keys()
            for key in file_config.keys():
                if key in eb_keys:
                    if file_config[key] != eb_config[key]:
                        click.echo(f"{key} does not match, replacing {output}")
                        replace_file = True
                        break
                else:
                    replace_file = True
                    break
        else:
            replace_file = True

        if replace_file:
            write_env_file(output, eb_config)
        else:
            click.echo(f"{output} matches Elastic Beanstalk config")
    else:
        if output == "-":
            click.echo("dumping Elastic Beanstalk config to stdout...")
            click.echo(f"Application = {application}")
            click.echo(f"Environment = {environment}")
            click.echo(json.dumps(eb_config, indent=4))
        else:
            write_env_file(output, eb_config)


if __name__ == '__main__':
    cli()