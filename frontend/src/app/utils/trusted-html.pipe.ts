import { DomSanitizer } from '@angular/platform-browser';
import { PipeTransform, Pipe } from '@angular/core';

@Pipe({name: 'trustHTML'})
export class TrustHTMLPipe implements PipeTransform {
    constructor(private sanitizer: DomSanitizer) { }

    transform(value: any): any {
        return this.sanitizer.bypassSecurityTrustHtml(value);
    }
}
