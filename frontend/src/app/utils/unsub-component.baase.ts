import { OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';

export abstract class UnsubBase implements OnDestroy {
    protected unsubscribe$ = new Subject<void>();

    ngOnDestroy() {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }
}
