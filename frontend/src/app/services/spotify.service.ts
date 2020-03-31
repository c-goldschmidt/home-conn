import { Artist, Album, Track, PlayableItem } from './../interfaces/spotify-api/items';
import { BehaviorSubject } from 'rxjs';
import { SocketService } from './socket.service';
import { Injectable } from '@angular/core';
import { SpotifyCMD } from '../interfaces/commands/spotify';
import { MessageType } from '../interfaces/comm';
import { PlaybackState } from '../interfaces/spotify-api/playback';
import { Playlist, BaseItem } from '../interfaces/spotify-api/items';
import { Paginated } from '../interfaces/spotify-api/resources';

@Injectable()
export class SpotifyService {
    public currentStatus$ = new BehaviorSubject<PlaybackState>(null);
    public playlists$ = new BehaviorSubject<Playlist[]>(null);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<PlaybackState>('spotify_status_change', status => this.handleStatusChange(status));
        this.comm.registerCallback<Paginated<Playlist>>('spotify_playlist_result', playlists => this.handleSpotifyPlaylists(playlists));
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

    private handleStatusChange(status: PlaybackState) {
        this.currentStatus$.next(status);
    }

    private handleSpotifyPlaylists(playlists: Paginated<Playlist>) {
        this.playlists$.next(playlists.items);
    }
}
