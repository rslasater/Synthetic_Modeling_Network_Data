def propagate_laundering(entries):
    """Propagate laundering labels through debit → credit flow.

    Placeholder counterparties like ``"ATM"`` should not cause tainting of other
    transactions. This function iterates until no new accounts become tainted,
    ensuring multi-hop propagation while ignoring non-account counterparties.
    """

    # Collect all actual account IDs present in the data
    account_ids = {e.get("account_id") for e in entries if e.get("account_id")}

    # Seed with any transactions already labelled as laundering
    tainted_accounts = {
        e["account_id"] for e in entries if e.get("is_laundering", False)
    }

    changed = True
    while changed:
        changed = False
        for entry in entries:
            direction = entry.get("direction")
            acct = entry.get("account_id")
            counterparty = entry.get("counterparty")

            if direction == "credit" and counterparty in tainted_accounts:
                if acct not in tainted_accounts:
                    tainted_accounts.add(acct)
                    entry["is_laundering"] = True
                    changed = True
            elif (
                direction == "debit"
                and acct in tainted_accounts
                and counterparty in account_ids
            ):
                if counterparty not in tainted_accounts:
                    tainted_accounts.add(counterparty)
                    entry["is_laundering"] = True
                    changed = True

    return entries
