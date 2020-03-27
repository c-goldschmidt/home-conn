import { Device } from './devices';
import { RepeatState, PlaybackType, ItemType } from './enums';
import { Track, Album, Artist } from './items';
import { Dictionary } from '../misc';

export interface PlaybackActions {
    disallows: Dictionary<boolean>;
    is_playing: boolean;
}

export type PlaybackItem = Track | Album | Artist;

export interface PlaybackStateBase {
    device: Device;
    shuffle_state: boolean;
    repeat_state: RepeatState;
    timestamp: number;
    context: null;  // todo
    progress_ms: number;
    actions: PlaybackActions;
    is_playing: boolean;

    item: PlaybackItem;
    currently_playing_type: ItemType;
}

export interface PlaybackTrack extends PlaybackStateBase {
    item: Track;
    currently_playing_type: ItemType.TRACK;
}


export type PlaybackState = PlaybackTrack;
