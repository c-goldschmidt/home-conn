import { NgModule } from '@angular/core';
import {
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatCardModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
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
    ],
})
export class MaterialModule { }
