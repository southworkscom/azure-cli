# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.core.util import CLIError
from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer, StorageAccountPreparer


class AmsAssetFilterTests(ScenarioTest):
    def _get_test_data_file(self, filename):
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', filename)
        self.assertTrue(os.path.isfile(filepath), 'File {} does not exist.'.format(filepath))
        return filepath

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_create')
    def test_ams_asset_filter_create(self, storage_account_for_create):
        amsname = self.create_random_name(prefix='ams', length=12)
        container = self.create_random_name(prefix='cont', length=8)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_create,
            'location': 'westus2',
            'container': container
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}')
        self.cmd('az ams account storage add -a {amsname} -g {rg} -n {storageAccount}')

        assetName = self.create_random_name(prefix='asset', length=12)
        alternateId = self.create_random_name(prefix='aid', length=12)
        description = self.create_random_name(prefix='desc', length=12)

        self.kwargs.update({
            'assetName': assetName,
            'alternateId': alternateId,
            'description': description
        })

        self.cmd('az ams asset create -a {amsname} -n {assetName} -g {rg} --description {description} --alternate-id {alternateId} --storage-account {storageAccount} --container {container}')

        filterName = self.create_random_name(prefix='filter', length=12)

        self.kwargs.update({
            'filterName': filterName,
            'bitrate': 420,
            'endTimestamp': 100000000,
            'liveBackoffDuration': 60,
            'presentationWindowDuration': 1200000000,
            'startTimestamp': 40000000,
            'timescale': 10000000,
            'tracks': '@' + self._get_test_data_file('filterTracks.json'),
        })

        self.cmd('az ams asset-filter create -a {amsname} --asset-name {assetName} -g {rg} -n {filterName} --bitrate {bitrate} --end-timestamp {endTimestamp} --live-backoff-duration {liveBackoffDuration} --presentation-window-duration {presentationWindowDuration} --start-timestamp {startTimestamp} --timescale {timescale} --tracks "{tracks}"', checks=[
            self.check('firstQuality.bitrate', '{bitrate}'),
            self.check('name', '{filterName}'),
            self.check('presentationTimeRange.endTimestamp', '{endTimestamp}'),
            self.check('presentationTimeRange.liveBackoffDuration', '{liveBackoffDuration}'),
            self.check('presentationTimeRange.presentationWindowDuration', '{presentationWindowDuration}'),
            self.check('presentationTimeRange.startTimestamp', '{startTimestamp}'),
            self.check('presentationTimeRange.timescale', '{timescale}'),
            self.check('tracks[0].trackSelections[0].operation', 'Equal'),
            self.check('tracks[0].trackSelections[0].property', 'FourCC'),
            self.check('tracks[0].trackSelections[0].value', 'AVC1'),
            self.check('tracks[1].trackSelections[0].operation', 'NotEqual'),
            self.check('tracks[1].trackSelections[0].property', 'Unknown'),
            self.check('tracks[1].trackSelections[0].value', 'AVC1'),
            self.check('tracks[1].trackSelections[1].operation', 'Equal'),
            self.check('tracks[1].trackSelections[1].property', 'FourCC'),
            self.check('tracks[1].trackSelections[1].value', 'EC-3'),
        ])

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_show')
    def test_ams_asset_filter_show(self, storage_account_for_show):
        amsname = self.create_random_name(prefix='ams', length=12)
        container = self.create_random_name(prefix='cont', length=8)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_show,
            'location': 'westus2',
            'container': container
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}')
        self.cmd('az ams account storage add -a {amsname} -g {rg} -n {storageAccount}')

        assetName = self.create_random_name(prefix='asset', length=12)
        alternateId = self.create_random_name(prefix='aid', length=12)
        description = self.create_random_name(prefix='desc', length=12)

        self.kwargs.update({
            'assetName': assetName,
            'alternateId': alternateId,
            'description': description
        })

        self.cmd('az ams asset create -a {amsname} -n {assetName} -g {rg} --description {description} --alternate-id {alternateId} --storage-account {storageAccount} --container {container}')

        filterName = self.create_random_name(prefix='filter', length=12)

        self.kwargs.update({
            'filterName': filterName,
            'bitrate': 420,
            'endTimestamp': 100000000,
            'liveBackoffDuration': 60,
            'presentationWindowDuration': 1200000000,
            'startTimestamp': 40000000,
            'timescale': 10000000,
            'tracks': '@' + self._get_test_data_file('filterTracks.json'),
        })

        self.cmd('az ams asset-filter create -a {amsname} --asset-name {assetName} -g {rg} -n {filterName} --bitrate {bitrate} --end-timestamp {endTimestamp} --live-backoff-duration {liveBackoffDuration} --presentation-window-duration {presentationWindowDuration} --start-timestamp {startTimestamp} --timescale {timescale} --tracks "{tracks}"')

        self.cmd('az ams asset-filter show -a {amsname} --asset-name {assetName} -g {rg} -n {filterName}', checks=[
            self.check('firstQuality.bitrate', '{bitrate}'),
            self.check('name', '{filterName}'),
            self.check('presentationTimeRange.endTimestamp', '{endTimestamp}'),
            self.check('presentationTimeRange.liveBackoffDuration', '{liveBackoffDuration}'),
            self.check('presentationTimeRange.presentationWindowDuration', '{presentationWindowDuration}'),
            self.check('presentationTimeRange.startTimestamp', '{startTimestamp}'),
            self.check('presentationTimeRange.timescale', '{timescale}'),
            self.check('tracks[0].trackSelections[0].operation', 'Equal'),
            self.check('tracks[0].trackSelections[0].property', 'FourCC'),
            self.check('tracks[0].trackSelections[0].value', 'AVC1'),
            self.check('tracks[1].trackSelections[0].operation', 'NotEqual'),
            self.check('tracks[1].trackSelections[0].property', 'Unknown'),
            self.check('tracks[1].trackSelections[0].value', 'AVC1'),
            self.check('tracks[1].trackSelections[1].operation', 'Equal'),
            self.check('tracks[1].trackSelections[1].property', 'FourCC'),
            self.check('tracks[1].trackSelections[1].value', 'EC-3'),
        ])

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_list_and_delete')
    def test_ams_asset_filter_list_and_delete(self, storage_account_for_list_and_delete):
        amsname = self.create_random_name(prefix='ams', length=12)
        container = self.create_random_name(prefix='cont', length=8)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_list_and_delete,
            'location': 'westus2',
            'container': container
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}')
        self.cmd('az ams account storage add -a {amsname} -g {rg} -n {storageAccount}')

        assetName = self.create_random_name(prefix='asset', length=12)
        alternateId = self.create_random_name(prefix='aid', length=12)
        description = self.create_random_name(prefix='desc', length=12)

        self.kwargs.update({
            'assetName': assetName,
            'alternateId': alternateId,
            'description': description
        })

        self.cmd('az ams asset create -a {amsname} -n {assetName} -g {rg} --description {description} --alternate-id {alternateId} --storage-account {storageAccount} --container {container}')

        filterName1 = self.create_random_name(prefix='filter', length=12)
        filterName2 = self.create_random_name(prefix='filter', length=13)

        self.kwargs.update({
            'filterName1': filterName1,
            'filterName2': filterName2,
            'bitrate1': 420,
            'bitrate2': 1000,
        })

        self.cmd('az ams asset-filter list -a {amsname} --asset-name {assetName} -g {rg}', checks=[
            self.check('length(@)', 0)
        ])

        self.cmd('az ams asset-filter create -a {amsname} --asset-name {assetName} -g {rg} -n {filterName1} --bitrate {bitrate1}')

        self.cmd('az ams asset-filter list -a {amsname} --asset-name {assetName} -g {rg}', checks=[
            self.check('length(@)', 1)
        ])

        self.cmd('az ams asset-filter create -a {amsname} --asset-name {assetName} -g {rg} -n {filterName2} --bitrate {bitrate2}')

        self.cmd('az ams asset-filter list -a {amsname} --asset-name {assetName} -g {rg}', checks=[
            self.check('length(@)', 2)
        ])

        self.cmd('az ams asset-filter delete -a {amsname} --asset-name {assetName} -g {rg} -n {filterName2}')

        self.cmd('az ams asset-filter list -a {amsname} --asset-name {assetName} -g {rg}', checks=[
            self.check('length(@)', 1)
        ])

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_update')
    def test_ams_asset_filter_update(self, storage_account_for_update):
        amsname = self.create_random_name(prefix='ams', length=12)
        container = self.create_random_name(prefix='cont', length=8)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_update,
            'location': 'westus2',
            'container': container
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}')
        self.cmd('az ams account storage add -a {amsname} -g {rg} -n {storageAccount}')

        assetName = self.create_random_name(prefix='asset', length=12)
        alternateId = self.create_random_name(prefix='aid', length=12)
        description = self.create_random_name(prefix='desc', length=12)

        self.kwargs.update({
            'assetName': assetName,
            'alternateId': alternateId,
            'description': description
        })

        self.cmd('az ams asset create -a {amsname} -n {assetName} -g {rg} --description {description} --alternate-id {alternateId} --storage-account {storageAccount} --container {container}')

        filterName = self.create_random_name(prefix='filter', length=12)

        self.kwargs.update({
            'filterName': filterName,
            'bitrate': 420,
            'endTimestamp': 100000000,
            'liveBackoffDuration': 60,
            'presentationWindowDuration': 1200000000,
            'startTimestamp': 40000000,
            'timescale': 10000000,
            'tracks': '@' + self._get_test_data_file('filterTracks.json'),
            'newBitrate': 1000,
            'newStartTimestamp': 40000001,
            'newEndTimestamp': 100000001,
            'newTrackOperation': 'Equal',
            'newTrackProperty': 'FourCC',
            'newTrackValue': 'EC-3'
        })

        self.cmd('az ams asset-filter create -a {amsname} --asset-name {assetName} -g {rg} -n {filterName} --bitrate {bitrate} --end-timestamp {endTimestamp} --live-backoff-duration {liveBackoffDuration} --presentation-window-duration {presentationWindowDuration} --start-timestamp {startTimestamp} --timescale {timescale} --tracks "{tracks}"')

        self.cmd('az ams asset-filter update -a {amsname} --asset-name {assetName} -g {rg} -n {filterName} --bitrate {newBitrate} --start-timestamp {newStartTimestamp} --end-timestamp {newEndTimestamp} --set tracks[1].trackSelections[0].operation={newTrackOperation} tracks[1].trackSelections[0].property={newTrackProperty} tracks[1].trackSelections[0].value={newTrackValue}', checks=[
            self.check('firstQuality.bitrate', '{newBitrate}'),
            self.check('name', '{filterName}'),
            self.check('presentationTimeRange.endTimestamp', '{newEndTimestamp}'),
            self.check('presentationTimeRange.liveBackoffDuration', '{liveBackoffDuration}'),
            self.check('presentationTimeRange.presentationWindowDuration', '{presentationWindowDuration}'),
            self.check('presentationTimeRange.startTimestamp', '{newStartTimestamp}'),
            self.check('presentationTimeRange.timescale', '{timescale}'),
            self.check('tracks[0].trackSelections[0].operation', 'Equal'),
            self.check('tracks[0].trackSelections[0].property', 'FourCC'),
            self.check('tracks[0].trackSelections[0].value', 'AVC1'),
            self.check('tracks[1].trackSelections[0].operation', '{newTrackOperation}'),
            self.check('tracks[1].trackSelections[0].property', '{newTrackProperty}'),
            self.check('tracks[1].trackSelections[0].value', '{newTrackValue}'),
            self.check('tracks[1].trackSelections[1].operation', 'Equal'),
            self.check('tracks[1].trackSelections[1].property', 'FourCC'),
            self.check('tracks[1].trackSelections[1].value', 'EC-3'),
        ])
