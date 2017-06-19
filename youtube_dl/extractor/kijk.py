# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
)


class KijkIE(InfoExtractor):
    IE_NAME = 'embed.kijk.nl'
    _VALID_URL =  r'https?://embed\.kijk\.nl\/video\/(?P<id>\w+)'

    _TESTS = [{
        # video with 5min ID
        'url': 'https://embed.kijk.nl/video/2wBZ882pH5zM',
        'md5': '18ef68f48740e86ae94b98da815eec42',
        'info_dict': {
            'id': '2wBZ882pH5zM',
            'ext': 'mp4',
            'title': 'U.S. Official Warns Of \'Largest Ever\' IRS Phone Scam',
            'description': 'A major phone scam has cost thousands of taxpayers more than $1 million, with less than a month until income tax returns are due to the IRS.',
            'timestamp': 1395405060,
            'upload_date': '20140321',
            'uploader': 'Newsy Studio',
        },
        'params': {
            # m3u8 download
            'skip_download': True,
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        video_data = self._download_json(
            'https://embed.kijk.nl/api/video/%s?id=embedded_3p&format=DASH&drm=CENC&' % video_id,
            video_id)
        formats = []
        roll_url = video_data.get('roll')
        roll = self._download_json(roll_url,"roll")

        for stream in roll.get('streams', []):
            video_url = stream.get('url')
            if not video_url:
                continue
            ext = stream.get('format')

            f = {
                'url': video_url,
                'format_id': stream.get('name'),
            }
            mobj = re.search(r'(\d+)x(\d+)', stream.get('resolution'))
            if mobj:
                f.update({
                    'width': int(mobj.group(1)),
                    'height': int(mobj.group(2)),
                })
            formats.append(f)
        self._sort_formats(formats, ('width', 'height', 'tbr', 'format_id'))
        print('111111111');
        print(video_data.get('metadata').get('title'));
        return {
            'id': video_id,
            'title': video_data.get('metadata').get('title'),
            'duration': int_or_none(video_data.get('duration')),
            'timestamp': int_or_none(video_data.get('publishDate')),
            'view_count': int_or_none(video_data.get('views')),
            'description': video_data.get('description'),
            'uploader': video_data.get('videoOwner'),
            'formats': formats,
        }