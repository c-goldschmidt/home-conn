import { User } from './user';
export enum ChatCMD {
    SEND = 'send',
    REQUEST_LOG = 'request_log'
}

export interface ChatMessage {
    sender_name: string;
    message: string;
    mentions: User[];
}

interface LogRequest {
    max_entires: number;
}

export interface ChatTypeMap {
    [ChatCMD.SEND]: string;
    [ChatCMD.REQUEST_LOG]: LogRequest;
}
