# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from knack.util import CLIError

def create_streaming_policy(cmd, resource_group_name, account_name,
                            streaming_policy_name, no_encryption_protocols=None,
                            default_content_key_policy_name=None, cenc_protocols=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_clear_tracks=None, cenc_key_to_track_mappings=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None, envelope_protocols=None,
                            envelope_clear_tracks=None, envelope_key_to_track_mappings=None,
                            envelope_custom_key_acquisition_url_template=None,
                            envelope_default_key_label=None, envelope_default_key_policy_name=None):
    from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client
    from azure.cli.command_modules.ams._utils import json2obj
    from azure.mgmt.media.models import (StreamingPolicy, NoEncryption, EnabledProtocols,
                                         CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                         StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                         CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                         StreamingPolicyWidevineConfiguration, EnvelopeEncryption)

    no_encryption_enabled_protocols = _build_enabled_protocols_object(no_encryption_protocols)
    cenc_enabled_protocols = _build_enabled_protocols_object(cenc_protocols)

    # TODO: Remove this after adding support for parsing JSON data
    track_property_condition = TrackPropertyCondition(property='FourCC', operation='Equal', value='testValue')

    cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
        custom_license_acquisition_url_template=cenc_play_ready_url_template,
        play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = StreamingPolicyWidevineConfiguration(
        custom_license_acquisition_url_template=cenc_widevine_url_template)

    # TODO: Remove this after adding support for parsing JSON data
    cenc_key_to_track_mappings = [StreamingPolicyContentKey(label='testLabel',
                                                            policy_name='x512Policy',
                                                            tracks=[TrackSelection(track_selections=[track_property_condition])])]

    envelope_encryption_enabled_protocols = _build_enabled_protocols_object(envelope_protocols)
            


    # TODO: Define envelope_streaming_policy_content_key (StreamingPolicyContentKey list) json: envelope_key_to_track_mappings
    track_selection = None
    envelope_streaming_policy_content_key = None
    if envelope_key_to_track_mappings is not None and os.path.exists(envelope_key_to_track_mappings):
        try:
            with open(envelope_key_to_track_mappings) as json_stream:
                envelope_streaming_policy_content_key = json2obj(json_stream)
        except:
            raise CLIError("Couldn't find a valid JSON definition in '{}'. Check the schema is correct."
                           .format(envelope_key_to_track_mappings))
    envelope_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=envelope_default_key_label,
                                                                              policy_name=envelope_default_key_policy_name),
                                                       key_to_track_mappings=envelope_streaming_policy_content_key)

    envelope_encryption = EnvelopeEncryption(enabled_protocols=envelope_encryption_enabled_protocols,
                                             clear_tracks=track_selection,
                                             content_keys=envelope_content_keys,
                                             custom_key_acquisition_url_template=envelope_custom_key_acquisition_url_template)

    common_encryption_cenc = CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                                  clear_tracks=[TrackSelection(track_selections=[track_property_condition])],
                                                  content_keys=StreamingPolicyContentKeys(
                                                      default_key=DefaultKey(label=cenc_default_key_label,
                                                                             policy_name=cenc_default_key_policy_name),
                                                      key_to_track_mappings=cenc_key_to_track_mappings),
                                                  drm=CencDrmConfiguration(play_ready=cenc_play_ready_config, widevine=cenc_widevine_config))

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=NoEncryption(enabled_protocols=no_encryption_enabled_protocols),
                                       common_encryption_cenc=common_encryption_cenc,
                                       envelope_encryption=envelope_encryption)

    return get_streaming_policies_client(cmd.cli_ctx).create(resource_group_name, account_name,
                                                             streaming_policy_name, streaming_policy)

def _build_enabled_protocols_object(protocols):
    from azure.mgmt.media.models import EnabledProtocols

    enabled_protocols = EnabledProtocols(download=False, dash=False, hls=False, smooth_streaming=False)
    if protocols is not None:
        for protocol in protocols:
            if protocol == 'Download':
                enabled_protocols.download = True
            elif protocol == 'Dash':
                enabled_protocols.dash = True
            elif protocol == 'HLS':
                enabled_protocols.hls = True
            elif protocol == 'SmoothStreaming':
                enabled_protocols.smooth_streaming = True
            else:
                raise CLIError('Unknown protocol {}.'.format(protocol))
    return enabled_protocols
