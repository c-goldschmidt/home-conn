import { BehaviorSubject } from 'rxjs';
import { SocketService } from './socket.service';
import { Injectable } from '@angular/core';
import { SpotifyCMD } from '../interfaces/commands/spotify';
import { MessageType } from '../interfaces/comm';
import { PlaybackState } from '../interfaces/spotify-api/playback';

@Injectable()
export class SpotifyService {
    public currentStatus$ = new BehaviorSubject<PlaybackState>(null);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<PlaybackState>('spotify_status_change', status => this.handleStatusChange(status));
    }

    public fetchStatus() {
        this.comm.sendMessage(MessageType.SPOTIFY, SpotifyCMD.FETCH_STATUS, null);
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

    private handleStatusChange(status: PlaybackState) {
        this.currentStatus$.next(status);
    }
}
