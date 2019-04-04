import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import{TranslateModule} from '@ngx-translate/core';
import { IonicModule } from '@ionic/angular';

import { CreateTripPage } from './create-trip.page';

const routes: Routes = [
  {
    path: '',
    component: CreateTripPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    TranslateModule,
    RouterModule.forChild(routes)
  ],
  declarations: [CreateTripPage]
})
export class CreateTripPageModule {}
