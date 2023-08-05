import binascii
import datetime
import random
import requests
from multiprocessing.dummy import Pool as ThreadPool
from octopus.platforms.NEO.explorer import NeoExplorerRPC
from octopus.platforms.NEO.disassembler import NeoDisassembler
from octopus.engine.explorer import RequestsConnectionError
from switcheo.switcheo_client import SwitcheoClient
from switcheo.neo.utils import create_offer_hash, neo_get_address_from_scripthash,\
    neo_get_scripthash_from_address, reverse_hex
from switcheo.Fixed8 import SwitcheoFixed8
from blockchain.neo.ingest import NeoIngest


class SwitcheoSmartContract(object):
    def __init__(self,
                 rpc_hostname='localhost',
                 rpc_port='10332',
                 rpc_tls=False,
                 contract_hash='91b83e96f2a7c4fdf0c1688441ec61986c7cae26',
                 mongodb_protocol='mongodb',
                 mongodb_user='switcheo',
                 mongodb_password='switcheo',
                 mongodb_hostname='localhost',
                 mongodb_port='27017',
                 mongodb_db='neo'
    ):
        # self.neo_rpc_client = self.get_neo_node()
        self.neo_rpc_client = NeoExplorerRPC(host=rpc_hostname, port=rpc_port, tls=rpc_tls)
        self.contract_hash = contract_hash
        self.function_params = []
        self.switcheo_transactions = []
        self.switcheo_fees = []
        self.switcheo_freezes = []
        self.deserialize_script = {
            'addToWhitelist': self.deserialize_add_to_whitelist,
            'announceWithdraw': self.deserialize_announce_withdraw,
            'approve': self.deserialize_approve,
            'cancelOffer': self.deserialize_cancel,
            'deposit': self.deserialize_deposit,
            'fillOffer': self.deserialize_fill_offer,
            'freezeTrading': self.deserialize_freeze_trading,
            'initialize': self.deserialize_initialize,
            'makeOffer': self.deserialize_make_offer,
            'mintTokens': self.deserialize_mint_tokens,
            'removeFromWhitelist': self.deserialize_remove_from_whitelist,
            'setTakerFee': self.deserialize_set_taker_fee,
            'transfer': self.deserialize_transfer,
            'unfreezeTrading': self.deserialize_unfreeze_trading,
            'withdraw': self.deserialize_withdraw,
            'withdrawAssets': self.deserialize_withdraw_assets,
            'withdrawal': self.deserialize_withdrawal
        }
        self.neo_smart_contract_function_dict = {
            str(binascii.hexlify(b'deposit').decode('utf-8')): 'deposit',
            str(binascii.hexlify(b'depositFrom').decode('utf-8')): 'depositFrom',
            str(binascii.hexlify(b'onTokenTransfer').decode('utf-8')): 'onTokenTransfer',
            str(binascii.hexlify(b'makeOffer').decode('utf-8')): 'makeOffer',
            str(binascii.hexlify(b'fillOffer').decode('utf-8')): 'fillOffer',
            str(binascii.hexlify(b'cancelOffer').decode('utf-8')): 'cancelOffer',
            str(binascii.hexlify(b'withdraw').decode('utf-8')): 'withdraw',
            str(binascii.hexlify(b'announceCancel').decode('utf-8')): 'announceCancel',
            str(binascii.hexlify(b'announceWithdraw').decode('utf-8')): 'announceWithdraw',
            str(binascii.hexlify(b'transfer').decode('utf-8')): 'transfer',
            str(binascii.hexlify(b'mintTokens').decode('utf-8')): 'mintTokens',
            str(binascii.hexlify(b'addToWhitelist').decode('utf-8')): 'addToWhitelist',
            str(binascii.hexlify(b'initialize').decode('utf-8')): 'initialize',
            str(binascii.hexlify(b'setTakerFee').decode('utf-8')): 'setTakerFee',
            str(binascii.hexlify(b'approve').decode('utf-8')): 'approve',
            str(binascii.hexlify(b'withdrawal').decode('utf-8')): 'withdrawal',
            str(binascii.hexlify(b'withdrawAssets').decode('utf-8')): 'withdrawAssets',
            str(binascii.hexlify(b'freezeTrading').decode('utf-8')): 'freezeTrading',
            str(binascii.hexlify(b'unfreezeTrading').decode('utf-8')): 'unfreezeTrading',
            str(binascii.hexlify(b'removeFromWhitelist').decode('utf-8')): 'removeFromWhitelist'
        }
        self.sc = SwitcheoClient(api_url='https://api.switcheo.network/')
        self.ni = NeoIngest(protocol=mongodb_protocol, username=mongodb_user, password=mongodb_password,
                            hostname=mongodb_hostname, port=mongodb_port, database=mongodb_db)
        self.neo_contract_list = self.get_neo_contract_list()
        self.neo_contract_list.append('78e6d16b914fe15bc16150aeb11d0c2a8e532bdd')
        self.neo_token_dict = self.get_neo_token_dict()
        self.neo_token_dict['78e6d16b914fe15bc16150aeb11d0c2a8e532bdd'] = 'Switcheo Token'
        self.neo_token_dict['ecc6b20d3ccac1ee9ef109af5a7cdb85706b1df9'] = 'RPX'
        self.neo_token_dict['891daf0e1750a1031ebe23030828ad7781d874d6'] = 'IAM'
        self.neo_token_dict['ceab719b8baa2310f232ee0d277c061704541cfb'] = 'ONT'
        self.neo_token_dict['9577c3f972d769220d69d1c4ddbd617c44d067aa'] = 'GALA'
        self.neo_contract_key_list = ['APPCALL', 'TAILCALL']
        self.neo_address_list = [
            'ASH41gtWftHvhuYhZz1jj7ee7z9vp9D9wk',
            'AMAvaXFKtowxB5VpJ928QCSLZD9iMRnhbo'
        ]

    def _get(self, url, params=None):
        """Perform GET request"""
        r = requests.get(url=url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def is_trading_active(self):
        state_dict = {"00": False, "01": True}
        function_name = 'getState'
        # response_script = self.get_neo_node().invokefunction(script_hash=self.contract_hash,
        response_script = self.neo_rpc_client.invokefunction(script_hash=self.contract_hash,
                                                             operation=function_name,
                                                             params=self.function_params)
        return state_dict[reverse_hex(response_script['stack'][0]['value'])]

    def get_neo_contract_list(self):
        contract_list = []
        neo_contracts = self.sc.get_contracts()['NEO']
        for key, value in neo_contracts.items():
            contract_list.append(value)
        return contract_list

    def get_neo_token_dict(self):
        token_dict = {}
        neo_tokens = self.sc.get_token_details()
        for key, value in neo_tokens.items():
            token_dict[value['hash']] = key
        return token_dict

    def get_neo_node(self):
        neo_node_list = []
        neo_node_max_height = 0
        for neo_nodes in self._get(url='https://api.neoscan.io/api/main_net/v1/get_all_nodes'):
            neo_node_dict = {}
            neo_node = neo_nodes['url'].split(':')
            neo_node_height = neo_nodes['height']
            if neo_node_max_height < neo_node_height:
                neo_node_max_height = neo_node_height
            neo_node_protocol = neo_node[0]
            neo_node_url = neo_node[1][2:]
            neo_node_port = neo_node[2]
            if neo_node_protocol == 'https':
                neo_node_rpc_tls = True
            elif neo_node_protocol == 'http':
                neo_node_rpc_tls = False
            else:
                exit(222)
            neo_node_dict['neo_node_url'] = neo_node_url
            neo_node_dict['neo_node_port'] = neo_node_port
            neo_node_dict['neo_node_tls'] = neo_node_rpc_tls
            neo_node_dict['neo_node_height'] = neo_node_height
            neo_node_list.append(neo_node_dict)

        neo_node_max_height_list = []
        for neo_node in neo_node_list:
            if neo_node['neo_node_height'] == neo_node_max_height and 'neo.org' not in neo_node['neo_node_url']:
                neo_node_max_height_list.append(neo_node)

        rand_int = random.randint(0, len(neo_node_max_height_list) - 1)
        print(neo_node_max_height_list[rand_int])
        return NeoExplorerRPC(host=neo_node_max_height_list[rand_int]['neo_node_url'],
                              port=neo_node_max_height_list[rand_int]['neo_node_port'],
                              tls=neo_node_max_height_list[rand_int]['neo_node_tls'])

    def get_neo_block_height(self):
        # return self.get_neo_node().getblockcount() - 1 # I believe this is required b/c the block needs at least 1 confirmation so you can't retrieve the most recent block.
        try:
            return self.neo_rpc_client.getblockcount() - 1  # I believe this is required b/c the block needs at least 1 confirmation so you can't retrieve the most recent block.
        except RequestsConnectionError:
            self.get_neo_block_height()

    def get_neo_latest_block(self):
        # return self.get_neo_node().get_block_by_number(block_number=self.get_neo_block_height())
        return self.neo_rpc_client.get_block_by_number(block_number=self.get_neo_block_height())

    def get_neo_bulk_blocks(self, block_number_list):
        pool = ThreadPool(25)
        try:
            # block_list = pool.map(self.get_neo_node().get_block_by_number, block_number_list)
            block_list = pool.map(self.neo_rpc_client.get_block_by_number, block_number_list)
        except RequestsConnectionError:
            self.get_neo_bulk_blocks(block_number_list=block_number_list)
        pool.close()
        pool.join()
        return block_list

    def chunk_list(self, input_list, chunk_size):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(input_list), chunk_size):
            yield input_list[i:i + chunk_size]

    def zero_pad_if_odd_length_string(self, input_string):
        input_string_length = len(input_string)
        if input_string_length % 2 == 1:
            return input_string.rjust(input_string_length + 1, '0')
        else:
            return input_string

    def deserialize_block(self, block):
        for transaction in block['tx']:
            self.deserialize_transaction(block, transaction)

    def deserialize_transaction(self, block, txn):
        is_pack = False
        is_switcheo = False
        contract_hash = None
        if 'vout' in txn:
            for txn_vout in txn['vout']:
                if txn_vout['address'] in self.neo_address_list:
                    is_switcheo = True
        if 'script' in txn:
            disassemble_dict = {}
            script_disassembler = NeoDisassembler(bytecode=txn['script']).disassemble()
            for s in script_disassembler:
                if str(s).split()[0] == "APPCALL":
                    contract_hash = reverse_hex(str(s).split()[1][2:])
            if contract_hash != '78e6d16b914fe15bc16150aeb11d0c2a8e532bdd':
                for disassemble in script_disassembler:
                    disassemble_list = str(disassemble).split()
                    if is_pack:
                        if 'function' not in disassemble_dict and disassemble_list[0].startswith('PUSHBYTES'):
                            disassemble_dict['function'] = disassemble_list[1][2:]
                        if 'contract' not in disassemble_dict and disassemble_list[0] in self.neo_contract_key_list:
                            disassemble_dict['contract'] = disassemble_list[1][2:]
                            if is_switcheo and disassemble_list[1][2:] in ['3fbc607c12c28736343224a4b4d8f513a5c27ca8', reverse_hex('ab38352559b8b203bde5fddfa0b07d8b2525e132')]:  # Custom Code for transfering MCT tokens.
                                disassemble_dict['function_name'] = self.neo_smart_contract_function_dict[
                                    disassemble_dict['function']]
                            if reverse_hex(disassemble_dict['contract']) in self.neo_contract_list:
                                is_switcheo = True
                                disassemble_dict['function_name'] = self.neo_smart_contract_function_dict[
                                    disassemble_dict['function']]
                    if disassemble_list[0] == 'PACK':
                        is_pack = True
                if is_switcheo:
                    return self.deserialize_script[disassemble_dict['function_name']](block, txn, script_disassembler)

    def deserialize_add_to_whitelist(self, block, txn, script):
        pass

    def deserialize_announce_withdraw(self, block, txn, script):
        pass

    def deserialize_approve(self, block, txn, script):
        pass

    def deserialize_cancel(self, block, txn, script):
        cancel_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'cancel',
            'offer_hash_original': str(script[0]).split()[1][2:],
            'offer_hash': reverse_hex(str(script[0]).split()[1][2:])
        }
        return cancel_dict

    def deserialize_deposit(self, block, txn, script):
        contract_hash = None
        for s in script:
            if str(s).split()[0] == "APPCALL":
                contract_hash = reverse_hex(str(s).split()[1][2:])
        script[1] = self.zero_pad_if_odd_length_string(str(script[1]).split()[1][2:])
        script[2] = self.zero_pad_if_odd_length_string(str(script[2]).split()[1][2:]).rjust(40, '0')
        if len(str(script[0]).split()) == 1 and str(script[0]).split()[0].startswith('PUSH'): # Redeemable Hash Puppies Deposit
            deposit_amount_original = str(script[0]).split()[0]
            deposit_amount = int(deposit_amount_original[4:])
            deposit_amount_fixed8 = SwitcheoFixed8(deposit_amount).ToString()
        elif contract_hash == '0ec5712e0f7c63e4b0fea31029a28cea5e9d551f':
            deposit_amount_original = str(script[0]).split()[1][2:]
            deposit_amount = int(reverse_hex(deposit_amount_original), 16)
            deposit_amount_fixed8 = SwitcheoFixed8(deposit_amount).ToString()
        else:
            deposit_amount_original = self.zero_pad_if_odd_length_string(str(script[0]).split()[1][2:]).rjust(16, '0')
            deposit_amount = int(reverse_hex(deposit_amount_original), 16)
            deposit_amount_fixed8 = SwitcheoFixed8(deposit_amount).ToString()
        deposit_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'deposit',
            'deposit_amount_original': deposit_amount_original,
            'deposit_amount': deposit_amount,
            'deposit_amount_fixed8': deposit_amount_fixed8,
            'deposit_asset_original': script[1],
            'deposit_asset': reverse_hex(script[1]),
            'deposit_asset_name': self.neo_token_dict[reverse_hex(script[1])],
            'deposit_address_original': script[2],
            'deposit_address': neo_get_address_from_scripthash(scripthash=reverse_hex(script[2])),
            'deposits': []
        }
        out_dict = {}
        for transfer in txn['vout']:
            out_dict['deposit_address'] = transfer['address']
            out_dict['deposit_asset'] = transfer['asset']
            out_dict['deposit_asset_name'] = self.neo_token_dict[transfer['asset'][2:]]
            out_dict['deposit_amount'] = transfer['value']
        deposit_dict['deposits'].append(out_dict)
        return deposit_dict

    def deserialize_fill_offer(self, block, txn, script):
        contract_hash = None
        for s in script:
            if str(s).split()[0] == "APPCALL":         # Needed for v1 Contract with 5 variables in block 2087974; tx: C9741EFBDDF1F43D6B8778B3887EE035D44BE49A5EDD093773BEF2FA231DF31E
                contract_hash = reverse_hex(str(s).split()[1][2:])
        if contract_hash in ['0ec5712e0f7c63e4b0fea31029a28cea5e9d551f', '01bafeeafe62e651efc3a530fde170cf2f7b09bd']:
            # if str(script[0]).startswith('PUSH'):
            use_native_token_original = str(script[0])
            use_native_token = True if use_native_token_original[4:] == 1 else False
            if len(str(script[1]).split()) == 1:
                amount_to_fill_original = str(script[1])
                amount_to_fill = int(str(script[1])[4:])
                amount_to_fill_fixed8 = SwitcheoFixed8(amount_to_fill).ToString()
            else:
                amount_to_fill_original = self.zero_pad_if_odd_length_string(str(script[1]).split()[1][2:]).rjust(8, '0')
                amount_to_fill = int(reverse_hex(amount_to_fill_original), 16)
                amount_to_fill_fixed8 = SwitcheoFixed8(amount_to_fill).ToString()
            offer_hash_original = self.zero_pad_if_odd_length_string(str(script[2]).split()[1][2:]).rjust(64, '0')
            offer_hash = reverse_hex(offer_hash_original)
            trading_pair_original = self.zero_pad_if_odd_length_string(str(script[3]).split()[1][2:]).rjust(104, '0')
            trading_pair = reverse_hex(trading_pair_original)
            taker_address_original = self.zero_pad_if_odd_length_string(str(script[4]).split()[1][2:]).rjust(40, '0')
            taker_address = neo_get_address_from_scripthash(scripthash=reverse_hex(taker_address_original))
            fee_amount_original = None
            fee_amount = None
            fee_amount_fixed8 = None
            fee_asset_original = None
            fee_asset = None          # reverse_hex(fee_asset_original)
            fee_asset_name =  None    # self.neo_token_dict[reverse_hex(fee_asset_original)]
            taker_amount_original = None
            taker_amount = None
            taker_amount_fixed8 = None
            fill_offer_dict = {
                'amount_to_fill_original': amount_to_fill_original,
                'amount_to_fill': amount_to_fill,
                'amount_to_fill_fixed8': amount_to_fill_fixed8,
                'block_hash': block['hash'][2:],
                'block_number': block['index'],
                'block_size': block['size'],
                'block_time': block['time'],
                'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
                'transaction_hash': txn['txid'][2:],
                'transaction_type': txn['type'],
                'switcheo_transaction_type': 'fillOffer',
                'fee_amount_original': fee_amount_original,
                'fee_amount': fee_amount,
                'fee_amount_fixed8': fee_amount_fixed8,
                'fee_asset_original': fee_asset_original,
                'fee_asset': fee_asset,
                'fee_asset_name': fee_asset_name,
                'taker_amount_original': taker_amount_original,
                'taker_amount': taker_amount,
                'taker_amount_fixed8': taker_amount_fixed8,
                'trading_pair_original': trading_pair_original,
                'trading_pair': trading_pair,
                'offer_hash_original': offer_hash_original,
                'offer_hash': offer_hash,
                'taker_address_original': taker_address_original,
                'taker_address': taker_address,
                'use_native_token_original': use_native_token_original,
                'use_native_token': use_native_token
            }
        else:
            script[2] = self.zero_pad_if_odd_length_string(str(script[2]).split()[1][2:])
            script[4] = self.zero_pad_if_odd_length_string(str(script[4]).split()[1][2:]).rjust(64, '0')
            script[5] = self.zero_pad_if_odd_length_string(str(script[5]).split()[1][2:]).rjust(40, '0')
            if len(str(script[1]).split()) == 1 and len(str(script[3]).split()) == 1:  # fillOffer with 1 taker and 0 fee: https://neoscan.io/transaction/B12E71381630318405480D69B868477B136B003F4050F6D1370B1B220DEBAF8D
                fee_amount_original = str(script[1]).split()[0]
                fee_amount = int(fee_amount_original[4:])
                fee_amount_fixed8 = SwitcheoFixed8(fee_amount).ToString()
                taker_amount_original = str(script[3]).split()[0]
                taker_amount = int(taker_amount_original[4:])
                taker_amount_fixed8 = SwitcheoFixed8(taker_amount).ToString()
            elif len(str(script[1]).split()) == 1 and len(str(script[3]).split()) == 2: # https://neoscan.io/transaction/2E7C792B63D281F79AE628EEEE80E180D939F98FBC92BE18F44CEF1A9299D6CC
                fee_amount_original = str(script[1]).split()[0]
                fee_amount = int(fee_amount_original[4:])
                fee_amount_fixed8 = SwitcheoFixed8(fee_amount).ToString()
                taker_amount_original = self.zero_pad_if_odd_length_string(str(script[3]).split()[1][2:]).rjust(16, '0')
                taker_amount = int(reverse_hex(taker_amount_original), 16)
                taker_amount_fixed8 = SwitcheoFixed8(taker_amount).ToString()
            else:
                fee_amount_original = self.zero_pad_if_odd_length_string(str(script[1]).split()[1][2:]).rjust(16, '0')
                fee_amount = int(reverse_hex(fee_amount_original), 16)
                fee_amount_fixed8 = SwitcheoFixed8(fee_amount).ToString()
                if len(str(script[3]).split()) == 1:
                    taker_amount_original = str(script[3]).split()[0]
                    taker_amount = int(taker_amount_original[4:])
                    taker_amount_fixed8 = SwitcheoFixed8(taker_amount).ToString()
                else:
                    taker_amount_original = self.zero_pad_if_odd_length_string(str(script[3]).split()[1][2:]).rjust(16, '0')
                    taker_amount = int(reverse_hex(taker_amount_original), 16)
                    taker_amount_fixed8 = SwitcheoFixed8(taker_amount).ToString()
            fill_offer_dict = {
                'block_hash': block['hash'][2:],
                'block_number': block['index'],
                'block_size': block['size'],
                'block_time': block['time'],
                'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
                'transaction_hash': txn['txid'][2:],
                'transaction_type': txn['type'],
                'switcheo_transaction_type': 'fillOffer',
                'fee_amount_original': fee_amount_original,
                'fee_amount': fee_amount,
                'fee_amount_fixed8': fee_amount_fixed8,
                'fee_asset_original': script[2],
                'fee_asset': reverse_hex(script[2]),
                'fee_asset_name': self.neo_token_dict[reverse_hex(script[2])],
                'taker_amount_original': taker_amount_original,
                'taker_amount': taker_amount,
                'taker_amount_fixed8': taker_amount_fixed8,
                'offer_hash_original': script[4],
                'offer_hash': reverse_hex(script[4]),
                'taker_address_original': script[5],
                'taker_address': neo_get_address_from_scripthash(scripthash=reverse_hex(script[5]))
            }
        return fill_offer_dict

    def deserialize_freeze_trading(self, block, txn, script):
        freeze_trading_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'freezeTrading',
            'trade_state_original': str(script[0]),
            'trade_state': 'Inactive' if int(str(script[0])[4:]) == 0 else 'Active'
        }
        return freeze_trading_dict

    def deserialize_initialize(self, block, txn, script):
        pass

    def deserialize_make_offer(self, block, txn, script):
        contract_hash = None
        for s in script:
            if str(s).split()[0] == "APPCALL":  # Needed for v1 Contract with 5 variables in block 2087928; tx: E839E289CC8D435EA49EC5FA66427085A10D3D2508FBC164C0BA2DB53BCB0198
                contract_hash = reverse_hex(str(s).split()[1][2:])
        if contract_hash in ['0ec5712e0f7c63e4b0fea31029a28cea5e9d551f', '01bafeeafe62e651efc3a530fde170cf2f7b09bd']:
            want_amount_original = None
            want_amount = None
            want_amount_fixed8 = None
            want_asset_id_original = None
            want_asset_original = None
            want_asset = None
            want_asset_name = None
            offer_amount_original = None
            offer_amount = None
            offer_amount_fixed8 = None
            offer_asset_id_original = None
            offer_asset_original = None
            offer_asset = None
            offer_asset_name = None
            offer_hash_orignal = None
            maker_address_original = None
            maker_address = None
            switcheo_transaction_id_original = self.zero_pad_if_odd_length_string(str(script[4]).split()[1][2:]).rjust(64, '0')
            switcheo_transaction_id = 'v1.1' if contract_hash == '0ec5712e0f7c63e4b0fea31029a28cea5e9d551f' else 'v1.5'
        else:
            if len(str(script[0]).split()[1][2:]) == 16:
                switcheo_transaction_id_original = str(script[0]).split()[1][2:]
                switcheo_transaction_id = 'v1'
            else:
                switcheo_transaction_id_original = self.zero_pad_if_odd_length_string(str(script[0]).split()[1][2:]).rjust(72, '0') # Unknown nonce from v1.5: https://neoscan.io/transaction/7BC7A3A2BB81AE772821C79A0357F0B905832852CF3150594FA56B63E5402C24
                switcheo_transaction_id = bytes.fromhex(switcheo_transaction_id_original).decode('utf-8')
            want_asset_original = self.zero_pad_if_odd_length_string(str(script[2]).split()[1][2:])
            want_asset = reverse_hex(want_asset_original)
            want_asset_name = self.neo_token_dict[want_asset]
            offer_asset_original = self.zero_pad_if_odd_length_string(str(script[4]).split()[1][2:])
            offer_asset = reverse_hex(offer_asset_original)
            offer_asset_name = self.neo_token_dict[offer_asset]
            maker_address_original = self.zero_pad_if_odd_length_string(str(script[5]).split()[1][2:]).rjust(40, '0')
            maker_address = neo_get_address_from_scripthash(scripthash=reverse_hex(maker_address_original))
            # if script[2] == 'c4cbd934b09e3889e742a357d17b6c6f8e002823' and str(script[1]).split()[0].startswith('PUSH'): # Redeemable Hash Puppies Deposit
            if len(str(script[1]).split()) == 1 and len(str(script[3]).split()) == 1:
                want_amount_original = str(script[1]).split()[0]
                want_amount = int(want_amount_original[4:])
                want_amount_fixed8 = SwitcheoFixed8(want_amount).ToString()
                offer_amount_original = str(script[3]).split()[0]
                offer_amount = int(offer_amount_original[4:])
                offer_amount_fixed8 = SwitcheoFixed8(offer_amount).ToString()
            elif len(str(script[1]).split()) == 1 and len(str(script[3]).split()) == 2:
                want_amount_original = str(script[1]).split()[0]
                want_amount = int(want_amount_original[4:])
                want_amount_fixed8 = SwitcheoFixed8(want_amount).ToString()
                offer_amount_original = self.zero_pad_if_odd_length_string(str(script[3]).split()[1][2:]).rjust(16, '0')
                offer_amount = int(reverse_hex(offer_amount_original), 16)
                offer_amount_fixed8 = SwitcheoFixed8(offer_amount).ToString()
            else:
                want_amount_original = self.zero_pad_if_odd_length_string(str(script[1]).split()[1][2:]).rjust(16, '0')
                want_amount = int(reverse_hex(want_amount_original), 16)
                want_amount_fixed8 = SwitcheoFixed8(want_amount).ToString()
                if len(str(script[3]).split()) == 1:
                    offer_amount_original = str(script[3]).split()[0]
                    offer_amount = int(offer_amount_original[4:])
                    offer_amount_fixed8 = SwitcheoFixed8(offer_amount).ToString()
                else:
                    offer_amount_original = self.zero_pad_if_odd_length_string(str(script[3]).split()[1][2:]).rjust(16, '0')
                    offer_amount = int(reverse_hex(offer_amount_original), 16)
                    offer_amount_fixed8 = SwitcheoFixed8(offer_amount).ToString()

        offer_hash = create_offer_hash(neo_address=maker_address,
                                       offer_asset_amt=offer_amount,
                                       offer_asset_hash=offer_asset,
                                       want_asset_amt=want_amount,
                                       want_asset_hash=want_asset,
                                       txn_uuid=switcheo_transaction_id)
        make_offer_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'makeOffer',
            'switcheo_transaction_id_original': switcheo_transaction_id_original,
            'switcheo_transaction_id': switcheo_transaction_id,
            'want_amount_original': want_amount_original,
            'want_amount': want_amount,
            'want_amount_fixed8': want_amount_fixed8,
            'want_asset_original': want_asset_original,
            'want_asset': want_asset,
            'want_asset_name': want_asset_name,
            'offer_amount_original': offer_amount_original,
            'offer_amount': offer_amount,
            'offer_amount_fixed8': offer_amount_fixed8,
            'offer_asset_original': offer_asset_original,
            'offer_asset': offer_asset,
            'offer_asset_name': offer_asset_name,
            'maker_address_original': maker_address_original,
            'maker_address': maker_address,
            'offer_hash': offer_hash
        }
        return make_offer_dict

    def deserialize_mint_tokens(self, block, txn, script):
        pass

    def deserialize_remove_from_whitelist(self, block, txn, script):
        pass

    def deserialize_set_taker_fee(self, block, txn, script):
        # https://neoscan.io/transaction/3BA488FABCAF208C3FA5A8A06CCD9FF03D27291B1C3B826F6D528547F16A3453
        # https://neoscan.io/transaction/3D8A37A29093535C5692A8334CB3ABB4DD8DEE69646D6DFA67CD1EDB57B7200F
        # taker_fee_amount_original = str(script[0]).split()[1][2:]
        # taker_fee_amount = int(reverse_hex(taker_fee_amount_original), 16)
        # taker_fee_amount_fixed8 = SwitcheoFixed8(taker_fee_amount).ToString()
        # # "takerFee".AsByteArray().Concat(assetID)
        # neo_address_original = str(script[2]).split()[1][2:]
        # neo_address = neo_get_address_from_scripthash(reverse_hex(neo_address_original))
        # set_taker_dict = {
        #     'block_hash': block['hash'][2:],
        #     'block_number': block['index'],
        #     'block_size': block['size'],
        #     'block_time': block['time'],
        #     'transaction_hash': txn['txid'][2:],
        #     'transaction_type': txn['type'],
        #     'switcheo_transaction_type': 'withdrawal',
        #     'taker_fee_amount_original': taker_fee_amount_original,
        #     'taker_fee_amount': taker_fee_amount,
        #     'taker_fee_amount_fixed8': taker_fee_amount_fixed8,
        #     'neo_address_original': neo_address_original,
        #     'neo_address': neo_address
        # }
        # return set_taker_dict
        pass

    def deserialize_transfer(self, block, txn, script):
        contract_hash = None
        for s in script:
            if str(s).split()[0] == "APPCALL":  # Needed for v1 Contract with 5 variables in block 2087928; tx: E839E289CC8D435EA49EC5FA66427085A10D3D2508FBC164C0BA2DB53BCB0198
                contract_hash = reverse_hex(str(s).split()[1][2:])
        if contract_hash == '78e6d16b914fe15bc16150aeb11d0c2a8e532bdd':
            transfer_dict = {
                'block_hash': block['hash'][2:],
                'block_number': block['index'],
                'block_size': block['size'],
                'block_time': block['time'],
                'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
                'transaction_hash': txn['txid'][2:],
                'transaction_type': txn['type'],
                'switcheo_transaction_type': 'transfer',
                'contract_hash': contract_hash
            }
        else:
            if len(str(script[0]).split()) == 1:
                transfer_amount_original = str(script[0]).split()[0]
                transfer_amount = transfer_amount_original[4:]
            else:
                transfer_amount_original = self.zero_pad_if_odd_length_string(str(script[0]).split()[1][2:]).rjust(16, '0')
                transfer_amount = reverse_hex(transfer_amount_original)
            script[1] = self.zero_pad_if_odd_length_string(str(script[1]).split()[1][2:]).rjust(40, '0')
            script[2] = self.zero_pad_if_odd_length_string(str(script[2]).split()[1][2:]).rjust(40, '0')
            transfer_dict = {
                'block_hash': block['hash'][2:],
                'block_number': block['index'],
                'block_size': block['size'],
                'block_time': block['time'],
                'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
                'transaction_hash': txn['txid'][2:],
                'transaction_type': txn['type'],
                'switcheo_transaction_type': 'transfer',
                'transfer_amount_original': transfer_amount_original,
                'transfer_amount': transfer_amount,
                'to_address_original': script[1],
                'to_address': neo_get_address_from_scripthash(scripthash=reverse_hex(script[1])),
                'from_address_original': script[2],
                'from_address': neo_get_address_from_scripthash(scripthash=reverse_hex(script[2]))
            }
        return transfer_dict

    def deserialize_unfreeze_trading(self, block, txn, script):
        unfreeze_trading_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'unfreezeTrading',
            'trade_state_original': str(script[0]),
            'trade_state': 'Active' if int(str(script[0])[4:]) == 1 else 'Inactive'
        }
        return unfreeze_trading_dict

    def deserialize_withdraw(self, block, txn, script):
        withdraw_dict = {
            'block_hash': block['hash'][2:],
            'block_number': block['index'],
            'block_size': block['size'],
            'block_time': block['time'],
            'block_date': datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d'),
            'transaction_hash': txn['txid'][2:],
            'transaction_type': txn['type'],
            'switcheo_transaction_type': 'withdrawal',
            'withdrawals': []
        }
        withdrawal_dict = {}
        for transfer in txn['vout']:
            withdrawal_dict['withdraw_address'] = transfer['address']
            withdrawal_dict['withdraw_asset'] = transfer['asset']
            withdrawal_dict['withdraw_asset_name'] = self.neo_token_dict[transfer['asset'][2:]]
            withdrawal_dict['withdraw_amount'] = transfer['value']
        withdraw_dict['withdrawals'].append(withdrawal_dict)
        return withdraw_dict

    def deserialize_withdraw_assets(self, block, txn, script):
        pass

    def deserialize_withdrawal(self, block, txn, script):
        pass

    def ingest_missing_neo_blocks(self):
        neo_block_start_height = 2000000
        neo_block_height = self.get_neo_block_height()
        switcheo_blocks_ingested = self.ni.get_collection_count(collection='blocks')
        switcheo_blocks_ingested_offset = switcheo_blocks_ingested + neo_block_start_height
        switcheo_blocks_ingested_list = set(range(neo_block_start_height, switcheo_blocks_ingested_offset))
        missing_blocks = self.ni.get_missing_blocks(block_height=neo_block_height,
                                                    block_offset=neo_block_start_height,
                                                    blocks_ingested=switcheo_blocks_ingested,
                                                    blocks_ingested_list=switcheo_blocks_ingested_list)
        for block_number_chunk in self.chunk_list(input_list=missing_blocks, chunk_size=200):
            neo_blocks = self.get_neo_bulk_blocks(block_number_list=block_number_chunk)
            self.ingest_switcheo_transactions(neo_blocks=neo_blocks)

    def ingest_switcheo_transactions(self, neo_blocks):
        for neo_block in neo_blocks:
            for transaction in neo_block['tx']:
                switcheo_transaction = self.deserialize_transaction(neo_block, transaction)
                if switcheo_transaction is not None:
                    self.switcheo_transactions.append(switcheo_transaction)
                    if switcheo_transaction['switcheo_transaction_type'] == 'fillOffer':
                        self.switcheo_fees.append(switcheo_transaction)
                    if switcheo_transaction['switcheo_transaction_type'] in ['freezeTrading', 'unfreezeTrading']:
                        self.switcheo_freezes.append(switcheo_transaction)
                if len(self.switcheo_transactions) % 500 == 0:
                    self.ni.mongo_upsert_many(collection='transactions', upsert_list_dict=self.switcheo_transactions)
                    self.switcheo_transactions.clear()
                    self.ni.mongo_upsert_many(collection='fees', upsert_list_dict=self.switcheo_fees)
                    self.switcheo_fees.clear()
                    self.ni.mongo_upsert_many(collection='freezes', upsert_list_dict=self.switcheo_freezes)
                    self.switcheo_freezes.clear()
        if len(self.switcheo_transactions) % 500 != 0:
            self.ni.mongo_upsert_many(collection='transactions', upsert_list_dict=self.switcheo_transactions)
            self.ni.mongo_upsert_many(collection='fees', upsert_list_dict=self.switcheo_fees)
            self.ni.mongo_upsert_many(collection='freezes', upsert_list_dict=self.switcheo_freezes)
        self.ni.mongo_upsert_many(collection='blocks', upsert_list_dict=neo_blocks)

    def get_contract_balance(self, address, asset):
        function_name = 'getBalance'
        function_params = [{
            "type": "ByteArray",
            "value": reverse_hex(neo_get_scripthash_from_address(address=address))
        }, {
            "type": "ByteArray",
            "value": reverse_hex(self.sc.get_token_details[asset])
        }]
        script_test = self.neo_rpc_client.invokefunction(script_hash=self.contract_hash,
                                                         operation=function_name,
                                                         params=function_params)
        print(script_test)
        print(reverse_hex(script_test['stack'][0]['value']))
        print(int(reverse_hex(script_test['stack'][0]['value']), 16))
        disassembler = NeoDisassembler(bytecode=script_test['script'])
        for disassemble in disassembler.disassemble():
            print(disassemble)
