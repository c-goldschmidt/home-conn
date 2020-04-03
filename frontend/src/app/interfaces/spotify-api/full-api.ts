import { Dictionary } from '../misc';
import { Image, Paginated } from './resources';

// parsed from docs...

export interface Album {
    album_type: string;
    artists: Artist[];
    available_markets: string[];
    copyrights: any[];
    external_ids: ExternalId;
    external_urls: Dictionary<string>;
    genres: string[];
    href: string;
    id: string;
    images: Image[];
    label: string;
    name: string;
    popularity: number;
    release_date: string;
    release_date_precision: string;
    tracks: SimplifiedTrack[];
    type: string;
    uri: string;
}

export interface Artist {
    external_urls: Dictionary<string>;
    followers: any;
    genres: string[];
    href: string;
    id: string;
    images: Image[];
    name: string;
    popularity: number;
    type: string;
    uri: string;
}

export interface AudioFeatures {
    acousticness: number;
    analysis_url: string;
    danceability: number;
    duration_ms: number;
    energy: number;
    id: string;
    instrumentalness: number;
    key: number;
    liveness: number;
    loudness: number;
    mode: number;
    speechiness: number;
    tempo: number;
    time_signature: number;
    track_href: string;
    type: string;
    uri: string;
    valence: number;
}

export interface Category {
    href: string;
    icons: Image[];
    id: string;
    name: string;
}

export interface Context {
    external_urls: Dictionary<string>;
    href: string;
    type: string;
    uri: string;
}

export interface CurrentlyPlaying {
    context: Context;
    currently_playing_type: string;
    is_playing: boolean;
    item: Track | Episode;
    progress_ms: number;
    timestamp: number;
}

export interface Cursor {
    after: string;
}

export interface CursorPaging {
    cursors: Cursor;
    href: string;
    items: Dictionary<any>[];
    limit: number;
    next: string;
    total: number;
}

export interface Device {
    id: string;
    is_active: boolean;
    is_private_session: boolean;
    is_restricted: boolean;
    name: string;
    type: string;
    volume_percent: number;
}

export interface Devices {
    devices: Device[];
}

export interface Episode {
    audio_preview_url: string;
    description: string;
    duration_ms: number;
    explicit: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    is_externally_hosted: boolean;
    is_playable: boolean;
    language: string;
    languages: string[];
    name: string;
    release_date: string;
    release_date_precision: string;
    resume_point: ResumePoint;
    show: SimplifiedShow;
    type: string;
    uri: string;
}

export interface ExternalId {
    ean: string;
    isrc: string;
    upc: string;
}

export interface Paging {
    href: string;
    items: Dictionary<any>[];
    limit: number;
    next: string;
    offset: number;
    previous: string;
    total: number;
}

export interface PlayHistory {
    context: Context;
    played_at: string;
    track: SimplifiedTrack;
}

export interface Playlist {
    collaborative: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    name: string;
    owner: PublicUser;
    public: boolean;
    snapshot_id: string;
    tracks: Paginated<PlaylistTrack>;
    type: string;
    uri: string;

    // custom property
    is_main_playlist: boolean;
}

export interface PlaylistTrack {
    added_at: string;
    added_by: PublicUser;
    is_local: boolean;
    track: Track | Episode;
}

export interface PrivateUser {
    country: string;
    display_name: string;
    email: string;
    external_urls: Dictionary<string>;
    followers: any;
    href: string;
    id: string;
    images: Image[];
    product: string;
    type: string;
    uri: string;
}

export interface PublicUser {
    display_name: string;
    external_urls: Dictionary<string>;
    followers: any;
    href: string;
    id: string;
    images: Image[];
    type: string;
    uri: string;
}

export interface RecommendationSeed {
    afterFilteringSize: number;
    afterRelinkingSize: number;
    href: string;
    id: string;
    initialPoolSize: number;
    type: string;
}

export interface RecommendationsResponse {
    seeds: RecommendationSeed[];
    tracks: SimplifiedTrack[];
}

export interface ResumePoint {
    fully_played: boolean;
    resume_position_ms: number;
}

export interface SavedAlbum {
    added_at: string;
    album: Album;
}

export interface SavedShow {
    added_at: string;
    show: SimplifiedShow;
}

export interface SavedTrack {
    added_at: string;
    track: Track;
}

export interface Show {
    available_markets: string[];
    copyrights: any[];
    description: string;
    episodes: SimplifiedEpisode[];
    explicit: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    is_externally_hosted: boolean;
    languages: string[];
    media_type: string;
    name: string;
    publisher: string;
    type: string;
    uri: string;
}

export interface SimplifiedAlbum {
    album_group: string;
    album_type: string;
    artists: Partial<Artist>[];
    available_markets: string[];
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    name: string;
    type: string;
    uri: string;
}

export interface SimplifiedEpisode {
    audio_preview_url: string;
    description: string;
    duration_ms: number;
    explicit: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    is_externally_hosted: boolean;
    is_playable: boolean;
    language: string;
    languages: string[];
    name: string;
    release_date: string;
    release_date_precision: string;
    resume_point: ResumePoint;
    type: string;
    uri: string;
}

export interface SimplifiedShow {
    available_markets: string[];
    copyrights: any[];
    description: string;
    explicit: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    images: Image[];
    is_externally_hosted: boolean;
    languages: string[];
    media_type: string;
    name: string;
    publisher: string;
    type: string;
    uri: string;
}

export interface SimplifiedTrack {
    artists: Partial<Artist>[];
    available_markets: string[];
    disc_number: number;
    duration_ms: number;
    explicit: boolean;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    is_playable: boolean;
    linked_from: any;
    name: string;
    preview_url: string;
    track_number: number;
    type: string;
    uri: string;
}

export interface Track {
    album: SimplifiedAlbum;
    artists: Artist[];
    available_markets: string[];
    disc_number: number;
    duration_ms: number;
    explicit: boolean;
    external_ids: ExternalId;
    external_urls: Dictionary<string>;
    href: string;
    id: string;
    is_playable: boolean;
    linked_from: Track;
    name: string;
    popularity: number;
    preview_url: string;
    restrictions: any[];
    track_number: number;
    type: string;
    uri: string;
}

export interface TuneableTrack {
    acousticness: number;
    danceability: number;
    duration_ms: number;
    energy: number;
    instrumentalness: number;
    key: number;
    liveness: number;
    loudness: number;
    mode: number;
    popularity: number;
    speechiness: number;
    tempo: number;
    time_signature: number;
    valence: number;
}
