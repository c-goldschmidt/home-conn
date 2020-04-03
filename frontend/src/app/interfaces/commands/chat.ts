import { User } from './user';

export enum ChatCMD {
    SEND = 'send',
    REQUEST_LOG = 'request_log',
    DELETE = 'delete',
}

export interface ChatMessage {
    id: number;
    sender: User;
    message: string;
    mentions: User[];
}

export interface ChatDeleteResult {
    success: boolean;
    error?: string;
    id?: number;
}

interface LogRequest {
    max_entires: number;
}

export interface ChatTypeMap {
    [ChatCMD.SEND]: string;
    [ChatCMD.REQUEST_LOG]: LogRequest;
    [ChatCMD.DELETE]: ChatMessage;
}
