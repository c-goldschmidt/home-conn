import { PlayableItem, Track } from '../spotify-api/items';

export enum SpotifyCMD {
    FETCH_STATUS = 'fetch_status',
    NEXT = 'next',
    PREV = 'prev',
    PAUSE = 'pause',
    RESUME = 'resume',
    FETCH_PLAYLISTS = 'fetch_playlists',
    PLAY = 'play',
    ADD_TO_PLAYLIST = 'add_to_playlist',
    RESOLVE_URI = 'resolve_uri',
}

export interface SpotifyTypeMap {
    [SpotifyCMD.FETCH_STATUS]: null;
    [SpotifyCMD.NEXT]: null;
    [SpotifyCMD.PREV]: null;
    [SpotifyCMD.PAUSE]: null;
    [SpotifyCMD.RESUME]: null;
    [SpotifyCMD.FETCH_PLAYLISTS]: null;
    [SpotifyCMD.PLAY]: PlayableItem;
    [SpotifyCMD.ADD_TO_PLAYLIST]: Track;
    [SpotifyCMD.RESOLVE_URI]: string;
}
