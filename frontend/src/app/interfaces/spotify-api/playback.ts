import { Device } from './devices';
import { RepeatState, ItemType } from './enums';
import { Track, Album, Artist, Playlist } from './items';
import { Dictionary } from '../misc';

export interface PlaybackActions {
    disallows: Dictionary<boolean>;
    is_playing: boolean;
}


export interface PlaybackState {
    device: Device;
    shuffle_state: boolean;
    repeat_state: RepeatState;
    timestamp: number;
    context: Playlist | Album | Artist;
    progress_ms: number;
    actions: PlaybackActions;
    is_playing: boolean;
    item: Track;
    currently_playing_type: ItemType;
}
