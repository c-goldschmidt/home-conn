import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { User } from 'src/app/interfaces/commands/user';

@Component({
    selector: 'app-user-info',
    templateUrl: './user-info.component.html',
    styleUrls: ['./user-info.component.scss'],
})
export class UserInfoComponent extends UnsubBase implements OnInit {
    public user: User = null;

    constructor(
        private userService: UserService,
    ) { super(); }

    ngOnInit() {
        this.userService.loggedInUser$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(user => this.user = user);
    }

    logout() {
        this.userService.logout();
    }
}
