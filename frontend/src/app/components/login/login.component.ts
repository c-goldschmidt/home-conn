import { UserService } from './../../services/user.service';
import { Component, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent extends UnsubBase implements OnInit {
    public error: string;

    public username: string;
    public password: string;

    constructor(private userService: UserService) { super(); }

    ngOnInit() {
        this.username = localStorage.getItem('__userName');
        this.userService.loginError$.pipe(
            takeUntil(this.unsubscribe$),
        ).subscribe(error => this.error = error);
    }

    public login() {
        localStorage.setItem('__userName', this.username);
        this.userService.login(this.username, this.password);
    }

}
