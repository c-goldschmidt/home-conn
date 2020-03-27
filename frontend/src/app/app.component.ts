import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { SocketService } from './services/socket.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
    private unsubscribe$ = new Subject<void>();

    constructor(private socket: SocketService) { }

    ngOnInit() {
        this.unsubscribe$ = new Subject<void>();
        this.socket.connect();
    }

    ngOnDestroy() {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }
}
