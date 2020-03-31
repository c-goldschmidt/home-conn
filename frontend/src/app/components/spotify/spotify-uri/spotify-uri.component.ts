import { takeUntil, take } from 'rxjs/operators';
import { ItemType } from './../../../interfaces/spotify-api/enums';
import { SpotifyService } from './../../../services/spotify.service';
import { Component, Input, OnChanges, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { Subscription } from 'rxjs';
import { PlayableItem } from 'src/app/interfaces/spotify-api/items';

interface UriContent {
    type: ItemType;
    id: string;
    name?: string;
}

@Component({
    selector: 'app-spotify-uri',
    templateUrl: './spotify-uri.component.html',
    styleUrls: ['./spotify-uri.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SpotifyUriComponent extends UnsubBase implements OnChanges {
    @Input() uri: string;

    public uriContent: UriContent;
    public isPlayable = false;
    private subscription: Subscription;

    constructor(
        private spotify: SpotifyService,
        private cdr: ChangeDetectorRef,
    ) {
        super();
    }

    ngOnChanges() {
        this.parseURI();
    }

    private parseURI() {
        this.uriContent = this.uriContent = {type: null, id: null};
        this.isPlayable = false;
        if (!this.uri) {
            return;
        }

        const split = this.uri.split(':');
        if (split.length < 3) {
            return;
        }

        this.uriContent = {
            type: split[1] as ItemType,
            id: split[2],
        };
        this.isPlayable = (
            this.uriContent.type === ItemType.PLAYLIST ||
            this.uriContent.type === ItemType.ALBUM ||
            this.uriContent.type === ItemType.ARTIST ||
            this.uriContent.type === ItemType.TRACK
        );
        this.fetchName();
    }

    public play() {
        if (!this.isPlayable) {
            return;
        }

        this.spotify.play({uri: this.uri} as PlayableItem);
    }

    private fetchName() {
        if (this.subscription) {
            this.subscription.unsubscribe();
        }

        this.subscription = this.spotify.resolveURI(this.uri).pipe(
            takeUntil(this.unsubscribe$),
            take(1),
        ).subscribe(content => {
            this.uriContent.name = content.name;
            this.subscription = null;
            this.cdr.detectChanges();
        });
    }
}
