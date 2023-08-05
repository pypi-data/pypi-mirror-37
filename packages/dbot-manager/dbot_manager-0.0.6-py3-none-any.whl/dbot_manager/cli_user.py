"""
This is demo showing how the minimal client could look like.
"""
import os
import re
import json
import click
import requests
import logging
from eth_utils import is_same_address, remove_0x_prefix, decode_hex
from urllib.parse import urljoin

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from microraiden import Atn, Client
from microraiden.config import NETWORK_CFG
from microraiden.utils import privkey_to_addr, verify_balance_proof, create_signed_contract_transaction
from microraiden.make_helpers import make_channel_manager_contract
from utils import load_module, get_private_key, remove_slash_prefix


def _test_call(web3, pk_file, pw_file, dbot_address, requests_data, retry_interval=5):
    atn = Atn(
        private_key=pk_file,
        key_password_path=pw_file,
        web3=web3,
        retry_interval=retry_interval
    )
    dbot_address = web3.toChecksumAddress(dbot_address)
    uri = requests_data['endpoint']['uri']
    method = requests_data['endpoint']['method']
    requests_kwargs = requests_data['kwargs']
    response = atn.test_call(dbot_address=dbot_address, uri=uri, method=method, **requests_kwargs)
    return response


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '--pk-file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    required=True,
    help='Path to private key file or a hex-encoded private key.'
)
@click.option(
    '--pw-file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    required=True,
    help='Path to file containing the password for the private key specified.'
)
@click.option(
    '--http-provider',
    required=True,
    help='Http Provider'
)
@click.option(
    '--dbot-address',
    required=True,
    help='dbot address')
@click.option(
    '--data',
    required=True,
    help='requests test data')
def call(
        pk_file: str,
        pw_file: str,
        http_provider: str,
        dbot_address: str,
        data: str
):
    """
    For API comsumer to Call DBot's API.
    Run in a session which is a HTTP persistent connection.
    In the session, it will find suitable state channel or create channel
    according Dbot service's Response.
    """

    w3 = Web3(HTTPProvider(http_provider))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    requests_test = load_module(os.path.splitext(os.path.basename(data))[0],
                                os.path.dirname(os.path.abspath(data)))
    requests_data = requests_test.data

    response = _test_call(w3, pk_file, pw_file, dbot_address, requests_data)

    if response.status_code == requests.codes.OK:
        click.echo('Got 200 Response. Content-Type: {}'.format(response.headers['Content-Type']))
        if re.match('^json/', response.headers['Content-Type']):
            click.echo(response.headers)
            click.echo(response.json)
        elif response.headers['Content-Type'].startswith('audio') or response.headers['Content-Type'].startswith('image'):
            click.echo(response.headers)
            response_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'response_file')
            with open(response_file, 'wb') as f:
                f.write(response.content)
            click.echo('Save response file at {}'.format(response_file))
        else:
            click.echo(response.headers)
            click.echo(response.text)
    else:
        click.echo('Got {} Response.'.format(response.status_code))
        click.echo(response.text)


@cli.command()
@click.option(
    '--pk_file',
    required=True,
    help='Path to private key file or a hex-encoded private key.'
)
@click.option(
    '--pw_file',
    default=None,
    help='Path to file containing the password for the private key specified.',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.option(
    '--http_provider',
    default='http://0.0.0.0:8545',
    help='Http Provider'
)
@click.option('--dbot_address', required=True, help='dbot address')
@click.option('--channel_manager_address', default='', help='channel manager contract address')
def close(
    pk_file: str,
    pw_file: str,
    http_provider: str,
    dbot_address: str,
    channel_manager_address: str
):
    # TODO 1. get close signature from receiver, 2. send tx to close channels
    # TODO select which channel to close (close the first channel now, we should allow one channel for one
    # dbot later)
    w3 = Web3(HTTPProvider(http_provider))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    dbot_address = Web3.toChecksumAddress(dbot_address)
    dbot_contract = w3.eth.contract(address=dbot_address, abi=abi)
    dbot_domain = Web3.toBytes(dbot_contract.functions.domain().call()).decode('utf-8').rstrip('\0')

    channel_client = Client(
        private_key=pk_file,
        key_password_path=pw_file,
        web3=w3
    )

    channels = channel_client.get_open_channels(dbot_address)

    pending_txs = []

    if not channels:
        click.echo('No channels')
        raise click.Abort()
    for channel in channels:
        click.echo('Close all channels with Dbot: {}'.format(dbot_address))
        # request close signature from dbot server
        #  channel.update_balance(balance)

        # Get last balance signature from server first
        private_key = get_private_key(pk_file, pw_file)
        url = 'http://{}/api/v1/dbots/{}/channels/{}/{}'.format(
            dbot_domain,
            dbot_address,
            privkey_to_addr(private_key),
            channel.block
        )
        r = requests.get(url)
        if r.status_code != 200:
            click.echo("Can not get channel info from server")
            raise click.Abort()

        channel_info = r.json()
        balance_sig = channel_info['last_signature']
        last_balance = channel_info['balance']

        verified = balance_sig and is_same_address(
            verify_balance_proof(
                channel.receiver,
                channel.block,
                last_balance,
                decode_hex(balance_sig),
                channel_client.context.channel_manager.address
            ),
            channel.sender
        )

        if verified:
            if last_balance == channel.balance:
                click.echo(
                    'Server tried to disguise the last unconfirmed payment as a confirmed payment.'
                )
                raise click.Abort()
            else:
                click.echo(
                    'Server provided proof for a different channel balance ({}). Adopting.'.format(
                        last_balance
                    )
                )
                channel.update_balance(last_balance)
        else:
            click.echo(
                'Server did not provide proof for a different channel balance. Reverting to 0.'
            )
            channel.update_balance(0)

        # Get close signature
        r = requests.delete(url, data = {'balance': channel.balance})
        if r.status_code != 200:
            click.echo("Can not get close signature form server.")
            click.echo(r.text)
            raise click.Abort()
        closing_sig = r.json().get('close_signature')
        print('Got close signature: {}'.format(closing_sig))

        channel_manager_address = channel_manager_address or NETWORK_CFG.CHANNEL_MANAGER_ADDRESS
        channel_manager_contract = make_channel_manager_contract(w3, channel_manager_address)
        raw_tx = create_signed_contract_transaction(
            private_key,
            channel_manager_contract,
            'cooperativeClose',
            [
                channel.receiver,
                channel.block,
                channel.balance,
                decode_hex(balance_sig),
                decode_hex(closing_sig)
            ]
        )
        tx_hash = w3.eth.sendRawTransaction(raw_tx)
        click.echo('Sending cooperative close tx (hash: {})'.format(tx_hash.hex()))
        pending_txs.append(tx_hash)

    for tx_hash in pending_txs:
        click.echo("wait for tx to be mined")
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    click.echo("All channels with the dbot are closed")
    print(tx_receipt)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
