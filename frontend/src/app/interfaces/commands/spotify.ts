import { PlayableItem } from '../spotify-api/items';

export enum SpotifyCMD {
    FETCH_STATUS = 'fetch_status',
    NEXT = 'next',
    PREV = 'prev',
    PAUSE = 'pause',
    RESUME = 'resume',
    FETCH_PLAYLISTS = 'fetch_playlists',
    PLAY = 'play',
}

export interface SpotifyTypeMap {
    [SpotifyCMD.FETCH_STATUS]: null;
    [SpotifyCMD.NEXT]: null;
    [SpotifyCMD.PREV]: null;
    [SpotifyCMD.PAUSE]: null;
    [SpotifyCMD.RESUME]: null;
    [SpotifyCMD.FETCH_PLAYLISTS]: null;
    [SpotifyCMD.PLAY]: PlayableItem;
}
