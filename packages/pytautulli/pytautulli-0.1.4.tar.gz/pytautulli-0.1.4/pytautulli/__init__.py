"""
A python module to get information from Tautulli.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import requests
import urllib3
urllib3.disable_warnings()


def get_users(host, port, api_key, schema='http'):
    """Get the all users."""
    cmd = 'get_users'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    users = []
    try:
        result = requests.get(url, timeout=8, verify=False).json()
        result = result['response']['data']
        for user_data in result:
            users.append(user_data['username'])
    except requests.exceptions.HTTPError:
        users.append('None')
    return users


def verify_user(host, port, api_key, username, schema='http'):
    """Verify that a user exist."""
    cmd = 'get_users'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    try:
        result = requests.get(url, timeout=8, verify=False).json()
        result = result['response']['data']
        for user_data in result:
            if user_data['username'].lower() == username.lower():
                user = True
                break
            else:
                user = False
    except requests.exceptions.HTTPError:
        user = False
    return user


def get_user_state(host, port, api_key, username, schema='http'):
    """Get the state of a user."""
    verify_user(host, port, api_key, username, schema)
    cmd = 'get_activity'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    user_state = 'not available'
    try:
        result = requests.get(url, timeout=8, verify=False).json()
        result = result['response']['data']['sessions']
        for sessions in result:
            if sessions['username'].lower() == username.lower():
                user_state = sessions['state']
                break
    except requests.exceptions.HTTPError:
        user_state = 'not available'
    return user_state


def get_user_activity(host, port, api_key, username, schema='http'):
    """Get the last activity for the spesified user."""
    verify_user(host, port, api_key, username, schema)
    cmd = 'get_activity'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    user_activity = default_activity_attributes()
    try:
        result = requests.get(url, timeout=8, verify=False).json()
        result = result['response']['data']['sessions']
        for sessions in result:
            if sessions['username'].lower() == username.lower():
                for key in sessions:
                    user_activity[key] = sessions[key]
                user_activity = custom_activity(user_activity)
                break
    except requests.exceptions.HTTPError:
        user_activity = 'not available'
    return user_activity


def get_most_stats(host, port, api_key, schema='http'):
    """Get the most * statistics."""
    cmd = 'get_home_stats'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    home_stats = {}
    try:
        request = requests.get(url, timeout=8, verify=False).json()
        result = request['response']['data']
    except IndexError:
        home_stats['Status'] = "not available"
    if result:
        try:
            if result[0]['rows'][0]['title']:
                home_stats['Top Movie'] = result[0]['rows'][0]['title']
        except IndexError:
            home_stats['Top Movie'] = None
        try:
            if result[3]['rows'][0]['title']:
                home_stats['Top TV Show'] = result[3]['rows'][0]['title']
        except IndexError:
            home_stats['Top TV Show'] = None
        try:
            if result[7]['rows'][0]['user']:
                home_stats['Top User'] = result[7]['rows'][0]['user']
        except IndexError:
            home_stats['Top User'] = None
    return home_stats


def get_server_stats(host, port, api_key, schema='http'):
    """Get server statistics."""
    cmd = 'get_activity'
    url = "{}://{}:{}/api/v2?apikey={}&cmd={}".format(schema, host, port,
                                                      api_key, cmd)
    server_stats = {}
    try:
        request = requests.get(url, timeout=8, verify=False).json()
        result = request['response']['data']
        server_stats['count'] = result['stream_count']
        server_stats['total_bandwidth'] = result['total_bandwidth']
        server_stats['count_transcode'] = result['stream_count_transcode']
        server_stats['wan_bandwidth'] = result['wan_bandwidth']
        server_stats['direct_plays'] = result['stream_count_direct_play']
        server_stats['lan_bandwidth'] = result['lan_bandwidth']
        server_stats['direct_streams'] = result['stream_count_direct_stream']
    except requests.exceptions.HTTPError:
        server_stats = {}
    except requests.exceptions.SSLError:
        server_stats = {}
    return server_stats


def custom_activity(alist):
    """Create additional activitie keys."""
    if alist['media_type'] == 'episode':
        senum = ('S{0}'.format(alist['parent_media_index'].zfill(2)) +
                 'E{0}'.format(alist['media_index'].zfill(2)))
        alist['senum'] = senum
        alist['show_senum'] = alist['grandparent_title'] + ' ' + senum
        alist['s_senum_e'] = (alist['grandparent_title'] +
                              ' ' + senum + ' ' + alist['title'])
        alist['magic_title'] = alist['s_senum_e']
    elif alist['media_type'] == 'movie':
        alist['magic_title'] = alist['full_title']
    return alist


def default_activity_attributes():
    """Return default values for the activity_list."""
    output = {}
    alist = ['_cache_time', 'actors', 'added_at', 'allow_guest', 'art',
             'aspect_ratio', 'audience_rating', 'audio_bitrate',
             'audio_bitrate_mode', 'audio_channel_layout', 'audio_channels',
             'audio_codec', 'audio_decision', 'audio_language',
             'audio_language_code', 'audio_profile', 'audio_sample_rate',
             'bandwidth', 'banner', 'bif_thumb', 'bitrate', 'channel_stream',
             'children_count', 'collections', 'container', 'content_rating',
             'deleted_user', 'device', 'directors', 'do_notify', 'duration',
             'email', 'file', 'file_size', 'full_title', 'genres',
             'grandparent_rating_key', 'grandparent_thumb',
             'grandparent_title', 'guid', 'height', 'id', 'indexes',
             'ip_address', 'ip_address_public', 'is_admin', 'is_allow_sync',
             'is_home_user', 'is_restricted', 'keep_history', 'labels',
             'last_viewed_at', 'library_name', 'live', 'live_uuid', 'local',
             'location', 'machine_id', 'media_index', 'media_type',
             'optimized_version', 'optimized_version_profile',
             'optimized_version_title', 'original_title',
             'originally_available_at', 'parent_media_index',
             'parent_rating_key', 'parent_thumb', 'parent_title', 'platform',
             'platform_name', 'platform_version', 'player', 'product',
             'product_version', 'profile', 'progress_percent',
             'quality_profile', 'rating', 'rating_key', 'relay', 's_senum_e',
             'section_id', 'senum', 'session_id', 'session_key',
             'shared_libraries', 'show_senum', 'sort_title', 'state',
             'stream_aspect_ratio', 'stream_audio_bitrate',
             'stream_audio_bitrate_mode', 'stream_audio_channel_layout',
             'stream_audio_channel_layout_', 'stream_audio_channels',
             'stream_audio_codec', 'stream_audio_decision',
             'stream_audio_language', 'stream_audio_language_code',
             'stream_audio_sample_rate', 'stream_bitrate', 'stream_container',
             'stream_container_decision', 'stream_duration',
             'stream_subtitle_codec', 'stream_subtitle_container',
             'stream_subtitle_decision', 'stream_subtitle_forced',
             'stream_subtitle_format', 'stream_subtitle_language',
             'stream_subtitle_language_code', 'stream_subtitle_location',
             'stream_video_bit_depth', 'stream_video_bitrate',
             'stream_video_codec', 'stream_video_codec_level',
             'stream_video_decision', 'stream_video_framerate',
             'stream_video_height', 'stream_video_language',
             'stream_video_language_code', 'stream_video_ref_frames',
             'stream_video_resolution', 'stream_video_width', 'studio',
             'subtitle_codec', 'subtitle_container', 'subtitle_decision',
             'subtitle_forced', 'subtitle_format', 'subtitle_language',
             'subtitle_language_code', 'subtitle_location', 'subtitles',
             'summary', 'synced_version', 'synced_version_profile', 'tagline',
             'throttled', 'thumb', 'title', 'transcode_audio_channels',
             'transcode_audio_codec', 'transcode_container',
             'transcode_decision', 'transcode_height', 'transcode_hw_decode',
             'transcode_hw_decode_title', 'transcode_hw_decoding',
             'transcode_hw_encode', 'transcode_hw_encode_title',
             'transcode_hw_encoding', 'transcode_hw_full_pipeline',
             'transcode_hw_requested', 'transcode_key', 'transcode_progress',
             'transcode_protocol', 'transcode_speed', 'transcode_throttled',
             'transcode_video_codec', 'transcode_width', 'type', 'updated_at',
             'user', 'user_id', 'user_rating', 'user_thumb', 'username',
             'video_bit_depth', 'video_bitrate', 'video_codec',
             'video_codec_level', 'video_decision', 'video_frame_rate',
             'video_framerate', 'video_height', 'video_language',
             'video_language_code', 'video_profile', 'video_ref_frames',
             'video_resolution', 'video_width', 'view_offset', 'width',
             'writers', 'year']
    for key in alist:
        output[key] = ""
    return output
