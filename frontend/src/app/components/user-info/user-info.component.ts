import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { User } from 'src/app/interfaces/commands/user';
import { MatDialog } from '@angular/material';

@Component({
    selector: 'app-user-info',
    templateUrl: './user-info.component.html',
    styleUrls: ['./user-info.component.scss'],
})
export class UserInfoComponent extends UnsubBase implements OnInit {
    public user: User = null;
    public authRequired: string = null;

    constructor(
        private userService: UserService,
        private matDialog: MatDialog,
    ) { super(); }

    ngOnInit() {
        this.userService.loggedInUser$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(user => this.user = user);

        this.userService.needAuth$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(url => {
            this.authRequired = url;
        });
    }

    public logout() {
        this.userService.logout();
    }

    public openAuthDialog() {
        const specs = [
            'location=no',
            'menubar=no',
            'status=no',
            'titlebar=no',
        ];
        window.open(this.authRequired, 'Spotify Auth', specs.join(','), false);
    }
}
