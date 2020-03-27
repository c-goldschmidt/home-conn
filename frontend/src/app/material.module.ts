import { NgModule } from '@angular/core';
import {
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatCardModule,
    MatToolbarModule,
    MatSidenavModule,
} from '@angular/material';

@NgModule({
    exports: [
        MatToolbarModule,
        MatCardModule,
        MatSidenavModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
    ],
})
export class MaterialModule { }
