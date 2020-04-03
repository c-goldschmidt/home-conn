import { Injectable } from '@angular/core';
import { MessageTypeMap, MessageType, CMDMap, SocketCallback } from '../interfaces/comm';
import { ReplaySubject } from 'rxjs';
import { UserCMD } from '../interfaces/commands/user';

@Injectable()
export class SocketService {
    public ready$ = new ReplaySubject<boolean>(1);

    private socket: WebSocket;
    private connected = false;
    private callbacks = new Map<string, SocketCallback<any>[]>();
    private tryReconnect = false;

    constructor() { }

    sendMessage<MsgType extends MessageType, Cmd extends keyof MessageTypeMap[MsgType]>(
        type: MsgType,
        cmd: Cmd,
        payload: MessageTypeMap[MsgType][Cmd],
    ) {
        const message = JSON.stringify({
            type, cmd, payload,
        });
        if (!this.connected) {
            if (this.tryReconnect) {
                this.connect(message);
            } else {
                console.error('socket is closed, discard message', message);
            }

            return;
        }
        this.socket.send(message);
    }

    public reset() {
        this.disconnect();
        this.connect();
    }

    private getUrl() {
        const ssl = window.location.protocol.includes('https');
        const protocol = ssl ? 'wss' : 'ws';
        return  `${protocol}://${window.location.hostname}/${protocol}`;
    }

    connect(initialMessage: string = null) {
        this.tryReconnect = false;
        this.socket = new WebSocket(this.getUrl());

        this.socket.onopen = event => {
            this.connected = true;
            this.onConnected();
            this.ready$.next(true);

            if (initialMessage) {
                this.socket.send(initialMessage);
                console.log('prevoulsy lost connection reestablished');
            }
        };

        this.socket.onerror = event => {
            this.connected = false; // todo: actually?
            this.ready$.next(false);
            this.tryReconnect = true;
            console.error('connection error', event);
        };

        this.socket.onclose = event => {
            this.connected = false;
            this.ready$.next(true);
            this.tryReconnect = true;
            console.error('connection closed', event);
        };

        this.socket.onmessage = event => {
            try {
                const message = JSON.parse(event.data);
                this.handle(message);
            } catch {
                return;
            }
        };
    }

    private onConnected(initialMessage: string = null) {
        const token = localStorage.getItem('__userToken');
        if (token) {
            this.sendMessage(
                MessageType.USER,
                UserCMD.TOKEN_LOGIN,
                {token},
            );
        }
    }

    private handle<T>(message: {type: string, payload: any}) { // todo
        if (this.callbacks.has(message.type)) {
            for (const callback of this.callbacks.get(message.type)) {
                callback(message.payload);
            }
        } else {
            console.error('no handler for message type', message.type);
        }
    }

    registerCallback<T>(messageType: string, callback: SocketCallback<T>) {
        const prev = this.callbacks.get(messageType) || [];
        this.callbacks.set(messageType, [...prev, callback]);
    }

    disconnect() {
        this.socket.close();
    }
}
