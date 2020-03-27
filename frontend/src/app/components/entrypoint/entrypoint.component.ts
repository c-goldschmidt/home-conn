import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';

@Component({
    templateUrl: './entrypoint.component.html',
    styleUrls: ['./entrypoint.component.scss'],
})
export class EntrypointComponent extends UnsubBase implements OnInit {
    public loggedIn = false;

    constructor(
        private userService: UserService,
    ) { super(); }

    ngOnInit() {
        this.userService.loggedIn$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(loggedIn => this.loggedIn = loggedIn);
    }
}
