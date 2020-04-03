import { User } from './../../interfaces/commands/user';
import { ChatMessage } from './../../interfaces/commands/chat';
import { UserService } from './../../services/user.service';
import { ChatService } from './../../services/chat.service';
import { Component, OnInit, HostListener } from '@angular/core';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { takeUntil, filter } from 'rxjs/operators';

@Component({
    selector: 'app-chatbox',
    templateUrl: './chatbox.component.html',
    styleUrls: ['./chatbox.component.scss'],
})
export class ChatBoxComponent extends UnsubBase implements OnInit {
    public loading = true;
    public messages: ChatMessage[] = [];
    public message = '';
    public user: User;

    private notificationsEnabled = false;
    private currentNote: Notification;

    constructor(
        private chatService: ChatService,
        private userService: UserService,
    ) {
        super();

        Notification.requestPermission().then((result) => {
            this.notificationsEnabled = result === 'granted';
        });
    }

    public send() {
        this.chatService.send(this.message);
        this.message = '';
    }

    public deleteMessage(message: ChatMessage) {
        this.chatService.deleteMessage(message);
    }

    ngOnInit() {
        this.loading = true;
        this.userService.loggedInUser$.pipe(takeUntil(this.unsubscribe$)).subscribe(user => {
            this.user = user;
        });

        this.chatService.allMessages$.pipe(
            takeUntil(this.unsubscribe$),
            filter(messages => !!messages),
        ).subscribe(messages => {
            this.messages = messages;
            this.loading = false;
        });

        this.chatService.newMessage$.pipe(takeUntil(this.unsubscribe$)).subscribe(message => {
            this.checkNotification(message);
        });
        this.chatService.requestLog(100);
    }

    private checkNotification(message: ChatMessage) {
        if (!this.user || !this.notificationsEnabled) {
            return;
        }

        if (message.mentions.find(user => user.id === this.user.id)) {
            const text = message.message.replace(/\[.+?]/g, '');
            this.currentNote = new Notification('New message', { body: text});
        }
    }
}
