import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EntrypointComponent } from './components/entrypoint/entrypoint.component';

const routes: Routes = [{
    path: '',
    component: EntrypointComponent,
}];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
