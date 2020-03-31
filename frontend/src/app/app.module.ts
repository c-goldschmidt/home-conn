import { LoginComponent } from './components/login/login.component';
import { EntrypointComponent } from './components/entrypoint/entrypoint.component';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SocketService } from './services/socket.service';
import { FormsModule } from '@angular/forms';
import { UserService } from './services/user.service';
import { UserInfoComponent } from './components/user-info/user-info.component';
import { ChatBoxComponent } from './components/chatbox/chatbox.component';
import { ChatService } from './services/chat.service';
import { MessageComponent } from './components/chatbox/message-renderer/message.component';
import { TrustHTMLPipe } from './utils/trusted-html.pipe';
import { SpotifyMainComponent } from './components/spotify/spotify-main.component';
import { SpotifyService } from './services/spotify.service';
import { PlaybackImageComponent } from './components/spotify/playback-image/playback-image.component';
import { SpotifySidebarComponent } from './components/spotify/sidebar/spotify-sidebar.component';

@NgModule({
    declarations: [
        TrustHTMLPipe,
        AppComponent,
        EntrypointComponent,
        LoginComponent,
        UserInfoComponent,
        ChatBoxComponent,
        MessageComponent,
        SpotifyMainComponent,
        PlaybackImageComponent,
        SpotifySidebarComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule,
        MaterialModule,
        FlexLayoutModule,
        FormsModule,
    ],
    providers: [
        ChatService,
        SocketService,
        UserService,
        SpotifyService,
    ],
    entryComponents: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
