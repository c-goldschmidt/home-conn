import { UserService } from './../../../services/user.service';
import { SpotifyService } from './../../../services/spotify.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil, filter, switchMap, tap } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { Playlist, CurrentlyPlaying } from 'src/app/interfaces/spotify-api/full-api';
import { PlayableItem } from 'src/app/interfaces/spotify-api/adaptions';

@Component({
    selector: 'app-spotify-sidenav',
    templateUrl: './spotify-sidebar.component.html',
    styleUrls: ['./spotify-sidebar.component.scss'],
})
export class SpotifySidebarComponent extends UnsubBase implements OnInit {
    public loggedIn = false;

    public currentContextUri: string;
    public ownerNames: string[];
    public playlistsByOwnerName = new Map<string, Playlist[]>();

    constructor(
        private spotify: SpotifyService,
        private user: UserService,
    ) { super(); }

    ngOnInit() {
        this.loadPlaylists();
        this.spotify.currentStatus$.pipe(takeUntil(this.unsubscribe$)).subscribe(status => {
            this.updateCurrentlyPlaying(status);
        });
    }

    private loadPlaylists() {
        this.user.loggedIn$.pipe(
            tap(loggedIn => this.loggedIn = loggedIn),
            filter(loggedIn => loggedIn),
            tap(() => this.spotify.fetchPlaylists()),
            switchMap(() => this.spotify.playlists$),
            takeUntil(this.unsubscribe$),
        ).subscribe(playlists => {
            playlists = playlists || [];

            this.playlistsByOwnerName = new Map<string, Playlist[]>();
            for (const playlist of playlists) {
                const old = this.playlistsByOwnerName.get(playlist.owner.display_name) || [];
                this.playlistsByOwnerName.set(playlist.owner.display_name, [...old, playlist]);
            }
            this.ownerNames = [...this.playlistsByOwnerName.keys()];

            window.dispatchEvent(new Event('resize'));
        });
    }

    private updateCurrentlyPlaying(status: CurrentlyPlaying) {
        if (!status || !status.context) {
            return;
        }
        this.currentContextUri = status.context.uri;
    }

    play(item: PlayableItem) {
        this.spotify.play(item);
    }
}
