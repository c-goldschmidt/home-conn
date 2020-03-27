export enum SpotifyCMD {
    FETCH_STATUS = 'fetch_status',
    NEXT = 'next',
    PREV = 'prev',
    PAUSE = 'pause',
    RESUME = 'resume',
}

export interface SpotifyTypeMap {
    [SpotifyCMD.FETCH_STATUS]: null;
    [SpotifyCMD.NEXT]: null;
    [SpotifyCMD.PREV]: null;
    [SpotifyCMD.PAUSE]: null;
    [SpotifyCMD.RESUME]: null;
}
