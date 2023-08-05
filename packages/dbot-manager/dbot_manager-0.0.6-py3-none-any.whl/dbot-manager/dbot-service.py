#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import click
import requests
from typing import List, Any
from urllib import parse

from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.middleware import geth_poa_middleware
from eth_account.messages import defunct_hash_message
from eth_account import Account
from eth_utils import is_same_address, to_checksum_address

from utils import get_private_key, load_module, SwaggerParser


DBOT_RIGISTER_ADDRESS = '0x0000000000000000000000000000000000000011'
CHANNEL_MANAGER_ADDRESS = '0x0000000000000000000000000000000000000012'
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'contracts/contracts.json')) as fh:
    CONTRACTS_METADATA = json.load(fh)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'microraiden/contracts/contracts.json')) as fh:
    CONTRACTS_METADATA.update(json.load(fh))


def _load_config(config_file=None):
    try:
        if config_file is None:
            config_file = os.path.join(click.get_app_dir('dbot-manager'), 'config.json')
        if not os.path.exists(config_file):
            click.echo('Read config file Error: {}: No such file or directory'.format(config_file))
            click.echo('Please use command "dbot-service config" to generate config file first')
            exit()
        # no such file or directory, please try "help config" to set configuration or use "--config-file" option!
        with open(config_file) as fh:
            config = json.load(fh)
            # TODO use auth api
            resp = requests.get(parse.urljoin(config['dbot_server'], '/api/v1'))
            if resp.status_code != 200:
                raise Exception('DBot server is not available.')
            return config
    except Exception as err:
        click.echo('Connect DBot Server at first.')
        exit()


def make_dbot_register_contract(web3, address=DBOT_RIGISTER_ADDRESS):
    return web3.eth.contract(address=to_checksum_address(address),
                             abi=CONTRACTS_METADATA['DbotFactory']['abi'])

def make_channel_manager_contract(web3, address=CHANNEL_MANAGER_ADDRESS):
    return web3.eth.contract(address=to_checksum_address(address),
                             abi=CONTRACTS_METADATA['TransferChannels']['abi'])

def make_dbot_contract(web3, address=None):
    if address:
        dbotContract = web3.eth.contract(address=to_checksum_address(address),
                                         abi=CONTRACTS_METADATA['Dbot']['abi'],
                                         bytecode=CONTRACTS_METADATA['Dbot']['bytecode'])
    else:
        dbotContract = web3.eth.contract(abi=CONTRACTS_METADATA['Dbot']['abi'],
                                         bytecode=CONTRACTS_METADATA['Dbot']['bytecode'])
    return dbotContract


def _tobytes32(string):
    length = len(string.encode('utf-8'))
    assert(length <= 256)
    return  string.encode('utf-8') + b'\0' * (32 - length)


def _url(domain):
    return domain if domain.lower().startswith('http') else 'https://{}'.format(domain)


def signed_contract_transaction(
    account: Account,
    contract: Contract,
    func_sig: str,
    args: List[Any],
    value: int=0
):
    web3 = contract.web3
    gasPrice = web3.eth.gasPrice
    tx_data = contract.get_function_by_signature(func_sig)(*args).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gasPrice': web3.eth.gasPrice
        })
    return account.signTransaction(tx_data)


@click.group()
def cli():
    pass

@cli.command()
@click.option('--dbot-server',
              required=True,
              help='DBot server address or domain')
@click.option('--pk-file',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              required=True,
              help='keystore or private key file, if private key file is provided')
@click.option('--pw-file',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              required=True,
              help='password file')
@click.option('--http-provider',
              required=True,
              help='HTTP Provider')
@click.option('--config-file',
              required=False,
              help='output config file path')
