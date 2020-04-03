import { Component, OnInit, OnDestroy, HostListener, ChangeDetectorRef } from '@angular/core';
import { Subject } from 'rxjs';
import { SocketService } from './services/socket.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
    public sidenavToggle = false;
    public gtSm = false;

    private unsubscribe$ = new Subject<void>();

    constructor(private socket: SocketService, private cdr: ChangeDetectorRef) { }

    @HostListener('window:resize')
    public resize() {
        const newVal = window.innerWidth >= 960;
        if (newVal !== this.gtSm) {
            this.gtSm = newVal;
            this.cdr.detectChanges();
        }
    }

    public toggleSidenav() {
        this.sidenavToggle = !this.sidenavToggle;
        this.cdr.detectChanges();
    }

    get sidenavOpen() {
        return this.sidenavToggle || this.gtSm;
    }

    ngOnInit() {
        this.unsubscribe$ = new Subject<void>();
        this.resize();
        this.socket.connect();
    }

    ngOnDestroy() {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }
}
