import { UserCMD, UserTypeMap } from './commands/user';
import { ChatCMD, ChatTypeMap } from './commands/chat';
import { SpotifyTypeMap, SpotifyCMD } from './commands/spotify';

export enum MessageType {
    SPOTIFY = 'spotify',
    CHAT = 'chat',
    USER = 'user',
}

export interface MessageTypeMap {
    [MessageType.SPOTIFY]: SpotifyTypeMap;
    [MessageType.CHAT]: ChatTypeMap;
    [MessageType.USER]: UserTypeMap;
}

export interface CMDMap {
    [MessageType.SPOTIFY]: SpotifyCMD;
    [MessageType.CHAT]: ChatCMD;
    [MessageType.USER]: UserCMD;
}

export type SocketCallback<T> = (message: T) => void;
