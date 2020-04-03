import { Device } from './../interfaces/spotify-api/full-api';
import { BehaviorSubject, of } from 'rxjs';
import { SocketService } from './socket.service';
import { Injectable } from '@angular/core';
import { SpotifyCMD } from '../interfaces/commands/spotify';
import { MessageType } from '../interfaces/comm';
import { Paginated } from '../interfaces/spotify-api/resources';
import { map, filter, take, tap } from 'rxjs/operators';
import { CurrentlyPlaying, Playlist, Track } from '../interfaces/spotify-api/full-api';
import { PlayableItem } from '../interfaces/spotify-api/adaptions';

@Injectable()
export class SpotifyService {
    public currentStatus$ = new BehaviorSubject<CurrentlyPlaying>(null);
    public playlists$ = new BehaviorSubject<Playlist[]>([]);
    public devices$ = new BehaviorSubject<Device[]>([]);
    public uriData$ = new BehaviorSubject<PlayableItem[]>([]);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<CurrentlyPlaying>('spotify_status_change', status => this.handleStatusChange(status));
        this.comm.registerCallback<Paginated<Playlist>>('spotify_playlist_result', playlists => this.handleSpotifyPlaylists(playlists));
        this.comm.registerCallback<Playlist>('spotify_update_playlist', playlist => this.handleUpdatePlaylists(playlist));
        this.comm.registerCallback<PlayableItem>('spotify_uri_result', item => this.handleURIResult(item));
        this.comm.registerCallback<Device[]>('spotify_devices_result', devices => this.handleDevicesResult(devices));
    }

    public fetchStatus() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.FETCH_STATUS, null);
    }

    public fetchDevices() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.FETCH_DEVICES, null);
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

    public switchToDevice(device: Device) {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.SWITCH_DEVICE, device);
    }

    private handleStatusChange(status: CurrentlyPlaying) {
        this.currentStatus$.next(status);
        if (status && status.item) {
            this.uriData$.next([...this.uriData$.getValue(), status.item]);
        }
    }

    private handleSpotifyPlaylists(playlists: Paginated<Playlist>) {
        this.playlists$.next(playlists.items);

        if (playlists.items) {
            this.uriData$.next([...this.uriData$.getValue(), ...playlists.items]);
        }
    }

    private handleUpdatePlaylists(playlist: Playlist) {
        this.playlists$.next((this.playlists$.getValue() || []).map(item => {
            return item.id === playlist.id ? playlist : item;
        }));
    }

    private handleURIResult(item: PlayableItem) {
        if (item) {
            this.uriData$.next([...this.uriData$.getValue(), item]);
        }
    }

    private handleDevicesResult(devices: Device[]) {
        this.devices$.next(devices);
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
