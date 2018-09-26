# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType

from azure.cli.core.commands.validators import get_default_location_from_resource_group
from azure.cli.core.commands.parameters import (get_location_type, get_enum_type, tags_type, get_three_state_flag)
from azure.cli.command_modules.ams._completers import (get_role_definition_name_completion_list,
                                                       get_cdn_provider_completion_list,
                                                       get_default_streaming_policies_completion_list,
                                                       get_presets_definition_name_completion_list,
                                                       get_allowed_languages_for_preset_completion_list,
                                                       get_token_type_completion_list,
                                                       get_fairplay_rentalandlease_completion_list,
                                                       get_token_completion_list)

from azure.mgmt.media.models import (Priority, AssetContainerPermission, LiveEventInputProtocol, LiveEventEncodingType, StreamOptionsFlag, OnErrorType)

from ._validators import validate_storage_account_id, datetime_format, validate_correlation_data, validate_token_claim


def load_arguments(self, _):  # pylint: disable=too-many-locals, too-many-statements
    name_arg_type = CLIArgumentType(options_list=['--name', '-n'], id_part='name', help='The name of the Azure Media Services account.', metavar='NAME')
    account_name_arg_type = CLIArgumentType(options_list=['--account-name', '-a'], id_part='name', help='The name of the Azure Media Services account.', metavar='ACCOUNT_NAME')
    storage_account_arg_type = CLIArgumentType(options_list=['--storage-account'], validator=validate_storage_account_id, metavar='STORAGE_NAME')
    password_arg_type = CLIArgumentType(options_list=['--password', '-p'], metavar='PASSWORD_NAME')
    transform_name_arg_type = CLIArgumentType(options_list=['--transform-name', '-t'], metavar='TRANSFORM_NAME')
    expiry_arg_type = CLIArgumentType(options_list=['--expiry'], type=datetime_format, metavar='EXPIRY_TIME')
    default_policy_name_arg_type = CLIArgumentType(options_list=['--content-key-policy-name'], help='The default content key policy name used by the streaming locator.', metavar='DEFAULT_CONTENT_KEY_POLICY_NAME')
    correlation_data_type = CLIArgumentType(validator=validate_correlation_data, help="Space-separated list of customer provided correlation data that will be returned in Job completed events in key=value format.", nargs='*', metavar='CORRELATION_DATA')
    token_claim_type = CLIArgumentType(validator=validate_token_claim, help='Space-separated list of required token claims in key=value format.', nargs='*', metavar='ASYMMETRIC TOKEN CLAIMS')

    with self.argument_context('ams') as c:
        c.argument('account_name', name_arg_type)

    with self.argument_context('ams account') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx),
                   validator=get_default_location_from_resource_group)
        c.argument('tags', arg_type=tags_type)

    with self.argument_context('ams account create') as c:
        c.argument('storage_account', storage_account_arg_type,
                   help='The name or resource ID of the primary storage account to attach to the Azure Media Services account. Blob only accounts are not allowed as primary.')

    with self.argument_context('ams account check-name') as c:
        c.argument('account_name', options_list=['--name', '-n'], id_part=None,
                   help='The name of the Azure Media Services account')
        c.argument('location', arg_type=get_location_type(self.cli_ctx))

    with self.argument_context('ams account storage') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('storage_account', name_arg_type,
                   help='The name or resource ID of the secondary storage account to detach from the Azure Media Services account.',
                   validator=validate_storage_account_id)

    with self.argument_context('ams account storage sync-storage-keys') as c:
        c.argument('id', required=True)

    with self.argument_context('ams account sp') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('sp_name', name_arg_type,
                   help="The app name or app URI to associate the RBAC with. If not present, a default name like '{amsaccountname}-access-sp' will be generated.")
        c.argument('sp_password', password_arg_type,
                   help="The password used to log in. Also known as 'Client Secret'. If not present, a random secret will be generated.")
        c.argument('role', help='The role of the service principal.', completer=get_role_definition_name_completion_list)
        c.argument('xml', action='store_true', help='Enables xml output format.')
        c.argument('years', help='Number of years for which the secret will be valid. Default: 1 year.', type=int, default=None)

    with self.argument_context('ams transform') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('transform_name', name_arg_type, id_part='child_name_1',
                   help='The name of the transform.')
        c.argument('preset', help='Preset that describes the operations that will be used to modify, transcode, or extract insights from the source file to generate the transform output. Allowed values: {}. In addition to the allowed values, you can also pass a path to a custom Standard Encoder preset JSON file. See https://docs.microsoft.com/rest/api/media/transforms/createorupdate#standardencoderpreset for further details on the settings to use to build a custom preset.'
                   .format(", ".join(get_presets_definition_name_completion_list())))
        c.argument('audio_insights_only', arg_group='Video Analyzer', action='store_true', help='Use this flag to only extract audio insights when processing a video file.')
        c.argument('audio_language', arg_group='Audio/Video Analyzer', help='The language for the audio payload in the input using the BCP-47 format of \"language tag-region\" (e.g: en-US). Allowed values: {}.'
                   .format(", ".join(get_allowed_languages_for_preset_completion_list())))
        c.argument('relative_priority', arg_type=get_enum_type(Priority), help='Sets the relative priority of the transform outputs within a transform. This sets the priority that the service uses for processing TransformOutputs. The default priority is Normal.')
        c.argument('on_error', arg_type=get_enum_type(OnErrorType), help='A Transform can define more than one output. This property defines what the service should do when one output fails - either continue to produce other outputs, or, stop the other outputs. The default is stop.')
        c.argument('description', help='The description of the transform.')

    with self.argument_context('ams transform output remove') as c:
        c.argument('output_index', help='The element index of the output to remove.',
                   type=int, default=None)

    with self.argument_context('ams transform list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams asset') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('asset_name', name_arg_type, id_part='child_name_1',
                   help='The name of the asset.')

    with self.argument_context('ams asset list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams asset create') as c:
        c.argument('alternate_id', help='The alternate id of the asset.')
        c.argument('description', help='The asset description.')
        c.argument('asset_name', name_arg_type, help='The name of the asset.')
        c.argument('storage_account', help='The name of the storage account.')
        c.argument('container', help='The name of the asset blob container.')

    with self.argument_context('ams asset update') as c:
        c.argument('alternate_id', help='The alternate id of the asset.')
        c.argument('description', help='The asset description.')

    with self.argument_context('ams asset get-sas-urls') as c:
        c.argument('permissions', arg_type=get_enum_type(AssetContainerPermission),
                   help='The permissions to set on the SAS URL.')
        c.argument('expiry_time', expiry_arg_type, help="Specifies the UTC datetime (Y-m-d'T'H:M:S'Z') at which the SAS becomes invalid.")

    with self.argument_context('ams job') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('transform_name', transform_name_arg_type, id_part='child_name_1',
                   help='The name of the transform.')
        c.argument('job_name', name_arg_type, id_part='child_name_2',
                   help='The name of the job.')

    with self.argument_context('ams job list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams job start') as c:
        c.argument('priority', arg_type=get_enum_type(Priority),
                   help='The priority with which the job should be processed.')
        c.argument('description', help='The job description.')
        c.argument('input_asset_name',
                   arg_group='Asset Job Input',
                   help='The name of the input asset.')
        c.argument('output_asset_names',
                   nargs='+', help='Space-separated list of output asset names.')
        c.argument('base_uri',
                   arg_group='Http Job Input',
                   help='Base uri for http job input. It will be concatenated with provided file names. If no base uri is given, then the provided file list is assumed to be fully qualified uris.')
        c.argument('files',
                   nargs='+',
                   help='Space-separated list of files. It can be used to tell the service to only use the files specified from the input asset.')
        c.argument('label', help='A label that is assigned to a JobInput, that is used to satisfy a reference used in the Transform.')
        c.argument('correlation_data', arg_type=correlation_data_type)

    with self.argument_context('ams job cancel') as c:
        c.argument('delete', action='store_true', help='Delete the job being cancelled.')

    with self.argument_context('ams content-key-policy') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('content_key_policy_name', name_arg_type,
                   help='The content key policy name.')
        c.argument('description', help='The content key policy description.')
        c.argument('clear_key_configuration',
                   action='store_true',
                   arg_group='Clear Key Configuration (AES Encryption)',
                   help='Use Clear Key configuration, a.k.a AES encryption. It\'s intended for non-DRM keys.')
        c.argument('open_restriction',
                   action='store_true',
                   arg_group='Open Restriction',
                   help='Use open restriction. License or key will be delivered on every request. Not recommended for production environments.')
        c.argument('policy_option_name', help='The content key policy option name.')
        c.argument('policy_option_id', help='The content key policy option identifier. This value can be obtained from "policyOptionId" property by running a show operation on a content key policy resource.')
        c.argument('issuer', arg_group='Token Restriction', help='The token issuer.')
        c.argument('audience', arg_group='Token Restriction', help='The audience for the token.')
        c.argument('token_key', arg_group='Token Restriction', help='Either a string (for symmetric key) or a filepath to a certificate (x509) or public key (rsa). Must be used in conjunction with --token-key-type.')
        c.argument('token_key_type', arg_group='Token Restriction', help='The type of the token key to be used for the primary verification key. Allowed values: {}'.format(", ".join(get_token_completion_list())))
        c.argument('add_alt_token_key', arg_group='Token Restriction', help='Creates an alternate token key with either a string (for symmetric key) or a filepath to a certificate (x509) or public key (rsa). Must be used in conjunction with --add-alt-token-key-type.')
        c.argument('add_alt_token_key_type', arg_group='Token Restriction', help='The type of the token key to be used for the alternate verification key. Allowed values: {}'.format(", ".join(get_token_completion_list())))
        c.argument('alt_symmetric_token_keys', nargs='+', arg_group='Token Restriction', help='Space-separated list of alternate symmetric token keys.')
        c.argument('alt_rsa_token_keys', nargs='+', arg_group='Token Restriction', help='Space-separated list of alternate rsa token keys.')
        c.argument('alt_x509_token_keys', nargs='+', arg_group='Token Restriction', help='Space-separated list of alternate x509 certificate token keys.')
        c.argument('token_claims', arg_group='Token Restriction', arg_type=token_claim_type)
        c.argument('token_type', arg_group='Token Restriction',
                   help='The type of token. Allowed values: {}.'.format(", ".join(get_token_type_completion_list())))
        c.argument('open_id_connect_discovery_document', arg_group='Token Restriction', help='The OpenID connect discovery document.')
        c.argument('widevine_template', arg_group='Widevine Configuration', help='JSON Widevine license template. Use @{file} to load from a file.')
        c.argument('ask', arg_group='FairPlay Configuration', help='The key that must be used as FairPlay ASK.')
        c.argument('fair_play_pfx_password', arg_group='FairPlay Configuration', help='The password encrypting FairPlay certificate in PKCS 12 (pfx) format.')
        c.argument('fair_play_pfx', arg_group='FairPlay Configuration', help='The filepath to a FairPlay certificate file in PKCS 12 (pfx) format (including private key).')
        c.argument('rental_and_lease_key_type', arg_group='FairPlay Configuration', help='The rental and lease key type. Available values: {}.'.format(", ".join(get_fairplay_rentalandlease_completion_list())))
        c.argument('rental_duration', arg_group='FairPlay Configuration', help='The rental duration. Must be greater than or equal to 0.')
        c.argument('play_ready_template', arg_group='PlayReady Configuration', help='JSON PlayReady license template. Use @{file} to load from a file.')

    with self.argument_context('ams content-key-policy show') as c:
        c.argument('with_secrets',
                   action='store_true',
                   help='Include secret values of the content key policy.')

    with self.argument_context('ams streaming-locator') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('default_content_key_policy_name', default_policy_name_arg_type)
        c.argument('streaming_locator_name', name_arg_type, id_part='child_name_1',
                   help='The name of the streaming locator.')
        c.argument('asset_name',
                   help='The name of the asset used by the streaming locator.')
        c.argument('streaming_policy_name',
                   help='The name of the streaming policy used by the streaming locator. You can either create one with `az ams streaming policy create` or use any of the predefined policies: {}'.format(", ".join(get_default_streaming_policies_completion_list())))
        c.argument('start_time', type=datetime_format,
                   help="Start time (Y-m-d'T'H:M:S'Z') of the streaming locator.")
        c.argument('end_time', type=datetime_format,
                   help="End time (Y-m-d'T'H:M:S'Z') of the streaming locator.")
        c.argument('streaming_locator_id', help='The identifier of the streaming locator.')
        c.argument('alternative_media_id', help='An alternative media identifier associated with the streaming locator.')
        c.argument('content_keys', help='JSON string with the content keys to be used by the streaming locator. Use @{file} to load from a file.')

    with self.argument_context('ams streaming-locator list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams streaming-policy') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('streaming_policy_name', name_arg_type, id_part='child_name_1',
                   help='The name of the streaming policy.')
        c.argument('download',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable Download protocol.')
        c.argument('dash',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable Dash protocol.')
        c.argument('hls',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable HLS protocol.')
        c.argument('smooth_streaming',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable SmoothStreaming protocol.')

    with self.argument_context('ams streaming-policy list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams streaming-endpoint') as c:
        c.argument('streaming_endpoint_name', name_arg_type, help='The name of the streaming endpoint.')
        c.argument('account_name', account_name_arg_type)

    with self.argument_context('ams streaming-endpoint create') as c:
        c.argument('tags', arg_type=tags_type)
        c.argument('description', help='The streaming endpoint description.')
        c.argument('scale_units', help='The number of scale units.')
        c.argument('availability_set_name', help='AvailabilitySet name.')
        c.argument('max_cache_age', help='Max cache age.')
        c.argument('custom_host_names', nargs='+', help='Space-separated list of custom host names for the streaming endpoint. Use "" to clear existing list.')
        c.argument('cdn_provider', arg_group='CDN Support', help='The CDN provider name. Allowed values: {}.'.format(", ".join(get_cdn_provider_completion_list())))
        c.argument('cdn_profile', arg_group='CDN Support', help='The CDN profile name.')
        c.argument('client_access_policy', arg_group='Cross Site Access Policies',
                   help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', arg_group='Cross Site Access Policies',
                   help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('auto_start', action='store_true', help='Start the streaming endpoint automatically after creating it.')
        c.argument('ips', nargs='+', arg_group='Access Control Support', help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')

    with self.argument_context('ams streaming-endpoint update') as c:
        c.argument('tags', arg_type=tags_type)
        c.argument('description', help='The streaming endpoint description.')
        c.argument('max_cache_age', help='Max cache age.')
        c.argument('custom_host_names', nargs='+', help='Space-separated list of custom host names for the streaming endpoint. Use "" to clear existing list.')
        c.argument('cdn_provider', arg_group='CDN Support', help='The CDN provider name. Allowed values: {}'.format(", ".join(get_cdn_provider_completion_list())))
        c.argument('cdn_profile', arg_group='CDN Support', help='The CDN profile name.')
        c.argument('client_access_policy', arg_group='Cross Site Access Policies',
                   help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', arg_group='Cross Site Access Policies',
                   help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('ips', nargs='+', arg_group='Access Control Support', help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')
        c.argument('disable_cdn', arg_group='CDN Support', action='store_true', help='Use this flag to disable CDN for the streaming endpoint.')

    with self.argument_context('ams streaming-endpoint scale') as c:
        c.argument('scale_unit', options_list=['--scale-units'], help='The number of scale units.')

    with self.argument_context('ams streaming-endpoint akamai add') as c:
        c.argument('identifier', help='Identifier of the key.')
        c.argument('base64_key', help='Authentication key.')
        c.argument('expiration', help='The exact time for the authentication key to expire.')

    with self.argument_context('ams streaming-endpoint akamai remove') as c:
        c.argument('identifier', help='Identifier of the key.')

    with self.argument_context('ams live-event') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('live_event_name', name_arg_type, help='The name of the live event.')

    with self.argument_context('ams live-event create') as c:
        c.argument('streaming_protocol', arg_type=get_enum_type(LiveEventInputProtocol),
                   arg_group='Input', help='The streaming protocol for the live event.')
        c.argument('auto_start', action='store_true', help='Start the live event automatically after creating it.')
        c.argument('encoding_type', arg_type=get_enum_type(LiveEventEncodingType),
                   arg_group='Encoding', help='The encoding type for live event.')
        c.argument('preset_name', arg_group='Encoding', help='The encoding preset name.')
        c.argument('tags', arg_type=tags_type)
        c.argument('key_frame_interval_duration', arg_group='Input',
                   help='ISO 8601 timespan duration of the key frame interval duration.')
        c.argument('access_token', arg_group='Input', help='The access token.')
        c.argument('description', help='The live event description.')
        c.argument('ips', nargs='+', arg_group='Preview', help='Space-separated list of allowed IP addresses for access control.')
        c.argument('preview_locator', arg_group='Preview', help='The preview locator Guid.')
        c.argument('streaming_policy_name', arg_group='Preview', help='The name of streaming policy used for live event preview.')
        c.argument('alternative_media_id', arg_group='Preview', help='An alternative media identifier associated with the preview URL. This identifier can be used to distinguish the preview of different live events for authorization purposes in the custom license acquisition URL template or the custom key acquisition URL template of the streaming policy specified in the streaming policy name field.')
        c.argument('vanity_url', action='store_true', help='The live event vanity URL flag.')
        c.argument('client_access_policy', arg_group='Cross Site Access Policies', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', arg_group='Cross Site Access Policies', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('stream_options', nargs='+', arg_type=get_enum_type(StreamOptionsFlag), help='The stream options.')

    with self.argument_context('ams live-event update') as c:
        c.argument('description', help='The live event description.')
        c.argument('ips', nargs='+', arg_group='Preview',
                   help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')
        c.argument('tags', arg_type=tags_type)
        c.argument('client_access_policy', arg_group='Cross Site Access Policies', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', arg_group='Cross Site Access Policies', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('key_frame_interval_duration', arg_group='Input', help='ISO 8601 timespan duration of the key frame interval duration.')

    with self.argument_context('ams live-event stop') as c:
        c.argument('remove_outputs_on_stop', action='store_true', help='Remove live outputs on stop.')

    with self.argument_context('ams live-output') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('live_event_name', help='The name of the live event.')
        c.argument('live_output_name', name_arg_type, help='The name of the live output.')

    with self.argument_context('ams live-output create') as c:
        c.argument('asset_name', help='The name of the asset.')
        c.argument('manifest_name', help='The manifest file name.')
        c.argument('archive_window_length', help='ISO 8601 timespan duration of the archive window length. This is the duration that customer want to retain the recorded content.')
        c.argument('description', help='The live output description.')
        c.argument('fragments_per_ts_segment', help='The amount of fragments per HLS segment.')
        c.argument('output_snap_time', help='The output snapshot time.')
