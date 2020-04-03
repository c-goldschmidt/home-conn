import { SpotifyService } from './../../services/spotify.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from '../../utils/unsub-component.baase';
import { CurrentlyPlaying, Track, Episode, Device } from '../../interfaces/spotify-api/full-api';
import { Image } from '../../interfaces/spotify-api/resources';

@Component({
    selector: 'app-spotify',
    templateUrl: './spotify-main.component.html',
    styleUrls: ['./spotify-main.component.scss'],
})
export class SpotifyMainComponent extends UnsubBase implements OnInit {
    public status: CurrentlyPlaying;
    public images: Image[] = null;
    public artistString: string = null;
    public devices: Device[] = [];

    constructor(
        private spotify: SpotifyService,
    ) { super(); }

    ngOnInit() {
        this.spotify.fetchStatus();
        this.spotify.fetchDevices();

        this.spotify.currentStatus$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(status => {
            this.status = status;
            this.updateMetadata();
        });

        this.spotify.devices$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(devices => {
            this.devices = devices;
        });
    }

    public next() { this.spotify.next(); }
    public prev() { this.spotify.prev(); }
    public pause() { this.spotify.pause(); }
    public resume() { this.spotify.resume(); }

    public pauseOrResume() {
        if (!this.status) {
            return;
        }

        if (this.status.is_playing) {
            this.pause();
        } else {
            this.resume();
        }
    }

    public switchToDevice(device: Device) {
        if (device.is_active) {
            return;
        }
        this.spotify.switchToDevice(device);
    }

    private updateMetadata() {
        this.images = null;
        this.artistString = null;

        if (!this.status) {
            return;
        }

        if (this.status.currently_playing_type === 'track') {
            const item =  (this.status.item as Track);
            this.images = item.album.images;
            this.artistString = item.artists.map(artist => artist.name). join(', ');
        } else {
            const item =  (this.status.item as Episode);
            this.images = item.images;
            this.artistString = item.show.name;
        }
    }
}
