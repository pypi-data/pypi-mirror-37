import pytest

from plenum.common.txn_util import get_type, get_payload_data
from plenum.common.util import hexToFriendly

from plenum.common.constants import TARGET_NYM, NODE, CLIENT_STACK_SUFFIX
from plenum.test.pool_transactions.helper import sdk_send_update_node, demote_node

nodeCount = 7
nodes_wth_bls = 0


@pytest.fixture()
def pool_node_txns(poolTxnData):
    node_txns = []
    for txn in poolTxnData["txns"]:
        if get_type(txn) == NODE:
            node_txns.append(txn)
    return node_txns


def test_get_nym_by_name(txnPoolNodeSet, pool_node_txns):
    check_get_nym_by_name(txnPoolNodeSet, pool_node_txns)


def test_get_nym_by_name_not_in_registry(txnPoolNodeSet, pool_node_txns):
    nodes_to_remove = [txnPoolNodeSet[4].name, txnPoolNodeSet[5].name]
    for node in txnPoolNodeSet:
        for node_to_remove in nodes_to_remove:
            del node.nodeReg[node_to_remove]
            del node.cliNodeReg[node_to_remove + CLIENT_STACK_SUFFIX]
    check_get_nym_by_name(txnPoolNodeSet, pool_node_txns)


def test_get_nym_by_name_demoted(txnPoolNodeSet, pool_node_txns,
                                 looper, sdk_wallet_steward, sdk_pool_handle):
    # sdk_wallet_steward fixture is a steward for [0] node,
    # so we can do things below:
    demote_node(looper, sdk_wallet_steward, sdk_pool_handle,
                txnPoolNodeSet[0])
    check_get_nym_by_name(txnPoolNodeSet, pool_node_txns)


def check_get_nym_by_name(txnPoolNodeSet, pool_node_txns):
    for i in range(nodeCount):
        node = txnPoolNodeSet[i]
        pool_manager = node.poolManager
        node_name = node.name

        node_nym = pool_manager.get_nym_by_name(node_name)
        expected_data = get_payload_data(pool_node_txns[i])[TARGET_NYM]

        assert node_nym
        assert node_nym == expected_data
