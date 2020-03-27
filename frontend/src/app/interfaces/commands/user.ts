export enum UserCMD {
    LOGIN = 'login',
    TOKEN_LOGIN = 'token_login',
    FETCH_USERS = 'fetch_users',
}

interface LoginPayload {
    username: string;
    password: string;
}

interface TokenLoginPayload {
    token: string;
}


export interface UserTypeMap {
    [UserCMD.LOGIN]: LoginPayload;
    [UserCMD.TOKEN_LOGIN]: TokenLoginPayload;
    [UserCMD.FETCH_USERS]: null;
}

export interface User {
    // self: with token
    id: string;
    name: string;
    token: string;
}

export interface OtherUser {
    id: string;
    name: string;
    // others: no token
}

export interface LoginResult {
    success: boolean;
    user: User;
    message: string;
}
