import { SpotifyService } from './../../../services/spotify.service';
import { Component, OnInit, ChangeDetectionStrategy, OnChanges, Input, ChangeDetectorRef } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { Playlist, Track } from 'src/app/interfaces/spotify-api/full-api';

@Component({
    selector: 'app-playlist-add',
    templateUrl: './playlist-add.component.html',
    styleUrls: ['./playlist-add.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlaylistAddComponent extends UnsubBase implements OnInit, OnChanges {
    @Input() track: Track;

    public trackInPlaylist = false;
    public loading = true;
    private playlist: Playlist;

    constructor(
        private spotify: SpotifyService,
        private cdr: ChangeDetectorRef,
    ) { super(); }

    ngOnInit() {
        this.spotify.playlists$.pipe(takeUntil(this.unsubscribe$)).subscribe(playlists => {
            this.playlist = playlists.find(item => item.is_main_playlist);
            this.loading = !this.playlist;
            this.updateTrack();
        });
    }

    ngOnChanges() {
        this.updateTrack();
    }

    private updateTrack() {
        this.trackInPlaylist = false;
        if (!this.track || !this.playlist) {
            return;
        }

        const items = this.playlist.tracks.items || [];
        for (const track of items) {
            if (track.track.id === this.track.id) {
                this.trackInPlaylist = true;
                return;
            }
        }
    }

    addToPlaylist() {
        if (this.trackInPlaylist || !this.track || !this.playlist) {
            return;
        }
        this.loading = true;
        this.spotify.addToPlaylist(this.track);
    }
}
