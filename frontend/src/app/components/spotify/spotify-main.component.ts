import { SpotifyService } from './../../services/spotify.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { PlaybackState } from 'src/app/interfaces/spotify-api/playback';

@Component({
    selector: 'app-spotify',
    templateUrl: './spotify-main.component.html',
    styleUrls: ['./spotify-main.component.scss'],
})
export class SpotifyMainComponent extends UnsubBase implements OnInit {
    public status: PlaybackState;

    constructor(
        private spotify: SpotifyService,
    ) { super(); }

    ngOnInit() {
        this.spotify.fetchStatus();
        this.spotify.fetchPlaylists();
        this.spotify.currentStatus$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(status => this.status = status);
    }

    next() { this.spotify.next(); }
    prev() { this.spotify.prev(); }
    pause() { this.spotify.pause(); }
    resume() { this.spotify.resume(); }

    pauseOrResume() {
        if (!this.status) {
            return;
        }

        if (this.status.is_playing) {
            this.pause();
        } else {
            this.resume();
        }
    }
}
