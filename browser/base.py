# -*- coding: utf-8 -*-


class BaseBrowser(object):
    def __init__(self):
        pass

    def search_music(self, keyword):
        """Search music by keyword.

        Args:
            keyword: The keyword to search music.

        Returns:
            Tuples of (music id, MUSIC INFO).
            MUSIC INFO is a dictionary such as,
            {
                'name': <music name>,
                'artist': <artist name>,
            }
        """
        raise NotImplementedError()

    def get_lyric(self, music_id):
        """Get lyric of the music.

        Args:
            music_id: The id of music, returned by 'search_music' method.

        Returns:
            The lyric as <unicode>.
        """
        raise NotImplementedError()
