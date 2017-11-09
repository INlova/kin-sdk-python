
from decimal import Decimal
import json
import kin
import pytest
from time import sleep

TEST_ADDRESS = '0x4c6527c2BEB032D46cfe0648072cAb641cA0aA80'
TEST_PRIVATE_KEY = 'd60baaa34ed125af0570a3df7d4ad3e80dd5dc5070680573f8de0ecfc1977275'
TEST_CONTRACT = '0xEF2Fcc998847DB203DEa15fC49d0872C7614910C'
TEST_CONTRACT_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newOwnerCandidate","type":"address"}],"name":"requestOwnershipTransfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"issueTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"newOwnerCandidate","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_by","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"OwnershipRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"OwnershipTransferred","type":"event"}]')   # noqa: E501
TEST_PROVIDER_ENDPOINT =  'http://207.154.247.11:8545'  # 'https://ropsten.infura.io/WszLuPswARhYyyunji2r'


def test_create_fail_empty_endpoint():
    with pytest.raises(kin.SdkConfigurationError, message='either provider or provider endpoint must be provided'):
        kin.TokenSDK(provider_endpoint_uri='')


def test_create_fail_bad_endpoint():
    with pytest.raises(kin.SdkConfigurationError, message='cannot connect to provider endpoint'):
        kin.TokenSDK(provider_endpoint_uri='bad')


def test_create_fail_empty_contract_address():
    with pytest.raises(kin.SdkConfigurationError, message='token contract address not provided'):
        kin.TokenSDK(contract_address='')


def test_create_fail_invalid_contract_address():
    with pytest.raises(kin.SdkConfigurationError, message='invalid token contract address'):
        kin.TokenSDK(contract_address='0xBAD')
    with pytest.raises(kin.SdkConfigurationError, message='invalid token contract address'):
        kin.TokenSDK(contract_address='0x4c6527c2BEB032D46cfe0648072cAb641cA0aA81')  # invalid checksum


def test_create_fail_empty_abi():
    with pytest.raises(kin.SdkConfigurationError, message='token contract abi not provided'):
        kin.TokenSDK(contract_abi='')


def test_create_fail_bad_private_key():
    with pytest.raises(kin.SdkConfigurationError, message='cannot load private key: Unexpected private key format.  '
                                                          'Must be length 32 byte string'):
        kin.TokenSDK(private_key='bad')


def test_sdk_not_configured():
    sdk = kin.TokenSDK()
    with pytest.raises(kin.SdkNotConfiguredError, message='address not configured'):
        sdk.get_address()
    with pytest.raises(kin.SdkNotConfiguredError, message='address not configured'):
        sdk.get_ether_balance()
    with pytest.raises(kin.SdkNotConfiguredError, message='address not configured'):
        sdk.get_token_balance()
    with pytest.raises(kin.SdkNotConfiguredError, message='address not configured'):
        sdk.send_ether('address', 100)
    with pytest.raises(kin.SdkNotConfiguredError, message='address not configured'):
        sdk.send_tokens('address', 100)


def test_create_default():
    sdk = kin.TokenSDK()
    assert sdk
    assert sdk.web3
    assert sdk.token_contract
    assert not sdk.private_key and not sdk.address


def test_create_with_private_key():
    sdk = kin.TokenSDK(provider_endpoint_uri=TEST_PROVIDER_ENDPOINT, private_key=TEST_PRIVATE_KEY)
    assert sdk
    assert sdk.web3
    assert sdk.token_contract
    assert sdk.private_key == TEST_PRIVATE_KEY
    assert sdk.get_address() == TEST_ADDRESS


@pytest.fixture(scope="module")
def test_sdk():
    return kin.TokenSDK(provider_endpoint_uri=TEST_PROVIDER_ENDPOINT, private_key=TEST_PRIVATE_KEY,
                        contract_address=TEST_CONTRACT, contract_abi=TEST_CONTRACT_ABI)


def test_get_address(test_sdk):
    assert test_sdk.get_address() == TEST_ADDRESS


def test_get_ether_balance(test_sdk):
    balance = test_sdk.get_ether_balance()
    assert balance > 0


def test_get_address_ether_balance(test_sdk):
    with pytest.raises(ValueError, message="'0xBAD' is not an address"):
        test_sdk.get_address_ether_balance('0xBAD')
    balance = test_sdk.get_address_ether_balance(TEST_ADDRESS)
    assert balance > 0


def test_get_token_balance(test_sdk):
    balance = test_sdk.get_token_balance()
    assert balance > 100000


