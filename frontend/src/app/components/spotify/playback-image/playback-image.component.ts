import { Component, OnChanges, Input, ChangeDetectionStrategy } from '@angular/core';
import { Image } from '../../../interfaces/spotify-api/resources';

@Component({
    selector: 'app-playback-image',
    templateUrl: './playback-image.component.html',
    styleUrls: ['./playback-image.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlaybackImageComponent implements OnChanges {
    @Input() images: Image[];
    public usedImage: Image = null;

    constructor() { }

    ngOnChanges() {
        this.usedImage = this.images && this.images.length > 1 ? this.images[1] : null;
    }
}
