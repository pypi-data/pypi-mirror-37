import pdb
import bitsharesbase.operations as operations
import bitsharesbase.operationids as operationids

cybex_ops = [
    "transfer", # replaced by cybex to support vesting transfer
    "limit_order_create",
    "limit_order_cancel", # replaced by cybex to support rte cancel
    "call_order_update",
    "fill_order",
    "account_create",
    "account_update",
    "account_whitelist",
    "account_upgrade",
    "account_transfer",
    "asset_create",
    "asset_update",
    "asset_update_bitasset",
    "asset_update_feed_producers",
    "asset_issue",
    "asset_reserve",
    "asset_fund_fee_pool",
    "asset_settle",
    "asset_global_settle",
    "asset_publish_feed",
    "witness_create",
    "witness_update",
    "proposal_create",
    "proposal_update",
    "proposal_delete",
    "withdraw_permission_create",
    "withdraw_permission_update",
    "withdraw_permission_claim",
    "withdraw_permission_delete",
    "committee_member_create",
    "committee_member_update",
    "committee_member_update_global_parameters",
    "vesting_balance_create",
    "vesting_balance_withdraw",
    "worker_create",
    "custom",
    "assert",
    "balance_claim",
    "override_transfer",
    "transfer_to_blind",
    "blind_transfer",
    "transfer_from_blind",
    "asset_settle_cancel",
    "asset_claim_fees",
    "fba_distribute",

# cybex added operations ################
    "initiate_crowdfund",
    "participate_crowdfund",
    "withdraw_crowdfund",
    "cancel_vesting",
    "fill_crowdfund",
# end cybex added operations ###########

    "bid_collateral",
    "execute_bid",

# rte operation
    "cancel_all"
]

cybex_operations = {o: cybex_ops.index(o) for o in cybex_ops}

operations.default_prefix = 'CYB'

operationids.ops = cybex_ops

operationids.operations = cybex_operations

from bitsharesbase.objects import Operation

__CYBEX_OPERATIONS = ['Transfer', 'Limit_order_cancel', 'Override_transfer',
                      'Cancel_vesting', 'Balance_claim', 'Asset_issue',
                      'Custom', 'Account_whitelist', 'Cancel_all', 'Proposal_delete' ]

def new_getklass(p1, name):
    if name not in __CYBEX_OPERATIONS:
        module = __import__("bitsharesbase.operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_
    else:
        module = __import__("cybex.cybex_operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_

Operation._getklass = new_getklass
