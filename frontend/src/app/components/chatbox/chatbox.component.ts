import { ChatService } from './../../services/chat.service';
import { Component, OnInit } from '@angular/core';
import { UnsubBase } from 'src/app/utils/unsub-component.baase';
import { takeUntil, filter } from 'rxjs/operators';

@Component({
    selector: 'app-chatbox',
    templateUrl: './chatbox.component.html',
    styleUrls: ['./chatbox.component.scss'],
})
export class ChatBoxComponent extends UnsubBase implements OnInit {
    public loading = true;
    public messages = [];
    public message = '';

    constructor(
        private chatService: ChatService,
    ) {
        super();
    }

    public send() {
        this.chatService.send(this.message);
        this.message = '';
    }

    ngOnInit() {
        this.loading = true;
        this.chatService.allMessages$.pipe(
            takeUntil(this.unsubscribe$),
            filter(messages => !!messages),
        ).subscribe(messages => {
            this.messages = messages;
            this.loading = false;
        });
        this.chatService.requestLog(100);
    }
}
