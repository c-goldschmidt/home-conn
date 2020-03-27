import { ChatMessage } from './../../../interfaces/commands/chat';
import { Input, Component, ChangeDetectionStrategy, OnChanges, ChangeDetectorRef, TemplateRef, ViewChild } from '@angular/core';

interface MessagePart {
    before: string;
    value?: string;
    content?: string;
    template?: TemplateRef<any>;
}

@Component({
    selector: 'app-chat-message',
    templateUrl: './message.component.html',
    styleUrls: ['./message.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MessageComponent implements OnChanges {
    @Input() message: string;
    public messageData: MessagePart[] = [];

    @ViewChild('mention', {static: true}) private mention: TemplateRef<any>;
    @ViewChild('color', {static: true}) private color: TemplateRef<any>;
    @ViewChild('unknown', {static: true}) private unknown: TemplateRef<any>;

    constructor(private cdr: ChangeDetectorRef) { }

    ngOnChanges() {
        this.parseMessage();
    }

    private parseMessage() {
        this.messageData = this.parseMessagePart(this.message);
        this.cdr.detectChanges();
    }

    private parseMessagePart(message: string): MessagePart[] {
        const regex = /(?<before>[^\[]*)\[(?<tagName>.+?)=?(?<value>.*?)](?<content>.+?)\[\/\2]/gmi;
        if (!message || !message.match(regex)) {
            return [{before: message || ''}];
        }

        let result = regex.exec(message);
        const resultContent = [];
        while (result) {
            resultContent.push({
                before: result.groups.before,
                template: this.getTemplate(result.groups.tagName),
                value: result.groups.value,
                content: result.groups.content,
            });
            result = regex.exec(message);
        }

        return resultContent;
    }

    private getTemplate(tagIn: string) {
        switch (tagIn) {
            case 'mention':
                return this.mention;
            case 'color':
                return this.color;
            default:
                return this.unknown;
        }
    }
}
