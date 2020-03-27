import { BehaviorSubject } from 'rxjs';
import { ChatCMD, ChatMessage } from './../interfaces/commands/chat';
import { SocketService } from './socket.service';
import { MessageType } from '../interfaces/comm';
import { Injectable } from '@angular/core';

@Injectable()
export class ChatService {
    allMessages$ = new BehaviorSubject<ChatMessage[]>(null);
    newMessage$ = new BehaviorSubject<ChatMessage>(null);

    constructor(private comm: SocketService) {
        this.comm.registerCallback<ChatMessage[]>('chat_backlog', messages => this.handleChatLog(messages));
        this.comm.registerCallback<ChatMessage>('chat_message', message => this.handleMessage(message));
    }

    private handleChatLog(messages: ChatMessage[]) {
        this.allMessages$.next(messages);
    }

    private handleMessage(message: ChatMessage) {
        this.allMessages$.next([
            ...this.allMessages$.value,
            message,
        ]);
        this.newMessage$.next(message);
    }

    public send(message: string) {
        this.comm.sendMessage(
            MessageType.CHAT,
            ChatCMD.SEND,
            message,
        );
    }

    requestLog(maxEntries) {
        this.comm.sendMessage(
            MessageType.CHAT,
            ChatCMD.REQUEST_LOG,
            {max_entires: maxEntries},
        );
    }
}
