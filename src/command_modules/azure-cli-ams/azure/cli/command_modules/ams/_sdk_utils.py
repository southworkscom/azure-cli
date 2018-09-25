# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import importlib

models_module = importlib.import_module('azure.mgmt.media.models')


def get_sdk_model_class(class_name):
    return getattr(models_module, class_name)


def get_stand_alone_presets():
    return ['AudioAnalyzer', 'VideoAnalyzer']


def get_cdn_providers():
    return ['StandardVerizon', 'PremiumVerizon', 'StandardAkamai']


def get_default_streaming_policies():
    return ['Predefined_DownloadOnly', 'Predefined_ClearStreamingOnly', 'Predefined_DownloadAndClearStreaming',
            'Predefined_ClearKey', 'Predefined_SecureStreaming', 'Predefined_SecureStreamingWithFairPlay']


def get_allowed_languages_for_preset():
    return ['en-US', 'en-GB', 'es-ES', 'es-MX', 'fr-FR', 'it-IT', 'ja-JP', 'pt-BR', 'zh-CN']
