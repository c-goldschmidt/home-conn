import { OtherUser } from './../interfaces/commands/user';
import { SocketService } from './socket.service';
import { BehaviorSubject } from 'rxjs';
import { MessageType } from '../interfaces/comm';
import { UserCMD, LoginResult, User } from '../interfaces/commands/user';
import { first } from 'rxjs/operators';
import { Injectable } from '@angular/core';

@Injectable()
export class UserService {
    public loggedIn$ = new BehaviorSubject<boolean>(false);
    public loggedInUser$ = new BehaviorSubject<User>(null);
    public loginError$ = new BehaviorSubject<string>(null);

    public otherUsers$ = new BehaviorSubject<OtherUser[]>([]);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<LoginResult>('login_result', message => this.handleLoginResult(message));
        this.comm.registerCallback<OtherUser[]>('user_result', message => this.handleUserResult(message));
    }

    public login(username: string, password: string) {
        this.comm.sendMessage(
            MessageType.USER,
            UserCMD.LOGIN,
            {username, password},
        );
    }

    public logout() {
        this.loggedIn$.next(false);
        this.loggedInUser$.next(null);
        localStorage.removeItem('__userToken');
    }

    private fetchUsers() {
        this.comm.sendMessage(
            MessageType.USER,
            UserCMD.FETCH_USERS,
            null,
        );
    }

    private handleUserResult(users: OtherUser[]) {
        this.otherUsers$.next(users);
    }

    private handleLoginResult(message: LoginResult) {
        this.loggedIn$.next(message.success);
        if (message.success) {
            localStorage.setItem('__userToken', message.user.token);
            this.loggedInUser$.next(message.user);
            this.fetchUsers();
        } else {
            this.loginError$.next(message.message);
        }
    }
}
