import { BehaviorSubject, Subject } from 'rxjs';
import { ChatCMD, ChatMessage, ChatDeleteResult } from './../interfaces/commands/chat';
import { SocketService } from './socket.service';
import { MessageType } from '../interfaces/comm';
import { Injectable } from '@angular/core';

@Injectable()
export class ChatService {
    allMessages$ = new BehaviorSubject<ChatMessage[]>(null);
    newMessage$ = new Subject<ChatMessage>();

    constructor(private comm: SocketService) {
        this.comm.registerCallback<ChatMessage[]>('chat_backlog', messages => this.handleChatLog(messages));
        this.comm.registerCallback<ChatMessage>('chat_message', message => this.handleMessage(message));
        this.comm.registerCallback<ChatDeleteResult>('chat_delete_result', result => this.handleDeleteResult(result));
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

    private handleDeleteResult(result: ChatDeleteResult) {
        if (!result.success) {
            return;
        }
        this.allMessages$.next(this.allMessages$.value.filter(message => message.id !== result.id));
    }

    public send(message: string) {
        this.comm.sendMessage(
            MessageType.CHAT,
            ChatCMD.SEND,
            message,
        );
    }

    public deleteMessage(message: ChatMessage) {
        this.comm.sendMessage(
            MessageType.CHAT,
            ChatCMD.DELETE,
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