def config(dbot_server, pk_file, pw_file, http_provider, config_file):
    try:
        resp = requests.get(parse.urljoin(dbot_server, '/api/v1'))
        if resp.status_code != 200:
            raise Exception('The DBot server in config file is not available.')
    except Exception as err:
        click.echo('Connect DBot server Error. Please start DBot Server first.')
        exit()

    default_config = True
    if config_file is None:
        app_dir = click.get_app_dir('dbot-manager')
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        config_file = os.path.join(app_dir, 'config.json')
    else:
        default_config = False
        config_file = os.path.abspath(config_file)
        if not os.path.exists(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w') as fh:
        json.dump({
            'dbot_server': dbot_server,
            'pk_file': os.path.abspath(pk_file),
            'pw_file': os.path.abspath(pw_file),
            'http_provider': http_provider
        }, fh, indent=2)
    click.echo('Config file write to "{}", the DBot server is {}'.format(config_file, dbot_server))
    if not default_config:
        click.echo("Warning: It's not a config file in default path, use it through '--config-file' option in following commands")
    click.echo('Use command "list/status/add/update/remove/publish" to operate DBot services on the Dbot server.')


@cli.command()
@click.option('--config-file', default=None, help='config file')
@click.option('--view', '-v', is_flag=True, default=False, help='view the dbot detail')
def list(config_file, view):
    config = _load_config(config_file)
    click.echo('List all DBot services on the local DBot server')
    ret = requests.get(parse.urljoin(_url(config['dbot_server']), '/api/v1/dbots'))
    dbot_list = ret.json()
    for dbot in dbot_list:
        name = dbot['info']['name']
        address = dbot['info']['addr']
        domain = dbot['info']['domain']
        click.echo('Dbot: {}({}) hosted on {}'.format(name, address, domain))
        if view:
            click.echo(json.dumps(dbot, indent=2))


@cli.command()
@click.option('--config-file', default=None, help='config file')
@click.option('--address', default=None, help='Dbot address')
def status(config_file, address):
    config = _load_config(config_file)
    ret = requests.get(parse.urljoin(config['dbot_server'], '/api/v1/dbots/{}'.format(address)))
    if ret.status_code != 200:
        click.echo('DBot service with address {} is not running on this server.'.format(address))
    else:
        click.echo('DBot service with address {} is running on this server.'.format(address))
        data = ret.json()
        domain = data['info']['domain']
        click.echo('The DBot hosted on domain {}'.format(domain))
    # TODO list all channels connect with this DBot

@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--profile', required=True, help='dbot profile file, which define the dbot domain, middleware and API specification')
@click.option('--address', default=None, help='Dbot address if the Dbot contract has been deployed')
@click.option('--publish', default=False, is_flag=True, help='if publish to public dbot register list')
def add(config_file, profile, address, publish):
    """
    Add a Dbot. It's API specification are defined by a swagger file, the API price also included
    1. Make sure the DBot Server on the domain is available
    2. Get DBot info (name, domain, api price list) which should be on chain;
    3. Deploy DBot contract on chain, get the dbot contract address;
    4. POST dbot data with dbot owner's signature in request header
    """
    config = _load_config(config_file)

    try:
        profile_path = os.path.dirname(os.path.abspath(profile))
        with open(profile, 'r') as fh:
            dbot_profile = json.load(fh)

        # TODO valid check for profile and specification
        specification = os.path.join(profile_path, dbot_profile['specification']['file'])
        spec_parser = SwaggerParser(specification)
        files = [
            ('profile', (profile, open(profile, 'r'))),
            ('specification', (specification, open(specification, 'r')))
        ]
        mw = dbot_profile.get('middleware')
        if mw is not None:
            middleware = os.path.join(profile_path, '{}.py'.format(mw['module']))
            files.append(('middleware', (middleware, open(middleware, 'r'))))
    except Exception as err:
        click.echo(err)
        raise click.Abort()

    dbot_server = config['dbot_server']
    web3 = Web3(HTTPProvider(config['http_provider']))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    private_key = get_private_key(config['pk_file'], config['pw_file'])
    if private_key is None:
        raise click.Abort(1)
    acct = web3.eth.account.privateKeyToAccount(private_key)

    domain = dbot_server
    if address is None:
        click.echo('Deploy a Dbot contract and start the service')

        # deploy the dbot contract and get the address
        Dbot = make_dbot_contract(web3)
        name = dbot_profile['info']['name']
        endpoints = dbot_profile['endpoints']
        dbot_deployed = False

        # deploy a dbot contract with first endpoint
        for ep in endpoints:
            uri = ep['uri']
            method = ep['method']
            price = ep['price']
            if not dbot_deployed:
                tx_data = Dbot.constructor(_tobytes32(name),
                                           _tobytes32(domain),
                                           _tobytes32(method),
                                           price,
                                           _tobytes32(uri)).buildTransaction({
                                               'from': acct.address,
                                               'nonce': web3.eth.getTransactionCount(acct.address),
                                               'gasPrice': web3.eth.gasPrice
                                           })
                signed_tx = acct.signTransaction(tx_data)
                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                click.echo('Waiting for the transaction (tx_hash = {}) to be mined.'.format(tx_hash.hex()))
                tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                address = tx_receipt.contractAddress.lower()
                click.echo('DBot contract address is {}'.format(address))
                dbot_deployed = True
            else:
                click.echo('Add endpoint {} in dbot({})'.format((uri, method), address))
                signed_tx = signed_contract_transaction(acct, Dbot, 'addEndPoint(bytes32,uint256,bytes32)',
                                                        [_tobytes32(method), price, _tobytes32(uri)])
                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                click.echo('Waiting for the transaction (tx_hash = {}) to be mined.'.format(tx_hash.hex()))
                tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        click.echo('Start Dbot service')
    else:
        click.echo('Start the Dbot service with a deployed dbot contract at {}'.format(address))
        address = address.lower()

    data = {
        'address': address,
        'owner': acct.address,
        'floor_price': min([ep['price'] for ep in dbot_profile['endpoints']]),
        'api_host': spec_parser.api_host,
        'protocol': spec_parser.protocol,
        'domain': domain,
    }
    click.echo('post dbot_data to dbot server to create a dbot service')
    url = parse.urljoin(_url(domain), '/api/v1/dbots')
    res = requests.post(url, data=data, files=files)
    if res.status_code != 200:
        click.echo('Add DBot failed.')
        click.echo(res.text)
    else:
        click.echo('Add DBot success.')

    if publish:
        click.echo('Publish the DBot to public register list')
        DbotFactory = make_dbot_register_contract(web3)
        tx_data = DbotFactory.functions.register(
            to_checksum_address(address)).buildTransaction({
                'nonce': web3.eth.getTransactionCount(acct.address),
                'gasPrice': web3.eth.gasPrice
            })
        signed_tx = acct.signTransaction(tx_data)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        click.echo('Waiting for the transaction (tx_hash = {}) to be mined.'.format(tx_hash.hex()))
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        click.echo('Publish success')


@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--profile', required=True, help='dbot profile file, which define the dbot domain, middleware and API specification')
@click.option('--address', required=True, help='Dbot address if the Dbot contract has been deployed')
def update(config_file, profile, address):
    config = _load_config(config_file)
    try:
        profile_path = os.path.dirname(os.path.abspath(profile))
        with open(profile, 'r') as fh:
            dbot_profile = json.load(fh)

        # TODO valid check for profile and specification
        specification = os.path.join(profile_path, dbot_profile['specification']['file'])
        spec_parser = SwaggerParser(specification)
        files = [
            ('profile', (profile, open(profile, 'r'))),
            ('specification', (specification, open(specification, 'r')))
        ]
        mw = dbot_profile.get('middleware')
        if mw is not None:
            middleware = os.path.join(profile_path, '{}.py'.format(mw['module']))
            files.append(('middleware', (middleware, open(middleware, 'r'))))
    except Exception as err:
        click.echo(err)
        raise click.Abort()


    dbot_server = config['dbot_server']
    web3 = Web3(HTTPProvider(config['http_provider']))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    private_key = get_private_key(config['pk_file'], config['pw_file'])
    if private_key is None:
        raise click.Abort(1)
    acct = web3.eth.account.privateKeyToAccount(private_key)

    # deploy the dbot contract and get the address
    Dbot = make_dbot_contract(web3, address)
    name = dbot_profile['info']['name']
    old_name = Dbot.functions.name().call()
    if (_tobytes32(name) != old_name):
        click.echo('Change DBot name from "{}" to "{}" on chain.'.format(old_name.decode('utf-8'), name))
        signed_tx = signed_contract_transaction(acct, Dbot, 'changeName(bytes32)', [_tobytes32(name)])
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    domain = dbot_server
    old_domain = Dbot.functions.domain().call()
    if (_tobytes32(domain) != old_domain):
        click.echo('Change DBot domain from "{}" to "{}" on chain.'.format(old_domain.decode('utf-8'), domain))
        signed_tx = signed_contract_transaction(acct, Dbot, 'changeDomain(bytes32)', [_tobytes32(domain)])
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    endpoints = dbot_profile['endpoints']
    # deploy a dbot contract with first endpoint
    for ep in endpoints:
        uri = ep['uri']
        method = ep['method']
        # TODO price valid check
        price = ep['price']
        key = Dbot.functions.getKey(_tobytes32(method), _tobytes32(uri)).call()
        ep_onchain = Dbot.functions.keyToEndPoints(key).call()
        if all(b == '\0' for b in ep_onchain[0].decode('utf-8')):
            click.echo('Add endpoints(method: {}, uri: {}, price: {}) on chain.'.format(method, uri, price))
            signed_tx = signed_contract_transaction(acct, Dbot, 'addEndPoint(bytes32,uint256,bytes32)',
                                                    [_tobytes32(method), price, _tobytes32(uri)])
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        elif price != ep_onchain[1]:
            click.echo('Change price of endpoints(method: {}, uri: {}) from {} to {} on chain'.format(method, uri, ep_onchain[1], price))
            signed_tx = signed_contract_transaction(acct, Dbot, 'updateEndPoint(bytes32,uint256,bytes32)',
                                                    [_tobytes32(method), price, _tobytes32(uri)])
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(web3.toHex(tx_hash))
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    address = address.lower()
    data = {
        'address': address,
        'owner': acct.address,
        'domain': domain,
        'floor_price': min([ep['price'] for ep in dbot_profile['endpoints']]),
        'api_host': spec_parser.api_host,
        'protocol': spec_parser.protocol
    }

    click.echo('Put dbot data to dbot server to update the dbot service')
    url = parse.urljoin(_url(domain), '/api/v1/dbots/{}'.format(address))
    res = requests.put(url, data=data, files=files)
    if res.status_code != 200:
        click.echo('Update DBot failed.')
        click.echo(res.text)
    else:
        click.echo('Update DBot success.')

@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--address', help='Address of Dbot contract')
def remove(config_file, address):
    config = _load_config(config_file)

    click.echo('Remove the DBot ...')
    dbot_server = config['dbot_server']
    web3 = Web3(HTTPProvider(config['http_provider']))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    private_key = get_private_key(config['pk_file'], config['pw_file'])
    if private_key is None:
        raise click.Abort(1)
    acct = web3.eth.account.privateKeyToAccount(private_key)

    url = parse.urljoin(_url(dbot_server), '/api/v1/dbots/{}'.format(address))
    res = requests.delete(url)
    if res.status_code != 200:
        click.echo('Remove Dbot service failed.')
        click.echo(res.text)
    else:
        click.echo('Remove Dbot service success.')


@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--address', required=True, help='Dbot address if the Dbot contract has been deployed')
def publish(config_file, address):
    config = _load_config(config_file)

    click.echo('Publish the DBot to public register list')
    dbot_server = config['dbot_server']
    web3 = Web3(HTTPProvider(config['http_provider']))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    private_key = get_private_key(config['pk_file'], config['pw_file'])
    if private_key is None:
        raise click.Abort(1)
    acct = web3.eth.account.privateKeyToAccount(private_key)

    DbotFactory = make_dbot_register_contract(web3)
    tx_data = DbotFactory.functions.register(
        to_checksum_address(address)).buildTransaction({
            'nonce': web3.eth.getTransactionCount(acct.address),
            'gasPrice': web3.eth.gasPrice
        })
    signed_tx = acct.signTransaction(tx_data)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    click.echo('Waiting for the transaction (tx_hash = {}) to be mined.'.format(tx_hash.hex()))
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    click.echo('Publish success')


@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--address', required=True, help='Dbot address')
@click.option('--sender', default=None, help='Dbot address')
def withdraw_from_channel(config_file, address, sender):
    config = _load_config(config_file)
    click.echo('WithDraw balance from channels to DBot, the ATN balance in DBot can only be withdraw by its owner')
    click.echo('TODO')


@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--address', required=True, help='Dbot address')
def withdraw(config_file, address):
    config = _load_config(config_file)
    click.echo('WithDraw all balance from DBot')
    click.echo('TODO')


@cli.command()
@click.option('--config-file', default=None, help='specify config file')
@click.option('--address', required=True, help='Dbot address')
@click.option('--sender', default=None, help='Dbot address')
def close_channel(config_file, address, sender):
    click.echo('Close channel')
    click.echo('TODO')

if __name__ == '__main__':
    cli()