def test_get_address_token_balance(test_sdk):
    with pytest.raises(ValueError, message="'0xBAD' is not an address"):
        test_sdk.get_address_token_balance('0xBAD')
    balance = test_sdk.get_address_token_balance(TEST_ADDRESS)
    assert balance > 100000


def test_send_ether_fail(test_sdk):
    with pytest.raises(ValueError, message='amount must be positive'):
        test_sdk.send_ether(TEST_ADDRESS, 0)
    with pytest.raises(ValueError, message='insufficient funds for gas * price + value'):
        test_sdk.send_ether(TEST_ADDRESS, 100)


def test_send_tokens_fail(test_sdk):
    with pytest.raises(ValueError, message='amount must be positive'):
        test_sdk.send_tokens(TEST_ADDRESS, 0)

    # NOTE: sending more tokens than available will not cause immediate exception like with ether,
    # but will result in failed onchain transaction


def test_get_transaction_status(test_sdk):
    # unknown
    tx_status = test_sdk.get_transaction_status('0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef')
    assert tx_status == kin.TransactionStatus.UNKNOWN
    # pending checked in test_send_xxx
    # successful
    # regular transaction, ether transfer
    tx_status = test_sdk.get_transaction_status('0x4c29ae8d617128322750d8cfd6788754f0a18799987531df903675182db5686a')
    assert tx_status == kin.TransactionStatus.SUCCESS
    # contract mediated, token transfer
    tx_status = test_sdk.get_transaction_status('0x7278d5e06ef9d7ee51bc78aa4bee8adf8fd63e28d08b80a26c39f6ab4a267895')
    assert tx_status == kin.TransactionStatus.SUCCESS
    # failed token transfer
    tx_status = test_sdk.get_transaction_status('0xc4736ef55b11cbd01a48477a51cc925eded4e63fc45de66d6b2712a4017822dd')
    assert tx_status == kin.TransactionStatus.FAIL


def test_monitor_ether_transactions(test_sdk):
    tx_statuses = {}

    def my_callback(tx_id, status, from_address, to_address, amount):
        if tx_id not in tx_statuses:  # not mine, skip it
            return
        assert from_address.lower() == TEST_ADDRESS.lower()
        assert to_address.lower() == TEST_ADDRESS.lower()
        assert amount == Decimal('0.001')
        tx_statuses[tx_id] = status

    with pytest.raises(ValueError, message='either from_address or to_address or both must be provided'):
        test_sdk.monitor_ether_transactions(my_callback)

    # start monitoring ether transactions
    test_sdk.monitor_ether_transactions(my_callback, from_address=TEST_ADDRESS)

    # successful ether transfer
    tx_id = test_sdk.send_ether(TEST_ADDRESS, 0.001)
    tx_statuses[tx_id] = kin.TransactionStatus.UNKNOWN

    for wait in range(0, 30):
        if tx_statuses[tx_id] > kin.TransactionStatus.UNKNOWN:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.PENDING

    for wait in range(0, 90):
        if tx_statuses[tx_id] > kin.TransactionStatus.PENDING:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.SUCCESS


def test_monitor_token_transactions(test_sdk):
    tx_statuses = {}

    def my_callback(tx_id, status, from_address, to_address, amount):
        if tx_id not in tx_statuses:  # not mine, skip it
            return
        assert from_address.lower() == TEST_ADDRESS.lower()
        assert to_address.lower() == TEST_ADDRESS.lower()
        assert amount > 0
        tx_statuses[tx_id] = status

    with pytest.raises(ValueError, message='either from_address or to_address or both must be provided'):
        test_sdk.monitor_token_transactions(my_callback)

    # start monitoring token transactions from my address
    test_sdk.monitor_token_transactions(my_callback, from_address=TEST_ADDRESS)

    # transfer more than available, must result in error
    tx_id = test_sdk.send_tokens(TEST_ADDRESS, 10000000)
    tx_statuses[tx_id] = kin.TransactionStatus.UNKNOWN

    for wait in range(0, 30):
        if tx_statuses[tx_id] > kin.TransactionStatus.UNKNOWN:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.PENDING

    for wait in range(0, 90):
        if tx_statuses[tx_id] > kin.TransactionStatus.PENDING:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.FAIL

    # successful token transfer
    tx_id = test_sdk.send_tokens(TEST_ADDRESS, 10)
    tx_statuses[tx_id] = kin.TransactionStatus.UNKNOWN

    for wait in range(0, 30):
        if tx_statuses[tx_id] > kin.TransactionStatus.UNKNOWN:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.PENDING

    for wait in range(0, 90):
        if tx_statuses[tx_id] > kin.TransactionStatus.PENDING:
            break
        sleep(1)
    assert tx_statuses[tx_id] == kin.TransactionStatus.SUCCESS
