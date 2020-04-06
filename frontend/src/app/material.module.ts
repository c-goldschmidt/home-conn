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
    MatDialogModule,
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
        MatDialogModule,
    ],
})
export class MaterialModule { }
