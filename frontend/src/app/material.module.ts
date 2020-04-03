import { NgModule } from '@angular/core';
import {
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatCardModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatChipsModule,
} from '@angular/material';

@NgModule({
    exports: [
        MatToolbarModule,
        MatCardModule,
        MatSidenavModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        MatListModule,
        MatChipsModule,
    ],
})
export class MaterialModule { }
