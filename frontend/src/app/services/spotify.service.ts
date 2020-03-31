import { Track, PlayableItem, Playlist } from './../interfaces/spotify-api/items';
import { BehaviorSubject, of } from 'rxjs';
import { SocketService } from './socket.service';
import { Injectable } from '@angular/core';
import { SpotifyCMD } from '../interfaces/commands/spotify';
import { MessageType } from '../interfaces/comm';
import { PlaybackState } from '../interfaces/spotify-api/playback';
import { Paginated } from '../interfaces/spotify-api/resources';
import { map, filter, take, tap } from 'rxjs/operators';

@Injectable()
export class SpotifyService {
    public currentStatus$ = new BehaviorSubject<PlaybackState>(null);
    public playlists$ = new BehaviorSubject<Playlist[]>([]);
    public uriData$ = new BehaviorSubject<PlayableItem[]>([]);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<PlaybackState>('spotify_status_change', status => this.handleStatusChange(status));
        this.comm.registerCallback<Paginated<Playlist>>('spotify_playlist_result', playlists => this.handleSpotifyPlaylists(playlists));
        this.comm.registerCallback<Playlist>('spotify_update_playlist', playlist => this.handleUpdatePlaylists(playlist));
        this.comm.registerCallback<PlayableItem>('spotify_uri_result', item => this.handleURIResult(item));
    }

    public fetchStatus() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.FETCH_STATUS, null);
    }

    public fetchPlaylists() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.FETCH_PLAYLISTS, null);
    }

    public pause() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.PAUSE, null);
    }

    public resume() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.RESUME, null);
    }

    public next() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.NEXT, null);
    }

    public prev() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.PREV, null);
    }

    public play(item: PlayableItem) {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.PLAY, item);
    }

    public addToPlaylist(item: Track) {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.ADD_TO_PLAYLIST, item);
    }

    private handleStatusChange(status: PlaybackState) {
        this.currentStatus$.next(status);
        this.uriData$.next([...this.uriData$.getValue(), status.item]);
    }

    private handleSpotifyPlaylists(playlists: Paginated<Playlist>) {
        this.playlists$.next(playlists.items);
        this.uriData$.next([...this.uriData$.getValue(), ...playlists.items]);
    }

    private handleUpdatePlaylists(playlist: Playlist) {
        this.playlists$.next((this.playlists$.getValue() || []).map(item => {
            return item.id === playlist.id ? playlist : item;
        }));
    }

    private handleURIResult(item: PlayableItem) {
        this.uriData$.next([...this.uriData$.getValue(), item]);
    }

    public resolveURI(uri: string) {
        const cached = this.uriData$.getValue().find(item => item.uri === uri);
        if (cached) {
            return of(cached);
        }

        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.RESOLVE_URI, uri);
        return this.uriData$.pipe(
            map(data => data.find(item => item.uri === uri)),
            filter(data => !!data),
            take(1),
        );
    }
}
