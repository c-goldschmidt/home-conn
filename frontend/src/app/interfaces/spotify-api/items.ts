import { Dictionary } from './../misc';
import { AlbumType, ItemType, Precision } from './enums';
import { Image } from './resources';

export interface BaseItem {
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    name: string;
    type: ItemType;
    uri: string;
}

export type Artist = BaseItem;

export interface Album extends BaseItem {
    album_type: AlbumType;
    artists: Artist[];
    available_markets: string[];
    images: Image[];
    release_date: string;
    release_date_precision: Precision;
    total_tracks: number;
    type: ItemType.ALBUM;
}

export interface Track extends BaseItem {
    album: Album;
    artists: Artist[];
    available_markets: string[];
    disc_number: number;
    track_number: number;
    duration_ms: number;
    explicit: boolean;
    external_ids: Dictionary<string | number>;
    isrc: string;
    is_local: boolean;
    popularity: number;
    preview_url: string;
    type: ItemType.TRACK;
}

export interface SpotifyUser extends BaseItem {
    display_name: string;
    type: ItemType.USER;
}

export interface PlaylistTrack extends BaseItem {
    added_at: string;
    added_by: SpotifyUser;
    is_local: boolean;
    primary_color: null;
    track: Track;
    video_thumbnail: Dictionary<string>;
}

export interface Playlist extends BaseItem {
    collaborative: boolean;
    description: string;
    images: Image[];
    owner: SpotifyUser;
    primary_color: any;  // todo
    public: boolean;
    type: ItemType.PLAYLIST;
    snapshot_id: string;
    is_main_playlist: boolean;
    tracks: {
        href: string;
        total: number;
        items?: PlaylistTrack[];
    };
}

export type PlayableItem = Playlist | Track | Album | Artist;
